#include "engine/narrative/Executor.hpp"

#include <stdexcept>

namespace novel::narrative {

Executor::Executor(const script::ScriptModule& module, BuiltinApi& api, platform::IBackend& backend)
    : module_(module), api_(api), backend_(backend), evaluator_(api.context(), api) {}

ExecutionResult Executor::run(const std::string& entry_label) {
    finished_ = false;
    return_stack_.clear();

    const script::Label* entry = find_label(entry_label);
    if (!entry) {
        throw std::runtime_error("unknown entry label: " + entry_label);
    }

    std::vector<Frame> frames;
    frames.push_back(Frame{&entry->body, 0});

    while (!frames.empty() && !finished_) {
        Frame& frame = frames.back();
        if (frame.index >= frame.statements->size()) {
            frames.pop_back();
            if (frames.empty()) {
                finished_ = true;
                break;
            }
            ++frames.back().index;
            continue;
        }

        const script::Stmt& stmt = *(*frame.statements)[frame.index];
        const bool advance_pc = execute_statement(stmt, frames);
        if (advance_pc) {
            ++frame.index;
        }
    }

    return ExecutionResult::Finished;
}

const script::Label* Executor::find_label(const std::string& name) const {
    for (const auto& label : module_.labels) {
        if (label.name == name) {
            return &label;
        }
    }
    return nullptr;
}

bool Executor::execute_statement(const script::Stmt& stmt, std::vector<Frame>& frames) {
    if (const auto* say = dynamic_cast<const script::SayStmt*>(&stmt)) {
        backend_.say(evaluate_text(*say->text));
        return true;
    }

    if (const auto* assign = dynamic_cast<const script::AssignStmt*>(&stmt)) {
        api_.context().set(assign->name, evaluator_.evaluate(*assign->value));
        return true;
    }

    if (const auto* jump = dynamic_cast<const script::JumpStmt*>(&stmt)) {
        const script::Label* label = find_label(jump->label);
        if (!label) {
            throw std::runtime_error("unknown label: " + jump->label);
        }
        while (frames.size() > 1) {
            frames.pop_back();
        }
        frames.back() = Frame{&label->body, 0};
        return_stack_.clear();
        return false;
    }

    if (const auto* call = dynamic_cast<const script::CallStmt*>(&stmt)) {
        const script::Label* label = find_label(call->label);
        if (!label) {
            throw std::runtime_error("unknown label: " + call->label);
        }
        Frame& caller = frames.back();
        return_stack_.push_back(ReturnPoint{caller.statements, caller.index + 1});
        frames.push_back(Frame{&label->body, 0});
        return false;
    }

    if (dynamic_cast<const script::ReturnStmt*>(&stmt)) {
        if (!return_stack_.empty()) {
            const ReturnPoint resume = return_stack_.back();
            return_stack_.pop_back();
            frames.pop_back();
            frames.back() = Frame{resume.statements, resume.index};
        } else {
            finished_ = true;
        }
        return false;
    }

    if (const auto* scene = dynamic_cast<const script::SceneStmt*>(&stmt)) {
        api_.call("scene", {core::Value::from_string(scene->room_id)});
        backend_.on_scene_changed(scene->room_id);
        return true;
    }

    if (const auto* go = dynamic_cast<const script::GoStmt*>(&stmt)) {
        const std::string direction = evaluate_text(*go->direction);
        api_.call("go", {core::Value::from_string(direction)});
        return true;
    }

    if (const auto* if_stmt = dynamic_cast<const script::IfStmt*>(&stmt)) {
        const script::StmtList* body = &if_stmt->else_body;
        for (const auto& branch : if_stmt->branches) {
            if (evaluator_.evaluate(*branch.condition).as_bool()) {
                body = &branch.body;
                break;
            }
        }
        frames.back().index += 1;
        frames.push_back(Frame{body, 0});
        return false;
    }

    if (const auto* menu = dynamic_cast<const script::MenuStmt*>(&stmt)) {
        std::vector<std::string> captions;
        captions.reserve(menu->choices.size());
        for (const auto& choice : menu->choices) {
            captions.push_back(choice.caption);
        }

        const int selected = backend_.choose(captions);
        frames.back().index += 1;
        frames.push_back(Frame{&menu->choices[static_cast<std::size_t>(selected)].body, 0});
        return false;
    }

    throw std::runtime_error("unsupported statement");
}

std::string Executor::evaluate_text(const script::Expr& expr) const {
    return evaluator_.evaluate_text(expr);
}

} // namespace novel::narrative
