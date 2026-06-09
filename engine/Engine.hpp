#pragma once

#include "engine/adventure/Player.hpp"
#include "engine/adventure/World.hpp"
#include "engine/core/Context.hpp"
#include "engine/core/PersistentStore.hpp"
#include "engine/core/SaveManager.hpp"
#include "engine/narrative/BuiltinApi.hpp"
#include "engine/platform/IBackend.hpp"
#include "engine/script/Ast.hpp"

#include <filesystem>
#include <functional>
#include <memory>
#include <optional>
#include <string>
#include <vector>

namespace novel::narrative {
class Executor;
}

namespace novel {

/// Top-level engine facade: load scripts, bootstrap world state, run stories.
class Engine {
public:
    Engine(platform::IBackend& backend,
           std::filesystem::path game_root,
           std::filesystem::path content_root,
           core::PersistentStore& persistent);

    void load_script_file(const std::filesystem::path& path);
    void load_script_directory(const std::filesystem::path& dir_path);
    void load_script_source(const std::string& source, const std::string& name = "<script>");
    void bootstrap();
    void prepare_new_game();
    platform::FlowSignal run(const std::string& entry_label = "start");
    platform::FlowSignal run_from_slot(int slot);

    core::Context& context() { return context_; }
    adventure::World& world() { return world_; }
    adventure::Player& player() { return player_; }
    narrative::BuiltinApi& api() { return *api_; }
    core::SaveManager& saves() { return save_manager_; }
    const core::PersistentStore& persistent() const { return persistent_; }

    void register_native(const std::string& name, narrative::BuiltinApi::NativeFn function);
    bool has_save() const { return save_manager_.has_any_save(); }

private:
    void apply_module(script::ScriptModule module);
    void apply_defaults();
    void register_meta_functions();
    platform::FlowSignal run_executor(narrative::Executor& executor,
                                      const std::function<platform::FlowSignal(narrative::Executor&)>& start);
    bool handle_save_request(narrative::Executor& executor);
    void run_save_loaded_hook();
    void mark_game_completed();

    platform::IBackend& backend_;
    core::Context context_;
    adventure::World world_;
    adventure::Player player_{"outside"};
    std::unique_ptr<narrative::BuiltinApi> api_;

    script::ScriptModule module_;
    bool bootstrapped_ = false;

    std::filesystem::path game_root_;
    std::filesystem::path content_root_;
    core::SaveManager save_manager_;
    core::PersistentStore& persistent_;
    std::uint64_t session_start_ms_ = 0;
};

} // namespace novel
