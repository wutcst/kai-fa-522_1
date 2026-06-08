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

// ─── Expressions ─────────────────────────────────────────────────────────────

struct Expr {
    enum class Kind { String, Number, Bool, Variable, Unary, Binary, Call };

    Kind kind() const { return kind_; }
    virtual ~Expr() = default;

protected:
    explicit Expr(Kind k) : kind_(k) {}

private:
    Kind kind_;
};

struct StringExpr : Expr {
    std::string value;
    explicit StringExpr(std::string value)
        : Expr(Kind::String), value(std::move(value)) {}
};

struct NumberExpr : Expr {
    double value;
    explicit NumberExpr(double value)
        : Expr(Kind::Number), value(value) {}
};

struct BoolExpr : Expr {
    bool value;
    explicit BoolExpr(bool value)
        : Expr(Kind::Bool), value(value) {}
};

struct VariableExpr : Expr {
    std::string name;
    explicit VariableExpr(std::string name)
        : Expr(Kind::Variable), name(std::move(name)) {}
};

struct UnaryExpr : Expr {
    UnaryOp op;
    ExprPtr operand;
    UnaryExpr(UnaryOp op, ExprPtr operand)
        : Expr(Kind::Unary), op(op), operand(std::move(operand)) {}
};

struct BinaryExpr : Expr {
    BinaryOp op;
    ExprPtr left;
    ExprPtr right;
    BinaryExpr(BinaryOp op, ExprPtr left, ExprPtr right)
        : Expr(Kind::Binary), op(op), left(std::move(left)), right(std::move(right)) {}
};

struct CallExpr : Expr {
    std::string name;
    std::vector<ExprPtr> args;
    CallExpr(std::string name, std::vector<ExprPtr> args)
        : Expr(Kind::Call), name(std::move(name)), args(std::move(args)) {}
};

// ─── Statements ──────────────────────────────────────────────────────────────

struct Stmt {
    enum class Kind {
        Say, Assign, Jump, Call, Return, Scene, Go,
        Bg, Show, Hide, PlayMusic, StopMusic, StopSound, PlaySound,
        Dialogue, If, Menu,
    };

    Kind kind() const { return kind_; }
    virtual ~Stmt() = default;

protected:
    explicit Stmt(Kind k) : kind_(k) {}

private:
    Kind kind_;
};

struct SayStmt : Stmt {
    ExprPtr text;
    explicit SayStmt(ExprPtr text)
        : Stmt(Kind::Say), text(std::move(text)) {}
};

struct AssignStmt : Stmt {
    std::string name;
    ExprPtr value;
    AssignStmt(std::string name, ExprPtr value)
        : Stmt(Kind::Assign), name(std::move(name)), value(std::move(value)) {}
};

struct JumpStmt : Stmt {
    std::string label;
    explicit JumpStmt(std::string label)
        : Stmt(Kind::Jump), label(std::move(label)) {}
};

struct CallStmt : Stmt {
    std::string label;
    explicit CallStmt(std::string label)
        : Stmt(Kind::Call), label(std::move(label)) {}
};

struct ReturnStmt : Stmt {
    ReturnStmt() : Stmt(Kind::Return) {}
};

struct SceneStmt : Stmt {
    std::string room_id;
    explicit SceneStmt(std::string room_id)
        : Stmt(Kind::Scene), room_id(std::move(room_id)) {}
};

struct GoStmt : Stmt {
    ExprPtr direction;
    explicit GoStmt(ExprPtr direction)
        : Stmt(Kind::Go), direction(std::move(direction)) {}
};

struct BgStmt : Stmt {
    std::string image_path;
    explicit BgStmt(std::string path)
        : Stmt(Kind::Bg), image_path(std::move(path)) {}
};

struct ShowStmt : Stmt {
    std::string tag;
    std::string image_path;
    std::string position;
    ShowStmt(std::string tag, std::string path, std::string pos = "center")
        : Stmt(Kind::Show), tag(std::move(tag)), image_path(std::move(path)),
          position(std::move(pos)) {}
};

struct HideStmt : Stmt {
    std::string tag;
    explicit HideStmt(std::string tag)
        : Stmt(Kind::Hide), tag(std::move(tag)) {}
};

struct PlayMusicStmt : Stmt {
    std::string path;
    double fadein = 0.0;
    double volume = -1.0;
    bool noloop = false;
    PlayMusicStmt(std::string path, double fadein = 0.0, bool noloop = false, double volume = -1.0)
        : Stmt(Kind::PlayMusic), path(std::move(path)), fadein(fadein),
          volume(volume), noloop(noloop) {}
};

struct StopMusicStmt : Stmt {
    double fadeout = 0.0;
    explicit StopMusicStmt(double fadeout = 0.0)
        : Stmt(Kind::StopMusic), fadeout(fadeout) {}
};

struct StopSoundStmt : Stmt {
    StopSoundStmt() : Stmt(Kind::StopSound) {}
};

struct PlaySoundStmt : Stmt {
    std::string path;
    bool loop = false;
    PlaySoundStmt(std::string path, bool loop = false)
        : Stmt(Kind::PlaySound), path(std::move(path)), loop(loop) {}
};

struct DialogueStmt : Stmt {
    std::string speaker;
    ExprPtr text;
    DialogueStmt(std::string speaker, ExprPtr text)
        : Stmt(Kind::Dialogue), speaker(std::move(speaker)), text(std::move(text)) {}
};

struct IfBranch {
    ExprPtr condition;
    StmtList body;
};

struct IfStmt : Stmt {
    std::vector<IfBranch> branches;
    StmtList else_body;
    IfStmt() : Stmt(Kind::If) {}
};

struct MenuChoice {
    std::string caption;
    StmtList body;
};

struct MenuStmt : Stmt {
    std::vector<MenuChoice> choices;
    MenuStmt() : Stmt(Kind::Menu) {}
};

// ─── Module-level definitions ────────────────────────────────────────────────

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
