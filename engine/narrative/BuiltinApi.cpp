#include "engine/narrative/BuiltinApi.hpp"

#include <sstream>
#include <stdexcept>

namespace novel::narrative {

namespace {

core::Value require_string(const core::Value& value, const char* argument_name) {
    if (!std::holds_alternative<std::string>(value.data)) {
        throw std::runtime_error(std::string(argument_name) + " must be a string");
    }
    return value;
}

} // namespace

BuiltinApi::BuiltinApi(adventure::World& world, adventure::Player& player, core::Context& context)
    : world_(world), player_(player), context_(context) {
    register_function("can_go", [this](const std::vector<core::Value>& args) -> core::Value {
        if (args.size() != 1) {
            throw std::runtime_error("can_go(direction) expects 1 argument");
        }
        const auto direction = require_string(args[0], "direction");
        return core::Value::from_bool(player_.can_go(world_, direction.as_string()));
    });

    register_function("go", [this](const std::vector<core::Value>& args) -> core::Value {
        if (args.size() != 1) {
            throw std::runtime_error("go(direction) expects 1 argument");
        }
        const auto direction = require_string(args[0], "direction");
        return core::Value::from_bool(player_.go(world_, direction.as_string()));
    });

    register_function("scene", [this](const std::vector<core::Value>& args) -> core::Value {
        if (args.size() != 1) {
            throw std::runtime_error("scene(room_id) expects 1 argument");
        }
        const auto room_id = require_string(args[0], "room_id");
        if (!world_.has_room(room_id.as_string())) {
            throw std::runtime_error("unknown room: " + room_id.as_string());
        }
        player_.set_room(room_id.as_string());
        return core::Value::nil();
    });

    register_function("room_description", [this](const std::vector<core::Value>&) -> core::Value {
        return core::Value::from_string(world_.format_description(player_.current_room()));
    });

    register_function("room_exits", [this](const std::vector<core::Value>&) -> core::Value {
        return core::Value::from_string(world_.format_exits(player_.current_room()));
    });

    register_function("current_room", [this](const std::vector<core::Value>&) -> core::Value {
        return core::Value::from_string(player_.current_room());
    });

    register_function("set_flag", [this](const std::vector<core::Value>& args) -> core::Value {
        if (args.size() != 2) {
            throw std::runtime_error("set_flag(name, value) expects 2 arguments");
        }
        const auto name = require_string(args[0], "name");
        context_.set(name.as_string(), args[1]);
        return core::Value::nil();
    });

    register_function("get_flag", [this](const std::vector<core::Value>& args) -> core::Value {
        if (args.size() != 1) {
            throw std::runtime_error("get_flag(name) expects 1 argument");
        }
        const auto name = require_string(args[0], "name");
        return context_.get(name.as_string());
    });
}

core::Value BuiltinApi::call(const std::string& name, const std::vector<core::Value>& args) const {
    const auto it = functions_.find(name);
    if (it == functions_.end()) {
        throw std::runtime_error("unknown function: " + name);
    }
    return it->second(args);
}

bool BuiltinApi::has(const std::string& name) const {
    return functions_.find(name) != functions_.end();
}

void BuiltinApi::register_function(const std::string& name, NativeFn function) {
    functions_[name] = std::move(function);
}

} // namespace novel::narrative
