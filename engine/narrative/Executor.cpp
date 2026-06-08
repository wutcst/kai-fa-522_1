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
    current_label_ = entry_label;
    current_index_ = 0;

    const script::Label* entry = find_label(entry_label);
    if (!entry) {
        throw std::runtime_error("unknown entry label: " + entry_label);
    }

    std::vector<Frame> frames;
    frames.push_back(Frame{&entry->body, 0});
    return run_frames(std::move(frames));
}

platform::FlowSignal Executor::run_from_save(const core::GameSaveState& state) {
    finished_ = false;
    pending_signal_ = platform::FlowSignal::Continue;
    return_stack_.clear();

    for (const auto& [name, value] : state.variables) {
        api_.context().set(name, value);
    }

    restore_visual_state(state);

    const script::Label* entry = find_label(state.label);
    if (!entry) {
        throw std::runtime_error("unknown save label: " + state.label);
    }

    for (const auto& frame : state.return_stack) {
        const script::Label* label = find_label(frame.label);
        if (!label) {
            throw std::runtime_error("unknown save return label: " + frame.label);
        }
        return_stack_.push_back(ReturnPoint{&label->body, frame.index});
    }

    current_label_ = state.label;
    current_index_ = state.statement_index;

    std::vector<Frame> frames;
    frames.push_back(Frame{&entry->body, state.statement_index});
    return run_frames(std::move(frames));
}

platform::FlowSignal Executor::run_frames(std::vector<Frame> frames) {
    while (!frames.empty() && !finished_) {
        Frame& frame = frames.back();
        current_label_ = label_for_statements(frame.statements);
        current_index_ = frame.index;

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

std::string Executor::label_for_statements(const script::StmtList* list) const {
    for (const auto& label : module_.labels) {
        if (&label.body == list) {
            return label.name;
        }
    }
    return {};
}

core::GameSaveState Executor::capture_state(const std::string& current_label,
                                            std::size_t current_index) const {
    core::GameSaveState state;
    state.label = current_label;
    state.statement_index = current_index;
    state.variables = api_.context().variables();
    state.background = backend_.current_background();
    state.sprites = backend_.current_sprites();

    const core::Value day = api_.context().get("day");
    if (!day.is_nil()) {
        state.day = static_cast<int>(day.as_number());
    }
    const core::Value glitch_count = api_.context().get("glitch_count");
    if (!glitch_count.is_nil()) {
        state.glitch_count = static_cast<int>(glitch_count.as_number());
    }
    const core::Value save_generation = api_.context().get("save_generation");
    if (!save_generation.is_nil()) {
        state.save_generation = static_cast<int>(save_generation.as_number());
    }

    state.corrupted = state.day >= 3 || state.glitch_count >= 2;

    for (const auto& point : return_stack_) {
        core::ReturnFrame frame;
        frame.label = label_for_statements(point.statements);
        frame.index = point.index;
        if (!frame.label.empty()) {
            state.return_stack.push_back(frame);
        }
    }
    return state;
}

void Executor::restore_visual_state(const core::GameSaveState& state) {
    if (!state.background.empty()) {
        backend_.show_background(state.background);
    }
    backend_.clear_sprites();
    for (const auto& sprite : state.sprites) {
        backend_.show_sprite(sprite.tag, sprite.path, sprite.position);
    }
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

    case Kind::PlayAmbient: {
        auto& s = static_cast<const script::PlayAmbientStmt&>(stmt);
        backend_.play_ambient(s.path);
        return true;
    }

    case Kind::StopAmbient: {
        backend_.stop_ambient();
        return true;
    }

    case Kind::Glitch: {
        auto& s = static_cast<const script::GlitchStmt&>(stmt);
        backend_.glitch(s.type, s.duration_ms);
        return true;
    }

    case Kind::WindowTitle: {
        auto& s = static_cast<const script::WindowTitleStmt&>(stmt);
        if (s.reset) {
            backend_.reset_window_title();
        } else {
            backend_.set_window_title(s.title);
        }
        return true;
    }

    case Kind::FakeCrash: {
        auto& s = static_cast<const script::FakeCrashStmt&>(stmt);
        backend_.fake_crash(s.message);
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
