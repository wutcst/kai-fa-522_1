#pragma once

#include <string>
#include <variant>
#include <vector>

namespace novel::core {

struct Value;

using ValueList = std::vector<Value>;

/// Dynamic value used by the script runtime (variables, expressions, API returns).
struct Value {
    using Storage = std::variant<std::monostate, bool, double, std::string>;

    Storage data = std::monostate{};

    static Value nil();
    static Value from_bool(bool value);
    static Value from_number(double value);
    static Value from_string(std::string value);

    bool is_nil() const;
    bool as_bool() const;
    double as_number() const;
    const std::string& as_string() const;
    std::string to_string() const;

    bool operator==(const Value& other) const;
};

} // namespace novel::core
