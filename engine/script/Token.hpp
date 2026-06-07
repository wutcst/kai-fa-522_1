#pragma once

#include <string>

namespace novel::script {

enum class TokenKind {
    End,
    Newline,
    Indent,
    Dedent,
    Identifier,
    String,
    Number,
    Colon,
    LParen,
    RParen,
    Comma,
    Equal,
    Dollar,
    Plus,
    Minus,
    Star,
    Slash,
    EqEq,
    NotEq,
    Lt,
    Gt,
    Le,
    Ge,
    Keyword,
};

struct Token {
    TokenKind kind = TokenKind::End;
    std::string text;
    double number = 0.0;
    int line = 1;
    int column = 1;
};

} // namespace novel::script
