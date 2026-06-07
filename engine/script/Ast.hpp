#pragma once

#include <memory>
#include <string>
#include <utility>
#include <vector>

namespace novel::script {

enum class BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
    Eq,
    Ne,
    Lt,
    Le,
    Gt,
    Ge,
    And,
    Or,
};

enum class UnaryOp { Not, Neg };

struct Expr;
struct Stmt;

using ExprPtr = std::unique_ptr<Expr>;
using StmtPtr = std::unique_ptr<Stmt>;
using StmtList = std::vector<StmtPtr>;

struct Expr {
    virtual ~Expr() = default;
};

struct StringExpr : Expr {
    std::string value;
    explicit StringExpr(std::string value) : value(std::move(value)) {}
};

struct NumberExpr : Expr {
    double value;
    explicit NumberExpr(double value) : value(value) {}
};

struct BoolExpr : Expr {
    bool value;
    explicit BoolExpr(bool value) : value(value) {}
};

struct VariableExpr : Expr {
    std::string name;
    explicit VariableExpr(std::string name) : name(std::move(name)) {}
};

struct UnaryExpr : Expr {
    UnaryOp op;
    ExprPtr operand;
    UnaryExpr(UnaryOp op, ExprPtr operand) : op(op), operand(std::move(operand)) {}
};

struct BinaryExpr : Expr {
    BinaryOp op;
    ExprPtr left;
    ExprPtr right;
    BinaryExpr(BinaryOp op, ExprPtr left, ExprPtr right)
        : op(op), left(std::move(left)), right(std::move(right)) {}
};

struct CallExpr : Expr {
    std::string name;
    std::vector<ExprPtr> args;
    CallExpr(std::string name, std::vector<ExprPtr> args)
        : name(std::move(name)), args(std::move(args)) {}
};

struct Stmt {
    virtual ~Stmt() = default;
};

struct SayStmt : Stmt {
    ExprPtr text;
    explicit SayStmt(ExprPtr text) : text(std::move(text)) {}
};

struct AssignStmt : Stmt {
    std::string name;
    ExprPtr value;
    AssignStmt(std::string name, ExprPtr value) : name(std::move(name)), value(std::move(value)) {}
};

struct JumpStmt : Stmt {
    std::string label;
    explicit JumpStmt(std::string label) : label(std::move(label)) {}
};

struct CallStmt : Stmt {
    std::string label;
    explicit CallStmt(std::string label) : label(std::move(label)) {}
};

struct ReturnStmt : Stmt {};

struct SceneStmt : Stmt {
    std::string room_id;
    explicit SceneStmt(std::string room_id) : room_id(std::move(room_id)) {}
};

struct GoStmt : Stmt {
    ExprPtr direction;
    explicit GoStmt(ExprPtr direction) : direction(std::move(direction)) {}
};

/// Visual novel: show background image
struct BgStmt : Stmt {
    std::string image_path;
    explicit BgStmt(std::string path) : image_path(std::move(path)) {}
};

/// Visual novel: show character sprite
struct ShowStmt : Stmt {
    std::string tag;
    std::string image_path;
    std::string position; // "left", "center", "right"
    ShowStmt(std::string tag, std::string path, std::string pos = "center")
        : tag(std::move(tag)), image_path(std::move(path)), position(std::move(pos)) {}
};

/// Visual novel: hide character sprite
struct HideStmt : Stmt {
    std::string tag;
    explicit HideStmt(std::string tag) : tag(std::move(tag)) {}
};

/// Visual novel: play music
struct PlayMusicStmt : Stmt {
    std::string path;
    explicit PlayMusicStmt(std::string path) : path(std::move(path)) {}
};

/// Visual novel: stop music
struct StopMusicStmt : Stmt {};

/// Visual novel: play sound effect
struct PlaySoundStmt : Stmt {
    std::string path;
    explicit PlaySoundStmt(std::string path) : path(std::move(path)) {}
};

/// Dialogue with speaker name
struct DialogueStmt : Stmt {
    std::string speaker;
    ExprPtr text;
    DialogueStmt(std::string speaker, ExprPtr text)
        : speaker(std::move(speaker)), text(std::move(text)) {}
};

struct IfBranch {
    ExprPtr condition;
    StmtList body;
};

struct IfStmt : Stmt {
    std::vector<IfBranch> branches;
    StmtList else_body;
};

struct MenuChoice {
    std::string caption;
    StmtList body;
};

struct MenuStmt : Stmt {
    std::vector<MenuChoice> choices;
};

struct Label {
    std::string name;
    StmtList body;
};

struct RoomDef {
    std::string id;
    std::string description;
    std::vector<std::pair<std::string, std::string>> exits;
};

struct DefaultDef {
    std::string name;
    ExprPtr value;
};

struct ScriptModule {
    std::vector<RoomDef> rooms;
    std::vector<DefaultDef> defaults;
    std::vector<Label> labels;
};

} // namespace novel::script
