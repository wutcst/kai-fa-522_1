#pragma once

#include "engine/core/Value.hpp"

#include <optional>
#include <string>
#include <unordered_map>

namespace novel::core {

/// Mutable script state: variables, flags, and persistent game data.
class Context {
public:
    void set(const std::string& name, Value value);
    Value get(const std::string& name) const;
    bool has(const std::string& name) const;

    const std::unordered_map<std::string, Value>& variables() const { return variables_; }

private:
    std::unordered_map<std::string, Value> variables_;
};

} // namespace novel::core
