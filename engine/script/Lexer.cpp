#include "engine/script/Lexer.hpp"

#include <cctype>
#include <stdexcept>
#include <unordered_set>

namespace novel::script {

namespace {

const std::unordered_set<std::string> kKeywords = {
    "room",     "description", "exit",    "default", "label",   "menu",
    "if",       "elif",        "else",    "jump",    "call",    "return",
    "scene",    "go",          "and",     "or",      "not",     "true",
    "false",    "define",      "bg",      "show",    "hide",    "play",
    "stop",     "music",       "sound",   "ambient", "at",      "fadein",
    "fadeout",  "noloop",      "loop",    "volume",  "glitch",  "window",
    "title",    "reset",
};

} // namespace

Lexer::Lexer(std::string source) : source_(std::move(source)) {
    tokenize();
}

void Lexer::push_token(TokenKind kind, std::string text, double number) {
    tokens_.push_back(Token{kind, std::move(text), number, line_, column_});
}

bool Lexer::is_keyword(const std::string& word) const {
    return kKeywords.count(word) > 0;
}

void Lexer::push_keyword(const std::string& word) {
    if (word == "true") {
        push_token(TokenKind::Keyword, "true");
        return;
    }
    if (word == "false") {
        push_token(TokenKind::Keyword, "false");
        return;
    }
    push_token(TokenKind::Keyword, word);
}

void Lexer::tokenize() {
    while (index_ < source_.size()) {
        if (source_[index_] == '\r') {
            ++index_;
            continue;
        }

        if (source_[index_] == '\n') {
            push_token(TokenKind::Newline);
            ++index_;
            ++line_;
            column_ = 1;

            std::size_t indent_start = index_;
            while (index_ < source_.size() && (source_[index_] == ' ' || source_[index_] == '\t')) {
                ++index_;
            }

            if (index_ < source_.size() && source_[index_] == '\n') {
                continue;
            }
            if (index_ >= source_.size()) {
                break;
            }
            if (source_[index_] == '#') {
                while (index_ < source_.size() && source_[index_] != '\n') {
                    ++index_;
                }
                continue;
            }

            const int indent = static_cast<int>(index_ - indent_start);
            const int current = indent_stack_.back();
            if (indent > current) {
                indent_stack_.push_back(indent);
                push_token(TokenKind::Indent);
            } else {
                while (indent < indent_stack_.back()) {
                    indent_stack_.pop_back();
                    push_token(TokenKind::Dedent);
                }
                if (indent != indent_stack_.back()) {
                    throw std::runtime_error("inconsistent indentation at line " + std::to_string(line_));
                }
            }
            continue;
        }

        if (std::isspace(static_cast<unsigned char>(source_[index_]))) {
            ++index_;
            ++column_;
            continue;
        }

        if (source_[index_] == '#') {
            while (index_ < source_.size() && source_[index_] != '\n') {
                ++index_;
            }
            continue;
        }

        if (source_[index_] == '"') {
            ++index_;
            ++column_;
            std::string value;
            while (index_ < source_.size() && source_[index_] != '"') {
                if (source_[index_] == '\\' && index_ + 1 < source_.size()) {
                    ++index_;
                    const char escaped = source_[index_++];
                    if (escaped == 'n') {
                        value.push_back('\n');
                    } else if (escaped == 't') {
                        value.push_back('\t');
                    } else if (escaped == '"') {
                        value.push_back('"');
                    } else if (escaped == '\\') {
                        value.push_back('\\');
                    } else {
                        value.push_back(escaped);
                    }
                    ++column_;
                    continue;
                }
                value.push_back(source_[index_++]);
                ++column_;
            }
            if (index_ >= source_.size()) {
                throw std::runtime_error("unterminated string at line " + std::to_string(line_));
            }
            ++index_;
            ++column_;
            push_token(TokenKind::String, std::move(value));
            continue;
        }

        if (std::isdigit(static_cast<unsigned char>(source_[index_]))) {
            std::size_t start = index_;
            while (index_ < source_.size() &&
                   (std::isdigit(static_cast<unsigned char>(source_[index_])) || source_[index_] == '.')) {
                ++index_;
            }
            const std::string number_text = source_.substr(start, index_ - start);
            column_ += static_cast<int>(index_ - start);
            push_token(TokenKind::Number, number_text, std::stod(number_text));
            continue;
        }

        if (std::isalpha(static_cast<unsigned char>(source_[index_])) || source_[index_] == '_') {
            std::size_t start = index_;
            while (index_ < source_.size() &&
                   (std::isalnum(static_cast<unsigned char>(source_[index_])) || source_[index_] == '_')) {
                ++index_;
            }
            const std::string word = source_.substr(start, index_ - start);
            column_ += static_cast<int>(index_ - start);
            if (is_keyword(word)) {
                push_keyword(word);
            } else {
                push_token(TokenKind::Identifier, word);
            }
            continue;
        }

        const char ch = source_[index_++];
        ++column_;

        switch (ch) {
        case ':':
            push_token(TokenKind::Colon);
            break;
        case '(':
            push_token(TokenKind::LParen);
            break;
        case ')':
            push_token(TokenKind::RParen);
            break;
        case ',':
            push_token(TokenKind::Comma);
            break;
        case '+':
            push_token(TokenKind::Plus);
            break;
        case '-':
            push_token(TokenKind::Minus);
            break;
        case '*':
            push_token(TokenKind::Star);
            break;
        case '/':
            push_token(TokenKind::Slash);
            break;
        case '$':
            push_token(TokenKind::Dollar);
            break;
        case '=':
            if (index_ < source_.size() && source_[index_] == '=') {
                ++index_;
                ++column_;
                push_token(TokenKind::EqEq);
            } else {
                push_token(TokenKind::Equal);
            }
            break;
        case '!':
            if (index_ < source_.size() && source_[index_] == '=') {
                ++index_;
                ++column_;
                push_token(TokenKind::NotEq);
            } else {
                throw std::runtime_error("unexpected '!' at line " + std::to_string(line_));
            }
            break;
        case '<':
            if (index_ < source_.size() && source_[index_] == '=') {
                ++index_;
                ++column_;
                push_token(TokenKind::Le);
            } else {
                push_token(TokenKind::Lt);
            }
            break;
        case '>':
            if (index_ < source_.size() && source_[index_] == '=') {
                ++index_;
                ++column_;
                push_token(TokenKind::Ge);
            } else {
                push_token(TokenKind::Gt);
            }
            break;
        default:
            throw std::runtime_error(std::string("unexpected character '") + ch + "' at line " +
                                     std::to_string(line_));
        }
    }

    while (indent_stack_.size() > 1) {
        indent_stack_.pop_back();
        push_token(TokenKind::Dedent);
    }
    push_token(TokenKind::End);
}

} // namespace novel::script
