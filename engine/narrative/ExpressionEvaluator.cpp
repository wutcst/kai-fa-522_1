#include "engine/narrative/ExpressionEvaluator.hpp"

namespace novel::narrative {

ExpressionEvaluator::ExpressionEvaluator(core::Context& context, BuiltinApi& api)
    : context_(context), api_(api) {}

core::Value ExpressionEvaluator::evaluate(const script::Expr& expr) const {
    if (const auto* value = dynamic_cast<const script::StringExpr*>(&expr)) {
        return core::Value::from_string(value->value);
    }
    if (const auto* value = dynamic_cast<const script::NumberExpr*>(&expr)) {
        return core::Value::from_number(value->value);
    }
    if (const auto* value = dynamic_cast<const script::BoolExpr*>(&expr)) {
        return core::Value::from_bool(value->value);
    }
    if (const auto* value = dynamic_cast<const script::VariableExpr*>(&expr)) {
        return context_.get(value->name);
    }
    if (const auto* value = dynamic_cast<const script::UnaryExpr*>(&expr)) {
        const core::Value operand = evaluate(*value->operand);
        if (value->op == script::UnaryOp::Not) {
            return core::Value::from_bool(!operand.as_bool());
        }
        return core::Value::from_number(-operand.as_number());
    }
    if (const auto* value = dynamic_cast<const script::BinaryExpr*>(&expr)) {
        if (value->op == script::BinaryOp::And) {
            return core::Value::from_bool(evaluate(*value->left).as_bool() &&
                                          evaluate(*value->right).as_bool());
        }
        if (value->op == script::BinaryOp::Or) {
            return core::Value::from_bool(evaluate(*value->left).as_bool() ||
                                          evaluate(*value->right).as_bool());
        }
        if (value->op == script::BinaryOp::Add) {
            const core::Value left = evaluate(*value->left);
            const core::Value right = evaluate(*value->right);
            if (std::holds_alternative<std::string>(left.data) ||
                std::holds_alternative<std::string>(right.data)) {
                return core::Value::from_string(left.to_string() + right.to_string());
            }
            return core::Value::from_number(left.as_number() + right.as_number());
        }
        if (value->op == script::BinaryOp::Eq) {
            return core::Value::from_bool(evaluate(*value->left) == evaluate(*value->right));
        }
        if (value->op == script::BinaryOp::Ne) {
            return core::Value::from_bool(!(evaluate(*value->left) == evaluate(*value->right)));
        }

        const double left = evaluate(*value->left).as_number();
        const double right = evaluate(*value->right).as_number();
        switch (value->op) {
        case script::BinaryOp::Sub:
            return core::Value::from_number(left - right);
        case script::BinaryOp::Mul:
            return core::Value::from_number(left * right);
        case script::BinaryOp::Div:
            return core::Value::from_number(left / right);
        case script::BinaryOp::Lt:
            return core::Value::from_bool(left < right);
        case script::BinaryOp::Le:
            return core::Value::from_bool(left <= right);
        case script::BinaryOp::Gt:
            return core::Value::from_bool(left > right);
        case script::BinaryOp::Ge:
            return core::Value::from_bool(left >= right);
        default:
            break;
        }
    }
    if (const auto* value = dynamic_cast<const script::CallExpr*>(&expr)) {
        return evaluate_call(*value);
    }

    return core::Value::nil();
}

core::Value ExpressionEvaluator::evaluate_call(const script::CallExpr& expr) const {
    std::vector<core::Value> args;
    args.reserve(expr.args.size());
    for (const auto& arg : expr.args) {
        args.push_back(evaluate(*arg));
    }
    return api_.call(expr.name, args);
}

std::string ExpressionEvaluator::evaluate_text(const script::Expr& expr) const {
    return evaluate(expr).to_string();
}

} // namespace novel::narrative
