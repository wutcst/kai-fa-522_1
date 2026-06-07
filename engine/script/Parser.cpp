#include "engine/script/Parser.hpp"

#include "engine/script/Lexer.hpp"

#include <sstream>
#include <stdexcept>

namespace novel::script {

Parser::Parser(std::vector<Token> tokens) : tokens_(std::move(tokens)) {}

const Token& Parser::peek(std::size_t offset) const {
    const std::size_t index = current_ + offset;
    if (index >= tokens_.size()) {
        return tokens_.back();
    }
    return tokens_[index];
}

const Token& Parser::advance() {
  if (current_ < tokens_.size()) {
    return tokens_[current_++];
  }
  return tokens_.back();
}

bool Parser::match(TokenKind kind) {
    if (check(kind)) {
        advance();
        return true;
    }
    return false;
}

bool Parser::check(TokenKind kind) const { return peek().kind == kind; }

bool Parser::check_keyword(const std::string& word) const {
    return peek().kind == TokenKind::Keyword && peek().text == word;
}

bool Parser::match_keyword(const std::string& word) {
    if (check_keyword(word)) {
        advance();
        return true;
    }
    return false;
}

void Parser::expect(TokenKind kind, const std::string& message) {
    if (!match(kind)) {
        throw std::runtime_error(message + " at line " + std::to_string(peek().line));
    }
}

void Parser::expect_keyword(const std::string& word) {
    if (!match_keyword(word)) {
        throw std::runtime_error("expected keyword '" + word + "' at line " + std::to_string(peek().line));
    }
}

void Parser::skip_newlines() {
    while (match(TokenKind::Newline)) {
    }
}

bool Parser::at_block_start() const {
    return check(TokenKind::Indent);
}

ScriptModule Parser::parse() {
    ScriptModule module;
    skip_newlines();

    while (!check(TokenKind::End)) {
        if (check_keyword("room")) {
            module.rooms.push_back(parse_room_def());
        } else if (check_keyword("default") || check_keyword("define")) {
            module.defaults.push_back(parse_default_def());
        } else if (check_keyword("label")) {
            module.labels.push_back(parse_label_def());
        } else if (check(TokenKind::End)) {
            break;
        } else {
            throw std::runtime_error("unexpected token at line " + std::to_string(peek().line));
        }
        skip_newlines();
    }

    return module;
}

RoomDef Parser::parse_room_def() {
    expect_keyword("room");
    RoomDef room;
    room.id = advance().text;
    expect(TokenKind::Colon, "expected ':' after room name");
    skip_newlines();
    expect(TokenKind::Indent, "expected indented room body");

    while (!check(TokenKind::Dedent) && !check(TokenKind::End)) {
        skip_newlines();
        if (check(TokenKind::Dedent)) {
            break;
        }
        if (match_keyword("description")) {
            if (!check(TokenKind::String)) {
                throw std::runtime_error("expected room description string");
            }
            room.description = advance().text;
        } else if (match_keyword("exit")) {
            const std::string direction = advance().text;
            const std::string target = advance().text;
            room.exits.emplace_back(direction, target);
        } else {
            throw std::runtime_error("unknown room statement at line " + std::to_string(peek().line));
        }
        skip_newlines();
    }

    expect(TokenKind::Dedent, "expected end of room block");
    return room;
}

DefaultDef Parser::parse_default_def() {
    if (match_keyword("default")) {
        DefaultDef def;
        def.name = advance().text;
        expect(TokenKind::Equal, "expected '=' in default declaration");
        def.value = parse_expression();
        return def;
    }

    expect_keyword("define");
    DefaultDef def;
    def.name = advance().text;
    expect(TokenKind::Equal, "expected '=' in define declaration");
    def.value = parse_expression();
    return def;
}

Label Parser::parse_label_def() {
    expect_keyword("label");
    Label label;
    label.name = advance().text;
    expect(TokenKind::Colon, "expected ':' after label name");
    label.body = parse_block();
    return label;
}

StmtList Parser::parse_block() {
    skip_newlines();
    expect(TokenKind::Indent, "expected indented block");

    StmtList statements;
    while (!check(TokenKind::Dedent) && !check(TokenKind::End)) {
        skip_newlines();
        if (check(TokenKind::Dedent)) {
            break;
        }
        statements.push_back(parse_statement());
        skip_newlines();
    }

    expect(TokenKind::Dedent, "expected end of block");
    return statements;
}

StmtPtr Parser::parse_statement() {
    if (check(TokenKind::String)) {
        const std::string raw = advance().text;
        return std::make_unique<SayStmt>(parse_string_with_interpolation(raw));
    }

    if (check(TokenKind::Dollar)) {
        advance();
        const std::string name = advance().text;
        expect(TokenKind::Equal, "expected '=' in assignment");
        return std::make_unique<AssignStmt>(name, parse_expression());
    }

    if (check_keyword("if")) {
        return parse_if_statement();
    }

    if (check_keyword("menu")) {
        return parse_menu_statement();
    }

    if (match_keyword("jump")) {
        return std::make_unique<JumpStmt>(advance().text);
    }

    if (match_keyword("call")) {
        return std::make_unique<CallStmt>(advance().text);
    }

    if (match_keyword("return")) {
        return std::make_unique<ReturnStmt>();
    }

    if (match_keyword("scene")) {
        return std::make_unique<SceneStmt>(advance().text);
    }

    if (match_keyword("go")) {
        if (check(TokenKind::String)) {
            return std::make_unique<GoStmt>(parse_primary());
        }
        if (check(TokenKind::Identifier)) {
            return std::make_unique<GoStmt>(std::make_unique<StringExpr>(advance().text));
        }
        throw std::runtime_error("expected direction after go at line " + std::to_string(peek().line));
    }

    if (match_keyword("bg")) {
        const std::string path = advance().text;
        return std::make_unique<BgStmt>(path);
    }

    if (match_keyword("show")) {
        const std::string tag = advance().text;
        std::string image_path = tag;
        std::string position = "center";

        if (check(TokenKind::String) || check(TokenKind::Identifier)) {
            image_path = advance().text;
        }
        if (match_keyword("at")) {
            position = advance().text;
        }

        return std::make_unique<ShowStmt>(tag, image_path, position);
    }

    if (match_keyword("hide")) {
        const std::string tag = advance().text;
        return std::make_unique<HideStmt>(tag);
    }

    if (match_keyword("play")) {
        if (match_keyword("music")) {
            const std::string path = advance().text;
            return std::make_unique<PlayMusicStmt>(path);
        }
        if (match_keyword("sound")) {
            const std::string path = advance().text;
            return std::make_unique<PlaySoundStmt>(path);
        }
        throw std::runtime_error("expected 'music' or 'sound' after play at line " + std::to_string(peek().line));
    }

    if (match_keyword("stop")) {
        if (match_keyword("music")) {
            return std::make_unique<StopMusicStmt>();
        }
        throw std::runtime_error("expected 'music' after stop at line " + std::to_string(peek().line));
    }

    // Dialogue: identifier followed by a string → "speaker" "text"
    if (check(TokenKind::Identifier) && peek(1).kind == TokenKind::String) {
        const std::string speaker = advance().text;
        const std::string raw = advance().text;
        return std::make_unique<DialogueStmt>(speaker, parse_string_with_interpolation(raw));
    }

    throw std::runtime_error("unexpected statement at line " + std::to_string(peek().line));
}

StmtPtr Parser::parse_if_statement() {
    auto stmt = std::make_unique<IfStmt>();
    expect_keyword("if");
    IfBranch branch;
    branch.condition = parse_expression();
    expect(TokenKind::Colon, "expected ':' after if condition");
    branch.body = parse_block();
    stmt->branches.push_back(std::move(branch));

    skip_newlines();
    while (match_keyword("elif")) {
        IfBranch elif_branch;
        elif_branch.condition = parse_expression();
        expect(TokenKind::Colon, "expected ':' after elif condition");
        elif_branch.body = parse_block();
        stmt->branches.push_back(std::move(elif_branch));
        skip_newlines();
    }

    if (match_keyword("else")) {
        expect(TokenKind::Colon, "expected ':' after else");
        stmt->else_body = parse_block();
    }

    return stmt;
}

StmtPtr Parser::parse_menu_statement() {
    auto stmt = std::make_unique<MenuStmt>();
    expect_keyword("menu");
    expect(TokenKind::Colon, "expected ':' after menu");
    skip_newlines();
    expect(TokenKind::Indent, "expected indented menu block");

    while (!check(TokenKind::Dedent) && !check(TokenKind::End)) {
        skip_newlines();
        if (check(TokenKind::Dedent)) {
            break;
        }

        MenuChoice choice;
        if (!check(TokenKind::String)) {
            throw std::runtime_error("expected menu choice caption");
        }
        choice.caption = advance().text;
        expect(TokenKind::Colon, "expected ':' after menu choice");
        choice.body = parse_block();
        stmt->choices.push_back(std::move(choice));
        skip_newlines();
    }

    expect(TokenKind::Dedent, "expected end of menu block");
    return stmt;
}

ExprPtr Parser::parse_expression() { return parse_or(); }

ExprPtr Parser::parse_or() {
    auto left = parse_and();
    while (match_keyword("or")) {
        auto right = parse_and();
        left = std::make_unique<BinaryExpr>(BinaryOp::Or, std::move(left), std::move(right));
    }
    return left;
}

ExprPtr Parser::parse_and() {
    auto left = parse_equality();
    while (match_keyword("and")) {
        auto right = parse_equality();
        left = std::make_unique<BinaryExpr>(BinaryOp::And, std::move(left), std::move(right));
    }
    return left;
}

ExprPtr Parser::parse_equality() {
    auto left = parse_comparison();
    while (true) {
        if (match(TokenKind::EqEq)) {
            auto right = parse_comparison();
            left = std::make_unique<BinaryExpr>(BinaryOp::Eq, std::move(left), std::move(right));
        } else if (match(TokenKind::NotEq)) {
            auto right = parse_comparison();
            left = std::make_unique<BinaryExpr>(BinaryOp::Ne, std::move(left), std::move(right));
        } else {
            break;
        }
    }
    return left;
}

ExprPtr Parser::parse_comparison() {
    auto left = parse_term();
    while (true) {
        if (match(TokenKind::Lt)) {
            auto right = parse_term();
            left = std::make_unique<BinaryExpr>(BinaryOp::Lt, std::move(left), std::move(right));
        } else if (match(TokenKind::Le)) {
            auto right = parse_term();
            left = std::make_unique<BinaryExpr>(BinaryOp::Le, std::move(left), std::move(right));
        } else if (match(TokenKind::Gt)) {
            auto right = parse_term();
            left = std::make_unique<BinaryExpr>(BinaryOp::Gt, std::move(left), std::move(right));
        } else if (match(TokenKind::Ge)) {
            auto right = parse_term();
            left = std::make_unique<BinaryExpr>(BinaryOp::Ge, std::move(left), std::move(right));
        } else {
            break;
        }
    }
    return left;
}

ExprPtr Parser::parse_term() {
    auto left = parse_factor();
    while (true) {
        if (match(TokenKind::Plus)) {
            auto right = parse_factor();
            left = std::make_unique<BinaryExpr>(BinaryOp::Add, std::move(left), std::move(right));
        } else if (match(TokenKind::Minus)) {
            auto right = parse_factor();
            left = std::make_unique<BinaryExpr>(BinaryOp::Sub, std::move(left), std::move(right));
        } else {
            break;
        }
    }
    return left;
}

ExprPtr Parser::parse_factor() {
    auto left = parse_unary();
    while (true) {
        if (match(TokenKind::Star)) {
            auto right = parse_unary();
            left = std::make_unique<BinaryExpr>(BinaryOp::Mul, std::move(left), std::move(right));
        } else if (match(TokenKind::Slash)) {
            auto right = parse_unary();
            left = std::make_unique<BinaryExpr>(BinaryOp::Div, std::move(left), std::move(right));
        } else {
            break;
        }
    }
    return left;
}

ExprPtr Parser::parse_unary() {
    if (match_keyword("not")) {
        return std::make_unique<UnaryExpr>(UnaryOp::Not, parse_unary());
    }
    if (match(TokenKind::Minus)) {
        return std::make_unique<UnaryExpr>(UnaryOp::Neg, parse_unary());
    }
    return parse_primary();
}

ExprPtr Parser::parse_primary() {
    if (check(TokenKind::String)) {
        return parse_string_with_interpolation(advance().text);
    }
    if (check(TokenKind::Number)) {
        return std::make_unique<NumberExpr>(advance().number);
    }
    if (check_keyword("true")) {
        advance();
        return std::make_unique<BoolExpr>(true);
    }
    if (check_keyword("false")) {
        advance();
        return std::make_unique<BoolExpr>(false);
    }
    if (check(TokenKind::Identifier)) {
        const std::string name = advance().text;
        if (match(TokenKind::LParen)) {
            std::vector<ExprPtr> args;
            if (!check(TokenKind::RParen)) {
                do {
                    args.push_back(parse_expression());
                } while (match(TokenKind::Comma));
            }
            expect(TokenKind::RParen, "expected ')' after call arguments");
            return std::make_unique<CallExpr>(name, std::move(args));
        }
        return std::make_unique<VariableExpr>(name);
    }
    if (match(TokenKind::LParen)) {
        auto expr = parse_expression();
        expect(TokenKind::RParen, "expected ')' after expression");
        return expr;
    }

    throw std::runtime_error("expected expression at line " + std::to_string(peek().line));
}

ExprPtr Parser::parse_string_with_interpolation(const std::string& raw) {
    std::string current;
    std::vector<ExprPtr> parts;
    auto append_part = [&](const std::string& part) {
        if (!part.empty()) {
            parts.push_back(std::make_unique<StringExpr>(part));
        }
    };
    for (std::size_t i = 0; i < raw.size(); ++i) {
        if (raw[i] == '[') {
            append_part(current);
            current.clear();

            const std::size_t end = raw.find(']', i + 1);
            if (end == std::string::npos) {
                throw std::runtime_error("unterminated interpolation");
            }

            const std::string expr_text = raw.substr(i + 1, end - i - 1);
            Parser sub_parser(Lexer(expr_text).tokens());
            parts.push_back(sub_parser.parse_expression());
            i = end;
            continue;
        }
        current.push_back(raw[i]);
    }
    append_part(current);

    if (parts.empty()) {
        return std::make_unique<StringExpr>("");
    }
    if (parts.size() == 1) {
        return std::move(parts.front());
    }

    ExprPtr result = std::move(parts.front());
    for (std::size_t i = 1; i < parts.size(); ++i) {
        result = std::make_unique<BinaryExpr>(BinaryOp::Add, std::move(result), std::move(parts[i]));
    }
    return result;
}

} // namespace novel::script
