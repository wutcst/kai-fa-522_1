#include "engine/narrative/Executor.hpp"

#include <stdexcept>

namespace novel::narrative {

Executor::Executor(const script::ScriptModule& module, BuiltinApi& api, platform::IBackend& backend)
    : module_(module), api_(api), backend_(backend), evaluator_(api.context(), api) {
    for (std::size_t i = 0; i < module_.labels.size(); ++i) {
        label_index_[module_.labels[i].name] = i;
    }
}

platform::FlowSignal Executor::run(const std::string& entry_label) {
    finished_ = false;
    pending_signal_ = platform::FlowSignal::Continue;
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
        if (pending_signal_ != platform::FlowSignal::Continue) {
            return pending_signal_;
        }
        if (advance_pc) {
            ++frame.index;
        }
    }

    return platform::FlowSignal::Continue;
}

const script::Label* Executor::find_label(const std::string& name) const {
    auto it = label_index_.find(name);
    if (it == label_index_.end()) {
        return nullptr;
    }
    return &module_.labels[it->second];
}

bool Executor::execute_statement(const script::Stmt& stmt, std::vector<Frame>& frames) {
    using Kind = script::Stmt::Kind;

    switch (stmt.kind()) {
    case Kind::Say: {
        auto& s = static_cast<const script::SayStmt&>(stmt);
        auto signal = backend_.say("", evaluate_text(*s.text));
        if (signal != platform::FlowSignal::Continue) {
            pending_signal_ = signal;
        }
        return true;
    }

    case Kind::Assign: {
        auto& s = static_cast<const script::AssignStmt&>(stmt);
        api_.context().set(s.name, evaluator_.evaluate(*s.value));
        return true;
    }

    case Kind::Jump: {
        auto& s = static_cast<const script::JumpStmt&>(stmt);
        const script::Label* label = find_label(s.label);
        if (!label) {
            throw std::runtime_error("unknown label: " + s.label);
        }
        while (frames.size() > 1) {
            frames.pop_back();
        }
        frames.back() = Frame{&label->body, 0};
        return_stack_.clear();
        return false;
    }

    case Kind::Call: {
        auto& s = static_cast<const script::CallStmt&>(stmt);
        const script::Label* label = find_label(s.label);
        if (!label) {
            throw std::runtime_error("unknown label: " + s.label);
        }
        Frame& caller = frames.back();
        return_stack_.push_back(ReturnPoint{caller.statements, caller.index + 1});
        frames.push_back(Frame{&label->body, 0});
        return false;
    }

    case Kind::Return: {
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

    case Kind::Scene: {
        auto& s = static_cast<const script::SceneStmt&>(stmt);
        api_.call("scene", {core::Value::from_string(s.room_id)});
        backend_.on_scene_changed(s.room_id);
        return true;
    }

    case Kind::Go: {
        auto& s = static_cast<const script::GoStmt&>(stmt);
        const std::string direction = evaluate_text(*s.direction);
        api_.call("go", {core::Value::from_string(direction)});
        return true;
    }

    case Kind::Bg: {
        auto& s = static_cast<const script::BgStmt&>(stmt);
        backend_.show_background(s.image_path);
        return true;
    }

    case Kind::Show: {
        auto& s = static_cast<const script::ShowStmt&>(stmt);
        backend_.show_sprite(s.tag, s.image_path, s.position);
        return true;
    }

    case Kind::Hide: {
        auto& s = static_cast<const script::HideStmt&>(stmt);
        backend_.hide_sprite(s.tag);
        return true;
    }

    case Kind::PlayMusic: {
        auto& s = static_cast<const script::PlayMusicStmt&>(stmt);
        int fadein_ms = static_cast<int>(s.fadein * 1000.0);
        backend_.play_music(s.path, fadein_ms, s.noloop, s.volume);
        return true;
    }

    case Kind::StopMusic: {
        auto& s = static_cast<const script::StopMusicStmt&>(stmt);
        int fadeout_ms = static_cast<int>(s.fadeout * 1000.0);
        backend_.stop_music(fadeout_ms);
        return true;
    }

    case Kind::StopSound: {
        backend_.stop_sound();
        return true;
    }

    case Kind::PlaySound: {
        auto& s = static_cast<const script::PlaySoundStmt&>(stmt);
        backend_.play_sound(s.path, s.loop);
        return true;
    }

    case Kind::Dialogue: {
        auto& s = static_cast<const script::DialogueStmt&>(stmt);
        auto signal = backend_.say(s.speaker, evaluate_text(*s.text));
        if (signal != platform::FlowSignal::Continue) {
            pending_signal_ = signal;
        }
        return true;
    }

    case Kind::If: {
        auto& s = static_cast<const script::IfStmt&>(stmt);
        const script::StmtList* body = &s.else_body;
        for (const auto& branch : s.branches) {
            if (evaluator_.evaluate(*branch.condition).as_bool()) {
                body = &branch.body;
                break;
            }
        }
        frames.push_back(Frame{body, 0});
        return false;
    }

    case Kind::Menu: {
        auto& s = static_cast<const script::MenuStmt&>(stmt);
        std::vector<std::string> captions;
        captions.reserve(s.choices.size());
        for (const auto& choice : s.choices) {
            captions.push_back(choice.caption);
        }

        auto result = backend_.choose(captions);
        if (result.signal != platform::FlowSignal::Continue) {
            pending_signal_ = result.signal;
            return false;
        }
        frames.push_back(Frame{&s.choices[static_cast<std::size_t>(result.selection)].body, 0});
        return false;
    }
    }

    throw std::runtime_error("unsupported statement");
}

std::string Executor::evaluate_text(const script::Expr& expr) const {
    return evaluator_.evaluate_text(expr);
}

} // namespace novel::narrative
