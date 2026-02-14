# Video Storyboard Generator

> 🎬 **Claude Skill** - 生成专业讲解视频分镜脚本，支持头脑风暴需求澄清和**画面顺序（镜头序列）**设计。

> **你的核心需求已实现** ✅ - 每个段落可包含多个镜头，精确控制视频节奏！

---

## 🎯 核心特性：画面顺序（镜头序列）

本项目的**核心创新**是 **画面顺序**（镜头序列）功能：

### 改进前后对比

**改进前（单一运镜）：**

```markdown
段落1：开场引入（0-12秒）
- 运镜：推近 + 环绕
- 布局：主角居中
- 旁白：开场白
```

**改进后（多镜头序列）✨：**
```markdown
段落1：开场引入（0-12秒）

**画面顺序**：
#### 镜头1：推近 (Dolly In)（0-3秒）
- **运镜**：从全黑快速推近
- **布局**：主角占屏 40%，标题满幅
- **视觉**：标题文字从四角飞入
- **过渡**：无缝过渡

#### 镜头2：环绕 (Orbiting)（3-12秒）
- **运镜**：360°环绕展示
- **布局**：主角居中，周围气泡
- **视觉**：主角表情变化
- **过渡**：平滑过渡

**旁白**：开场白
```

**优势：**
- ✅ 精确控制每个镜头的时间范围
- ✅ 每个镜头独立配置运镜、布局、视觉
- ✅ 更丰富的视觉表达效果

---

## 🚀 如何使用

### ⭐ 方式 1: 通过 Claude Skill（最简单，推荐）

**无需安装，直接在 Claude 对话中使用：**

```
我想做一个[你的视频主题]的分镜脚本
```

**示例对话：**

```
用户：我想做一个 AI 技术讲解视频
```

**Claude 会：**

1. 🧠 **头脑风暴引导** - 帮你理清需求
   - "这是技术概念还是产品介绍？"
   - "目标受众是初学者吗？"
   - "视频时长大概多久？"
   - "需要什么视觉风格？"
   - "需要角色助手吗？"

2. 📋 **段落结构设计** - 根据主题定制段落
   - 开场引入
   - 核心概念
   - 详细解析
   - 效果展示
   - 结尾号召

3. 🎬 **生成分镜脚本** - 每个段落包含 2-4 个镜头
   - 每个镜头时间范围独立指定
   - 运镜、布局、视觉、过渡精确描述

4. 💾 **确认保存** - 建议保存位置

**✅ 完全免费，不需要安装任何东西！**

---

### 🔧 方式 2: 使用 CLI 工具（高阶用户）

如果你需要：
- 批量生成多个视频分镜
- 集成到自动化流程
- 导出 JSON/YAML 格式

则使用 CLI 工具（需要安装依赖）：

```bash
cd scripts
pip install -r requirements.txt
python cli.py interactive
```

详见：[CLI 使用指南](scripts/INSTALL.md)

---

## 📂 项目结构

```
video-storyboard-generator/
├── SKILL.md                 # Skill 核心文档
├── README.md                # 本文件
├── config/                  # 配置文件
│   ├── default-config.yaml      # 默认配置
│   └── video-types.yaml         # 视频类型模板
├── examples/                # 示例合集
│   ├── short-video/             # 短视频（30秒）
│   ├── medium-video/            # 中等视频（60秒）
│   ├── long-video/              # 长视频（3分钟）
│   ├── json/                    # JSON 示例
│   └── yaml/                    # YAML 示例
├── references/              # 参考文档
│   ├── camera-movements.md   # 运镜类型
│   └── story-patterns.md     # 叙事模式
├── scripts/                 # 脚本文件
│   ├── cli.py                   # CLI 应用
│   ├── export.py                # 导出模块
│   ├── generate_storyboard.py   # 核心生成器
│   ├── requirements.txt         # 依赖
│   └── INSTALL.md               # 使用指南
└── docs/                    # 输出目录
```

## 🎨 视频类型

| 类型 | key | 视觉风格 | 适合场景 |
|------|-----|----------|----------|
| 技术教程 | tech_tutorial | 科技风（深蓝+粒子） | 技术讲解、概念演示 |
| 产品推广 | product_promo | 活泼轻松（明亮色彩） | 产品介绍、版本更新 |
| 故事讲述 | story_telling | 温暖柔和（渐变色彩） | 品牌故事、用户案例 |
| 数据洞察 | data_insight | 严肃专业（数据可视化） | 分析报告、趋势展示 |

## 📐 分镜结构

```
视频总体规格
└── 分镜段落
    ├── 段落目标
    ├── 画面顺序（镜头序列）← 新增！
    │   ├── 镜头1
    │   ├── 镜头2
    │   └── 镜头3
    └── 旁白
```

### 画面顺序（镜头序列）

每个段落包含多个镜头：

- **镜头编号** (shot_id)
- **时间范围** (time_range) - 如 "0-3秒"
- **镜头类型** (shot_type) - "推近 (Dolly In)"
- **运镜描述** (camera)
- **画面布局** (layout)
- **视觉元素** (visual)
- **过渡方式** (transition)

## ⚙️ 配置文件

### 默认配置 (`config/default-config.yaml`)

```yaml
video:
  fps: 30
  default_duration: 60
  output_format: "markdown"

visual:
  background_style: "深蓝渐变 + 神经网络线条流动 + 微光粒子"
  main_color: "蓝色"

output:
  directory: "./docs"
  filename_pattern: "{title}_storyboard.{extension}"
```

### 视频类型配置 (`config/video-types.yaml`)

4 种预置视频类型的完整配置模板。

## 📖 示例

查看 `examples/` 目录：

- [技术视频示例](examples/medium-video/microGPT-storyboard.md) - 60秒
- [产品推广示例](examples/short-video/product-intro-storyboard.md) - 30秒
- [教学视频示例](examples/long-video/guide-tutorial-storyboard.md) - 3分钟

生成所有示例：

```bash
python generate_all_examples.py
```

## 🛠️ CLI 命令

```bash
# 查看帮助
python cli.py --help

# 交互式生成
python cli.py interactive

# 命令行生成
python cli.py generate --title "标题" --duration 60 --video-type tech_tutorial

# 批量生成
python cli.py batch config.yaml

# 格式转换
python cli.py convert --input input.md --format json
```

## 📚 参考文档

- [SKILL.md](SKILL.md) - Skill 核心文档
- [运镜类型参考](references/camera-movements.md) - 完整运镜技术说明
- [叙事模式参考](references/story-patterns.md) - 6种叙事模式
- [scripts/INSTALL.md](scripts/INSTALL.md) - 详细安装使用指南

## 📄 License

MIT

---

**Made with ❤️ for video creators**
