#pragma once

#include "engine/core/Context.hpp"
#include "engine/core/Value.hpp"
#include "engine/narrative/BuiltinApi.hpp"
#include "engine/script/Ast.hpp"

namespace novel::narrative {

/// Evaluates script expressions against runtime state.
class ExpressionEvaluator {
public:
    ExpressionEvaluator(core::Context& context, BuiltinApi& api);

    core::Value evaluate(const script::Expr& expr) const;
    std::string evaluate_text(const script::Expr& expr) const;

private:
    core::Value evaluate_call(const script::CallExpr& expr) const;

    core::Context& context_;
    BuiltinApi& api_;
};

} // namespace novel::narrative
