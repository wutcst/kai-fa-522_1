#include "engine/Engine.hpp"

#include "engine/core/ScriptLoader.hpp"
#include "engine/narrative/Executor.hpp"
#include "engine/narrative/ExpressionEvaluator.hpp"

#include <algorithm>
#include <filesystem>
#include <stdexcept>
#include <vector>

namespace novel {

Engine::Engine(std::unique_ptr<platform::IBackend> backend)
    : backend_(std::move(backend)), player_("outside") {
    api_ = std::make_unique<narrative::BuiltinApi>(world_, player_, context_);
}

void Engine::load_script_file(const std::string& path) {
    apply_module(core::ScriptLoader::load_file(path));
}

void Engine::load_script_directory(const std::string& dir_path) {
    namespace fs = std::filesystem;
    std::vector<std::string> files;
    for (const auto& entry : fs::directory_iterator(dir_path)) {
        if (entry.is_regular_file() && entry.path().extension() == ".rpy") {
            files.push_back(entry.path().string());
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

void Engine::run(const std::string& entry_label) {
    if (!bootstrapped_) {
        bootstrap();
    }

    narrative::Executor executor(module_, *api_, *backend_);
    executor.run(entry_label);
}

void Engine::register_native(const std::string& name, narrative::BuiltinApi::NativeFn function) {
    api_->register_function(name, std::move(function));
}

} // namespace novel
