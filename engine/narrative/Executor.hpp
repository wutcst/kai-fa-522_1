#pragma once

#include "engine/narrative/BuiltinApi.hpp"
#include "engine/narrative/ExpressionEvaluator.hpp"
#include "engine/platform/IBackend.hpp"
#include "engine/script/Ast.hpp"

#include <string>
#include <unordered_map>
#include <vector>

namespace novel::narrative {

/// Executes parsed script labels and statements.
class Executor {
public:
    Executor(const script::ScriptModule& module, BuiltinApi& api, platform::IBackend& backend);

    platform::FlowSignal run(const std::string& entry_label);

    BuiltinApi& api() { return api_; }
    const script::ScriptModule& module() const { return module_; }

private:
    struct Frame {
        const script::StmtList* statements = nullptr;
        std::size_t index = 0;
    };

    struct ReturnPoint {
        const script::StmtList* statements = nullptr;
        std::size_t index = 0;
    };

    bool execute_statement(const script::Stmt& stmt, std::vector<Frame>& frames);
    const script::Label* find_label(const std::string& name) const;
    std::string evaluate_text(const script::Expr& expr) const;

    const script::ScriptModule& module_;
    BuiltinApi& api_;
    platform::IBackend& backend_;
    ExpressionEvaluator evaluator_;
    std::vector<ReturnPoint> return_stack_;
    std::unordered_map<std::string, std::size_t> label_index_;
    platform::FlowSignal pending_signal_ = platform::FlowSignal::Continue;
    bool finished_ = false;
};

} // namespace novel::narrative
