#pragma once

#include "engine/adventure/Player.hpp"
#include "engine/adventure/World.hpp"
#include "engine/core/Context.hpp"
#include "engine/core/Value.hpp"

#include <functional>
#include <string>
#include <unordered_map>

namespace novel::narrative {

/// Script-callable functions exposed by the engine.
class BuiltinApi {
public:
    using NativeFn = std::function<core::Value(const std::vector<core::Value>&)>;

    BuiltinApi(adventure::World& world, adventure::Player& player, core::Context& context);

    core::Value call(const std::string& name, const std::vector<core::Value>& args) const;
    bool has(const std::string& name) const;
    void register_function(const std::string& name, NativeFn function);

    core::Context& context() { return context_; }
    const core::Context& context() const { return context_; }

private:
    adventure::World& world_;
    adventure::Player& player_;
    core::Context& context_;
    std::unordered_map<std::string, NativeFn> functions_;
};

} // namespace novel::narrative
