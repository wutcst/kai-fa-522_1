#include "engine/core/Value.hpp"

#include <cmath>
#include <sstream>
#include <stdexcept>

namespace novel::core {

Value Value::nil() { return Value{}; }

Value Value::from_bool(bool value) {
    Value result;
    result.data = value;
    return result;
}

Value Value::from_number(double value) {
    Value result;
    result.data = value;
    return result;
}

Value Value::from_string(std::string value) {
    Value result;
    result.data = std::move(value);
    return result;
}

bool Value::is_nil() const { return std::holds_alternative<std::monostate>(data); }

bool Value::as_bool() const {
    if (std::holds_alternative<bool>(data)) {
        return std::get<bool>(data);
    }
    if (std::holds_alternative<double>(data)) {
        return std::get<double>(data) != 0.0;
    }
    if (std::holds_alternative<std::string>(data)) {
        return !std::get<std::string>(data).empty();
    }
    return false;
}

double Value::as_number() const {
    if (std::holds_alternative<double>(data)) {
        return std::get<double>(data);
    }
    if (std::holds_alternative<bool>(data)) {
        return std::get<bool>(data) ? 1.0 : 0.0;
    }
    if (std::holds_alternative<std::string>(data)) {
        return std::stod(std::get<std::string>(data));
    }
    return 0.0;
}

const std::string& Value::as_string() const {
    if (std::holds_alternative<std::string>(data)) {
        return std::get<std::string>(data);
    }
    throw std::runtime_error("value is not a string");
}

std::string Value::to_string() const {
    if (std::holds_alternative<std::monostate>(data)) {
        return "null";
    }
    if (std::holds_alternative<bool>(data)) {
        return std::get<bool>(data) ? "true" : "false";
    }
    if (std::holds_alternative<double>(data)) {
        const double number = std::get<double>(data);
        if (std::floor(number) == number) {
            return std::to_string(static_cast<long long>(number));
        }
        std::ostringstream stream;
        stream << number;
        return stream.str();
    }
    return std::get<std::string>(data);
}

bool Value::operator==(const Value& other) const {
    if (is_nil() && other.is_nil()) {
        return true;
    }
    if (std::holds_alternative<bool>(data) && std::holds_alternative<bool>(other.data)) {
        return std::get<bool>(data) == std::get<bool>(other.data);
    }
    if (std::holds_alternative<double>(data) && std::holds_alternative<double>(other.data)) {
        return std::get<double>(data) == std::get<double>(other.data);
    }
    if (std::holds_alternative<std::string>(data) && std::holds_alternative<std::string>(other.data)) {
        return std::get<std::string>(data) == std::get<std::string>(other.data);
    }
    return false;
}

} // namespace novel::core
