#include "engine/core/Context.hpp"

namespace novel::core {

void Context::set(const std::string& name, Value value) {
    variables_[name] = std::move(value);
}

Value Context::get(const std::string& name) const {
    const auto it = variables_.find(name);
    if (it == variables_.end()) {
        return Value::nil();
    }
    return it->second;
}

bool Context::has(const std::string& name) const {
    return variables_.find(name) != variables_.end();
}

} // namespace novel::core
