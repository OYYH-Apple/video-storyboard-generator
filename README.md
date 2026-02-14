# Video Storyboard Generator

> 生成专业讲解视频分镜脚本的 Claude Skill，支持头脑风暴需求澄清和结构化时间轴分镜设计。

## ✨ 特性

- 🎯 **需求澄清** - 头脑风暴引导，帮你理清视频需求
- 🎬 **画面顺序** - 支持段落内多镜头序列设计
- 📋 **多种模板** - 技术教程、产品推广、故事讲述等预置模板
- 🔧 **配置化** - YAML 配置文件支持自定义默认值
- 💻 **交互式 CLI** - 向导式生成和批量处理
- 📊 **多格式导出** - Markdown / JSON / YAML

## 🚀 快速开始

### 前置要求

```bash
cd scripts
pip install -r requirements.txt
```

依赖：
- click >= 8.0.0
- PyYAML >= 6.0

### 方式 1: 交互式生成（推荐新手）

```bash
cd scripts
python cli.py interactive
```

跟随向导，逐步填写：
1. 视频标题
2. 视频时长
3. 视频类型（4种预置）
4. 角色设置
5. 输出格式
6. 确认生成

### 方式 2: 命令行生成（推荐高级用户）

```bash
python cli.py generate --title "AI技术讲解" --duration 60 --video-type tech_tutorial

# 导出 JSON 格式
python cli.py generate --title "产品介绍" --format json --duration 30
```

### 方式 3: 批量生成

创建 `batch.yaml`：

```yaml
- title: "技术视频"
  duration: 60
  video_type: "tech_tutorial"
- title: "产品视频"
  duration: 30
  video_type: "product_promo"
```

运行：

```bash
python cli.py batch batch.yaml
```

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
