#include "engine/narrative/ExpressionEvaluator.hpp"

namespace novel::narrative {

ExpressionEvaluator::ExpressionEvaluator(core::Context& context, BuiltinApi& api)
    : context_(context), api_(api) {}

core::Value ExpressionEvaluator::evaluate(const script::Expr& expr) const {
    using Kind = script::Expr::Kind;

    switch (expr.kind()) {
    case Kind::String:
        return core::Value::from_string(
            static_cast<const script::StringExpr&>(expr).value);

    case Kind::Number:
        return core::Value::from_number(
            static_cast<const script::NumberExpr&>(expr).value);

    case Kind::Bool:
        return core::Value::from_bool(
            static_cast<const script::BoolExpr&>(expr).value);

    case Kind::Variable:
        return context_.get(
            static_cast<const script::VariableExpr&>(expr).name);

    case Kind::Unary: {
        auto& e = static_cast<const script::UnaryExpr&>(expr);
        const core::Value operand = evaluate(*e.operand);
        if (e.op == script::UnaryOp::Not) {
            return core::Value::from_bool(!operand.as_bool());
        }
        return core::Value::from_number(-operand.as_number());
    }

    case Kind::Binary: {
        auto& e = static_cast<const script::BinaryExpr&>(expr);
        if (e.op == script::BinaryOp::And) {
            return core::Value::from_bool(evaluate(*e.left).as_bool() &&
                                          evaluate(*e.right).as_bool());
        }
        if (e.op == script::BinaryOp::Or) {
            return core::Value::from_bool(evaluate(*e.left).as_bool() ||
                                          evaluate(*e.right).as_bool());
        }
        if (e.op == script::BinaryOp::Add) {
            const core::Value left = evaluate(*e.left);
            const core::Value right = evaluate(*e.right);
            if (std::holds_alternative<std::string>(left.data) ||
                std::holds_alternative<std::string>(right.data)) {
                return core::Value::from_string(left.to_string() + right.to_string());
            }
            return core::Value::from_number(left.as_number() + right.as_number());
        }
        if (e.op == script::BinaryOp::Eq) {
            return core::Value::from_bool(evaluate(*e.left) == evaluate(*e.right));
        }
        if (e.op == script::BinaryOp::Ne) {
            return core::Value::from_bool(!(evaluate(*e.left) == evaluate(*e.right)));
        }

        const double left = evaluate(*e.left).as_number();
        const double right = evaluate(*e.right).as_number();
        switch (e.op) {
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
        break;
    }

    case Kind::Call:
        return evaluate_call(static_cast<const script::CallExpr&>(expr));
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
