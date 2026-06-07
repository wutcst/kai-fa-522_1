# RPY 脚本语法指南

本文档描述 **novel 引擎** 所支持的 `.rpy` 脚本语法。语法设计参考 [Ren'Py](https://www.renpy.org/)，在保留核心叙事结构的同时，针对文字冒险游戏做了精简与扩展。

脚本按职责拆分为多个文件，由游戏入口依次加载，例如：

```
content/scripts/world.rpy   # 世界与房间定义
content/scripts/story.rpy   # 剧情与交互流程
```

---

## 1. 基础规则

### 1.1 注释

以 `#` 开头，直到行尾均为注释：

```rpy
# 这是注释
label start:  # 行尾注释
```

### 1.2 缩进

使用 **空格缩进**（与 Ren'Py 相同），缩进决定代码块归属。同一代码块内的语句必须保持相同缩进层级，子块比父块多缩进一级（通常 4 个空格）。

```rpy
label example:
    "外层语句"
    if true:
        "内层语句"
```

缩进不一致将导致解析错误。

### 1.3 行结构

- 块起始行以 `:` 结尾（如 `label start:`、`menu:`、`if ...:`）
- 块体写在下一行，并增加一级缩进
- 单行语句不需要 `:`（如 `jump end`、`go east`）

---

## 2. 世界定义

在脚本顶层声明房间与初始变量，供引擎在 `bootstrap()` 阶段加载。

### 2.1 房间 `room`

```rpy
room <房间ID>:
    description "<房间描述文本>"
    exit <方向> <目标房间ID>
    exit <方向> <目标房间ID>
```

| 字段 | 说明 |
|------|------|
| `房间ID` | 唯一标识符，供 `scene`、出口引用 |
| `description` | 房间的描述文字（不含 "You are" 前缀，引擎会自动拼接） |
| `exit` | 定义从一个房间到另一个房间的出口 |

示例：

```rpy
room outside:
    description "outside the main entrance of the university"
    exit east theater
    exit south lab
    exit west pub

room theater:
    description "in a lecture theater"
    exit west outside
```

### 2.2 默认变量 `default` / `define`

在顶层声明变量初始值，游戏启动时写入运行时上下文：

```rpy
default start_room = "outside"
default visited_theater = false
default score = 0

define player_name = "Alice"   # 与 default 等价
```

支持的初始值类型：字符串、数字、布尔值（`true` / `false`），以及由这些组成的表达式。

特殊变量 `start_room`：若已定义，引擎将玩家初始位置设为该房间 ID。

---

## 3. 剧情标签与控制流

### 3.1 标签 `label`

定义一段可跳转执行的语句块：

```rpy
label start:
    "游戏从这里开始"
    jump game_loop
```

标签名由字母、数字、下划线组成。游戏默认从 `start` 标签开始执行。

### 3.2 跳转 `jump`

无条件跳转到指定标签，**清空调用栈**（不返回）：

```rpy
jump game_loop
jump end_game
```

### 3.3 调用 `call` / 返回 `return`

`call` 跳转到子标签，执行完毕后通过 `return` 回到调用处继续：

```rpy
label game_loop:
    call show_room
    "调用 show_room 返回后继续执行"
    jump game_loop

label show_room:
    "[room_description()]"
    return
```

- `return` 在有 `call` 时回到调用点
- 在最外层标签执行 `return` 将结束游戏

---

## 4. 叙事语句

### 4.1 对白 / 旁白

字符串字面量单独占一行时，作为叙事文本显示给玩家：

```rpy
"Welcome to the World of Zuul!"
"这里可以写多行文本，\\n 换行符需转义。"
```

### 4.2 字符串插值

字符串内用 `[表达式]` 嵌入动态内容：

```rpy
"[room_description()]"
"Exits: [room_exits()]"
"当前房间：[current_room()]"
"分数：[score]"
```

---

## 5. 场景与移动

### 5.1 切换场景 `scene`

将玩家传送到指定房间（不经过出口检查）：

```rpy
scene outside
scene theater
```

等价于调用内置函数 `scene("房间ID")`。

### 5.2 方向移动 `go`

沿出口方向移动玩家：

```rpy
go east
go south
go west
go north
```

方向可为标识符（如 `east`）或字符串（`go "east"`）。移动是否成功取决于当前房间是否定义了对应出口。

---

## 6. 菜单 `menu`

向玩家展示选项列表，根据选择执行对应分支：

```rpy
menu:
    "选项一显示文字":
        "你选择了第一项"
        jump somewhere
    "选项二显示文字":
        jump other_place
    "退出":
        jump end_game
```

- 每个选项由 **显示文字** + `:` + **缩进语句块** 组成
- 控制台后端以数字序号展示选项，玩家输入对应数字选择

---

## 7. 条件分支 `if`

```rpy
if <条件>:
    "条件成立时执行"
elif <条件>:
    "否则若成立"
else:
    "以上均不成立"
```

示例：

```rpy
if can_go("east"):
    go east
    jump game_loop
else:
    "There is no door!"
    jump travel_menu

if current_room() == "theater" and not visited_theater:
    $ visited_theater = true
    "第一次进入讲堂。"
```

---

## 8. 变量与赋值

### 8.1 运行时赋值 `$`

在标签体内修改变量：

```rpy
$ visited_theater = true
$ score = score + 10
$ player_name = "Bob"
```

### 8.2 读取变量

在表达式中直接使用变量名：

```rpy
if not visited_lab:
    $ visited_lab = true

if score >= 100:
    "你赢了！"
```

未定义的变量读取结果为 `null`，在布尔上下文中视为 `false`。

---

## 9. 表达式

### 9.1 字面量

| 类型 | 示例 |
|------|------|
| 字符串 | `"hello"` |
| 数字 | `0`、`3.14` |
| 布尔 | `true`、`false` |

### 9.2 运算符

| 类别 | 运算符 |
|------|--------|
| 算术 | `+` `-` `*` `/` |
| 比较 | `==` `!=` `<` `<=` `>` `>=` |
| 逻辑 | `and` `or` `not` |

运算符优先级（从高到低）：`not` → 算术 → 比较 → `and` → `or`。可用 `()` 改变优先级。

字符串的 `+` 为拼接：

```rpy
$ greeting = "Hello, " + player_name
```

### 9.3 函数调用

```rpy
can_go("east")
current_room() == "lab"
not visited_theater
```

---

## 10. 内置 API

引擎向脚本暴露以下函数，可在表达式或条件中调用：

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `can_go(direction)` | 方向字符串 | `bool` | 当前房间是否存在该出口 |
| `go(direction)` | 方向字符串 | `bool` | 沿方向移动，成功返回 `true` |
| `scene(room_id)` | 房间 ID | — | 将玩家置于指定房间 |
| `room_description()` | — | `string` | 当前房间的完整描述 |
| `room_exits()` | — | `string` | 当前房间出口列表（空格分隔） |
| `current_room()` | — | `string` | 玩家当前所在房间 ID |
| `set_flag(name, value)` | 名称、值 | — | 设置标志/变量 |
| `get_flag(name)` | 名称 | 任意 | 读取标志/变量 |

C++ 侧可通过 `Engine::register_native()` 注册更多原生函数。

---

## 11. 完整示例

### world.rpy

```rpy
room outside:
    description "outside the main entrance of the university"
    exit east theater
    exit south lab

room theater:
    description "in a lecture theater"
    exit west outside

default start_room = "outside"
default visited_theater = false
```

### story.rpy

```rpy
label start:
    scene outside
    "Welcome to the World of Zuul!"
    jump game_loop

label game_loop:
    call show_room
    menu:
        "Look around":
            jump game_loop
        "Travel":
            jump travel_menu
        "Quit":
            jump end_game

label travel_menu:
    menu:
        "East":
            if can_go("east"):
                go east
                call on_enter_room
                jump game_loop
            else:
                "There is no door!"
                jump travel_menu
        "Back":
            jump game_loop

label show_room:
    "[room_description()]"
    "Exits: [room_exits()]"
    return

label on_enter_room:
    if current_room() == "theater" and not visited_theater:
        $ visited_theater = true
        "This is your first time in the lecture theater."
    return

label end_game:
    "Thank you for playing.  Good bye."
    return
```

---

## 12. 与 Ren'Py 的差异

本引擎语法是 Ren'Py 的 **子集 + 文字冒险扩展**，以下 Ren'Py 特性 **尚未支持**：

| 特性 | 状态 |
|------|------|
| Python 语句块 | 不支持 |
| `character` 角色定义 | 不支持 |
| `show` / `hide` 立绘 | 不支持（预留图形后端扩展） |
| `image` / `transform` | 不支持 |
| `pause` / `with` 转场 | 不支持 |
| 多文件 `init` 优先级 | 不支持（按加载顺序合并） |

已支持的 Ren'Py 核心结构：`label`、`jump`、`call`/`return`、`menu`、`if`/`elif`/`else`、字符串叙事、`$` 赋值、`default`/`define`、`scene`。

---

## 13. 关键字一览

```
room  description  exit  default  define
label  menu  if  elif  else
jump  call  return
scene  go
and  or  not  true  false
```

---

## 14. 常见错误

| 错误信息 | 原因 |
|----------|------|
| `inconsistent indentation` | 同一块内缩进层级不一致 |
| `unknown label: xxx` | `jump` / `call` 目标标签不存在 |
| `duplicate room id` | 两个 `room` 使用了相同 ID |
| `duplicate label` | 两个 `label` 使用了相同名称 |
| `unknown function: xxx` | 调用了未注册的内置/原生函数 |
| `There is no door!` | 脚本逻辑提示，非解析错误——当前方向无出口 |

---

更多示例见 `content/scripts/` 目录。
