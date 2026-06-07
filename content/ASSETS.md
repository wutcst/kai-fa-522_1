# 素材需求清单

本文件列出游戏脚本所引用的所有素材资源，请按以下规格提供。

## 图片格式要求

- 格式：**PNG**（推荐）或 JPG
- 背景图：**1280×720** 像素（16:9）
- 角色立绘：**高度 600-900px**，宽度自由，透明背景 PNG

## 背景图（放入 `content/images/`）

| 文件名 | 描述 |
|--------|------|
| `bg_outside.png` | 大学主入口外景，哥特式建筑、石拱门、校园远景 |
| `bg_theater.png` | 阶梯教室/讲堂内部，排排座椅、讲台、投影仪 |
| `bg_pub.png` | 校园酒吧/咖啡厅内部，暖色灯光、吧台、老照片墙 |
| `bg_lab.png` | 计算机实验室，一排排显示器、键盘、暗色调蓝光 |
| `bg_office.png` | 教务办公室，文件柜、办公桌、茶杯 |

## 角色立绘（放入 `content/images/`）

| 文件名 | 角色 | 描述 |
|--------|------|------|
| `char_guide.png` | 校园向导 | 友好的学生/助教形象，微笑 |
| `char_professor.png` | 教授 | 穿学术袍或正装，手持书本 |
| `char_barkeep.png` | 酒保 | 围裙、擦杯子、温和微笑 |
| `char_student.png` | 学生 | 戴眼镜、疲惫但专注、面前有笔记本电脑 |

## 字体（放入 `content/fonts/`）

| 文件名 | 说明 |
|--------|------|
| `default.ttf` | 主要 UI 字体，支持中英文（推荐：思源黑体/Noto Sans CJK） |

> 如不提供字体，Linux 下将自动回退到 DejaVu Sans（不支持中文）。
> Windows 下无回退字体将导致文字渲染失败，请务必提供。

## 目录结构预览

```
content/
├── fonts/
│   └── default.ttf
├── images/
│   ├── bg_outside.png
│   ├── bg_theater.png
│   ├── bg_pub.png
│   ├── bg_lab.png
│   ├── bg_office.png
│   ├── char_guide.png
│   ├── char_professor.png
│   ├── char_barkeep.png
│   └── char_student.png
└── scripts/
    ├── world.rpy
    └── story.rpy
```
