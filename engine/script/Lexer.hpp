#pragma once

#include "engine/script/Token.hpp"

#include <string>
#include <vector>

namespace novel::script {

/// Tokenizes Ren'Py-inspired script source with indentation-aware blocks.
class Lexer {
public:
    explicit Lexer(std::string source);

    const std::vector<Token>& tokens() const { return tokens_; }

private:
    void tokenize();
    void push_token(TokenKind kind, std::string text = {}, double number = 0.0);
    void push_keyword(const std::string& word);
    bool is_keyword(const std::string& word) const;

    std::string source_;
    std::vector<Token> tokens_;
    std::size_t index_ = 0;
    int line_ = 1;
    int column_ = 1;
    std::vector<int> indent_stack_{0};
};

} // namespace novel::script
