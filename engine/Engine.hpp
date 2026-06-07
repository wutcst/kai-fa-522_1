#pragma once

#include "engine/adventure/Player.hpp"
#include "engine/adventure/World.hpp"
#include "engine/core/Context.hpp"
#include "engine/narrative/BuiltinApi.hpp"
#include "engine/platform/IBackend.hpp"
#include "engine/script/Ast.hpp"

#include <memory>
#include <string>
#include <vector>

namespace novel {

/// Top-level engine facade: load scripts, bootstrap world state, run stories.
class Engine {
public:
    explicit Engine(std::unique_ptr<platform::IBackend> backend);

    void load_script_file(const std::string& path);
    void load_script_source(const std::string& source, const std::string& name = "<script>");
    void bootstrap();
    void run(const std::string& entry_label = "start");

    core::Context& context() { return context_; }
    adventure::World& world() { return world_; }
    adventure::Player& player() { return player_; }
    narrative::BuiltinApi& api() { return *api_; }

    void register_native(const std::string& name, narrative::BuiltinApi::NativeFn function);

private:
    void apply_module(script::ScriptModule module);
    void apply_defaults();

    std::unique_ptr<platform::IBackend> backend_;
    core::Context context_;
    adventure::World world_;
    adventure::Player player_{"outside"};
    std::unique_ptr<narrative::BuiltinApi> api_;

    script::ScriptModule module_;
    bool bootstrapped_ = false;
};

} // namespace novel
