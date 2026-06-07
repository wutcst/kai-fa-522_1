#pragma once

#include "engine/script/Ast.hpp"
#include "engine/script/Token.hpp"

#include <string>
#include <vector>

namespace novel::script {

/// Parses tokens into a script module (rooms, defaults, labels).
class Parser {
public:
    explicit Parser(std::vector<Token> tokens);

    ScriptModule parse();

private:
    const Token& peek(std::size_t offset = 0) const;
    const Token& advance();
    bool match(TokenKind kind);
    bool check(TokenKind kind) const;
    bool check_keyword(const std::string& word) const;
    bool match_keyword(const std::string& word);
    void expect(TokenKind kind, const std::string& message);
    void expect_keyword(const std::string& word);
    void skip_newlines();

    bool at_block_start() const;
    StmtList parse_block();
    StmtPtr parse_statement();
    StmtPtr parse_if_statement();
    StmtPtr parse_menu_statement();

    ExprPtr parse_expression();
    ExprPtr parse_or();
    ExprPtr parse_and();
    ExprPtr parse_equality();
    ExprPtr parse_comparison();
    ExprPtr parse_term();
    ExprPtr parse_factor();
    ExprPtr parse_unary();
    ExprPtr parse_primary();
    ExprPtr parse_string_with_interpolation(const std::string& raw);

    RoomDef parse_room_def();
    DefaultDef parse_default_def();
    Label parse_label_def();

    std::vector<Token> tokens_;
    std::size_t current_ = 0;
};

} // namespace novel::script
