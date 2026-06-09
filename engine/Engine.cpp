#include "engine/Engine.hpp"

#include "engine/core/ScriptLoader.hpp"
#include "engine/narrative/Executor.hpp"
#include "engine/narrative/ExpressionEvaluator.hpp"

#include <SDL.h>
#include <algorithm>
#include <chrono>
#include <ctime>
#include <filesystem>
#include <stdexcept>
#include <vector>

namespace novel {

namespace {

std::uint64_t now_ms() {
    return static_cast<std::uint64_t>(SDL_GetTicks());
}

} // namespace

Engine::Engine(platform::IBackend& backend,
               std::filesystem::path game_root,
               std::filesystem::path content_root,
               core::PersistentStore& persistent)
    : backend_(backend),
      game_root_(std::move(game_root)),
      content_root_(std::move(content_root)),
      save_manager_(game_root_),
      persistent_(persistent) {
    api_ = std::make_unique<narrative::BuiltinApi>(world_, player_, context_);
    register_meta_functions();
    session_start_ms_ = now_ms();
}

void Engine::register_meta_functions() {
    register_native("get_playthrough", [this](const std::vector<core::Value>&) {
        return core::Value::from_number(persistent_.playthrough_count());
    });
    register_native("get_launch_count", [this](const std::vector<core::Value>&) {
        return core::Value::from_number(persistent_.launch_count());
    });
    register_native("get_hour", [](const std::vector<core::Value>&) {
        const std::time_t now = std::time(nullptr);
        std::tm local_tm{};
#if defined(_WIN32)
        localtime_s(&local_tm, &now);
#else
        localtime_r(&now, &local_tm);
#endif
        return core::Value::from_number(local_tm.tm_hour);
    });
    register_native("character_exists", [this](const std::vector<core::Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("character_exists(name) expects 1 argument");
        }
        return core::Value::from_bool(save_manager_.character_exists(args[0].as_string()));
    });
    register_native("delete_character", [this](const std::vector<core::Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("delete_character(name) expects 1 argument");
        }
        return core::Value::from_bool(save_manager_.delete_character(args[0].as_string()));
    });
    register_native("write_game_file", [this](const std::vector<core::Value>& args) {
        if (args.size() != 2) {
            throw std::runtime_error("write_game_file(path, content) expects 2 arguments");
        }
        return core::Value::from_bool(
            save_manager_.write_game_file(args[0].as_string(), args[1].as_string()));
    });
    register_native("game_file_exists", [this](const std::vector<core::Value>& args) {
        if (args.size() != 1) {
            throw std::runtime_error("game_file_exists(path) expects 1 argument");
        }
        return core::Value::from_bool(save_manager_.game_file_exists(args[0].as_string()));
    });
}

void Engine::prepare_new_game() {
    bootstrap();
    save_manager_.restore_characters(content_root_);
    context_.set("playthrough", core::Value::from_number(persistent_.playthrough_count()));
    context_.set("launch_count", core::Value::from_number(persistent_.launch_count()));
    context_.set("save_generation", core::Value::from_number(0));
    context_.set("just_loaded", core::Value::from_bool(false));
    context_.set("monika_chr_deleted", core::Value::from_bool(false));
}

void Engine::load_script_file(const std::filesystem::path& path) {
    apply_module(core::ScriptLoader::load_file(path));
}

void Engine::load_script_directory(const std::filesystem::path& dir_path) {
    namespace fs = std::filesystem;
    std::vector<fs::path> files;
    for (const auto& entry : fs::directory_iterator(dir_path)) {
        if (entry.is_regular_file() && entry.path().extension() == ".rpy") {
            files.push_back(entry.path());
        }
    }
    std::sort(files.begin(), files.end());
    for (const auto& file : files) {
        load_script_file(file);
    }
}

void Engine::load_script_source(const std::string& source, const std::string& name) {
    apply_module(core::ScriptLoader::load_source(source, name));
}

void Engine::apply_module(script::ScriptModule incoming) {
    std::vector<script::ScriptModule> parts;
    parts.push_back(std::move(module_));
    parts.push_back(std::move(incoming));
    module_ = core::ScriptLoader::merge(std::move(parts));
    bootstrapped_ = false;
}

void Engine::bootstrap() {
    world_.clear();
    for (const auto& room_def : module_.rooms) {
        adventure::Room& room = world_.define_room(room_def.id);
        room.set_description(room_def.description);
        for (const auto& [direction, target] : room_def.exits) {
            room.set_exit(direction, target);
        }
    }

    apply_defaults();

    const core::Value start_room = context_.get("start_room");
    if (!start_room.is_nil()) {
        player_.set_room(start_room.as_string());
    } else if (!module_.rooms.empty()) {
        player_.set_room(module_.rooms.front().id);
    }

    bootstrapped_ = true;
}

void Engine::apply_defaults() {
    narrative::ExpressionEvaluator evaluator(context_, *api_);
    for (const auto& def : module_.defaults) {
        context_.set(def.name, evaluator.evaluate(*def.value));
    }
}

bool Engine::handle_save_request(narrative::Executor& executor) {
    const auto slots = save_manager_.list_slots();
    const int slot = backend_.show_slot_menu(true, slots);
    if (slot < 0) {
        return false;
    }

    auto state = executor.capture_state(executor.current_label(), executor.current_index());
    const core::Value generation = context_.get("save_generation");
    state.save_generation = generation.is_nil() ? 1 : static_cast<int>(generation.as_number()) + 1;
    context_.set("save_generation", core::Value::from_number(state.save_generation));
    state.corrupted = state.day >= 3 || state.glitch_count >= 2;
    return save_manager_.save_slot(slot, state);
}

void Engine::run_save_loaded_hook() {
    for (const auto& label : module_.labels) {
        if (label.name == "save_loaded_hook") {
            narrative::Executor hook_executor(module_, *api_, backend_);
            hook_executor.run("save_loaded_hook");
            break;
        }
    }
}

platform::FlowSignal Engine::run_executor(
    narrative::Executor& executor,
    const std::function<platform::FlowSignal(narrative::Executor&)>& start) {
    platform::FlowSignal signal = start(executor);

    while (signal == platform::FlowSignal::SaveRequest) {
        handle_save_request(executor);
        auto state = executor.capture_state(executor.current_label(), executor.current_index());
        signal = executor.run_from_save(state);
    }

    while (signal == platform::FlowSignal::LoadRequest) {
        const auto resume = executor.capture_state(executor.current_label(), executor.current_index());
        const auto slots = save_manager_.list_slots();
        const int slot = backend_.show_slot_menu(false, slots);
        if (slot < 0) {
            signal = executor.run_from_save(resume);
            continue;
        }

        auto loaded = save_manager_.load_slot(slot);
        if (!loaded) {
            signal = executor.run_from_save(resume);
            continue;
        }

        context_.set("just_loaded", core::Value::from_bool(true));
        run_save_loaded_hook();
        context_.set("just_loaded", core::Value::from_bool(false));
        signal = executor.run_from_save(*loaded);
    }

    if (signal == platform::FlowSignal::Continue) {
        mark_game_completed();
    }

    const auto elapsed = (now_ms() - session_start_ms_) / 1000;
    if (elapsed > 0) {
        persistent_.add_play_seconds(elapsed);
    }

    return signal;
}

void Engine::mark_game_completed() {
    const core::Value ending_reached = context_.get("ending_reached");
    if (!ending_reached.is_nil() && ending_reached.as_bool()) {
        persistent_.on_game_completed();
    }
}

platform::FlowSignal Engine::run(const std::string& entry_label) {
    if (!bootstrapped_) {
        bootstrap();
    }

    narrative::Executor executor(module_, *api_, backend_);
    return run_executor(executor, [&](narrative::Executor& exec) {
        return exec.run(entry_label);
    });
}

platform::FlowSignal Engine::run_from_slot(int slot) {
    if (!bootstrapped_) {
        bootstrap();
    }

    auto state = save_manager_.load_slot(slot);
    if (!state) {
        throw std::runtime_error("failed to load save slot " + std::to_string(slot));
    }

    context_.set("just_loaded", core::Value::from_bool(true));
    context_.set("just_loaded", core::Value::from_bool(true));
    run_save_loaded_hook();
    context_.set("just_loaded", core::Value::from_bool(false));

    narrative::Executor executor(module_, *api_, backend_);
    return run_executor(executor, [&](narrative::Executor& exec) {
        return exec.run_from_save(*state);
    });
}

void Engine::register_native(const std::string& name, narrative::BuiltinApi::NativeFn function) {
    api_->register_function(name, std::move(function));
}

} // namespace novel
