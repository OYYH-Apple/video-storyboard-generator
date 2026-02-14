# Video Storyboard Generator - 示例合集

这里包含了各种类型和时长的分镜脚本示例，帮助你快速上手。

## 📁 示例分类

### 短视频示例 (30秒)

适合快速推广、社交媒体视频。

- [`product-intro.md`](short-video/product-intro-storyboard.md) - 产品快速介绍
  - 时长：30秒
  - 类型：产品推广
  - 特点：快速节奏，2-3个镜头/段落

### 中等视频示例 (60秒-90秒)

适合技术讲解、概念演示。

- [`microGPT.md`](medium-video/microGPT-storyboard.md) - MicroGPT 原理讲解（60秒）
  - 类型：技术教程
  - 特点：清晰逻辑，3-4个镜头/段落
- [`neural-network.md`](medium-video/neural-network-demo.md) - 神经网络可视化（90秒）
  - 类型：数据洞察
  - 特点：专业风格，抽象图形为主

### 长视频示例 (3分钟)

适合深度教学、完整教程。

- [`guide-tutorial.md`](long-video/guide-tutorial-storyboard.md) - 完整教学教程（180秒）
  - 类型：故事讲述
  - 特点：逐步深入，详细讲解

## 📊 数据格式示例

### JSON 格式

路径：`json/microGPT-storyboard.json`（需手动生成）

适用于：
- 程序化生成
- 数据集成
- 自动化处理

### YAML 格式

路径：`yaml/microGPT-storyboard.yaml`（需手动生成）

适用于：
- 人工编辑
- 版本控制
- 配置管理

## 🎨 画面顺序示例

以下是一个段落中多镜头序列的示例（来自 microGPT）：

### 段落2：核心概念（12-24秒）

**段落目标**：解释核心概念或机制

#### 镜头1：推近 (Dolly In)（12-16秒）

- **运镜**：快速 spring dolly in，核心概念图从底部升起
- **布局**：概念图占屏50%，周围环绕关键词气泡
- **视觉**：核心概念文字飞入，关键词从四周stagger出现
- **过渡**：无缝过渡

#### 镜头2：环绕 (Orbiting)（16-24秒）

- **运镜**：360°环绕展示概念结构
- **布局**：核心概念居中，子概念环绕分布
- **视觉**：连接线波纹扩散，节点图标旋转
- **过渡**：平滑过渡

**旁白**："核心概念的核心在于..."（贯穿整个段落）

## 💡 如何使用示例

### 1. 学习结构

打开示例文件，观察：
- 段落如何组织
- 镜头序列如何设计
- 运镜描述如何撰写

### 2. 作为模板

复制示例，修改：
- 标题和内容
- 运镜方式（根据需求）
- 视觉元素

### 3. 参考模式

查看 `../references/story-patterns.md`，了解如何：
- 选择合适的叙事模式
- 设计段落结构
- 分配时间

## 🔄 生成新示例

```bash
# 使用 CLI 交互式生成
cd scripts
python cli.py interactive

# 或使用命令行生成
python cli.py generate --title "新视频" --duration 60 --video-type tech_tutorial

# 批量生成多个示例
python cli.py batch batch-config.yaml
```

## 📚 更多资源

- [运镜类型参考](../references/camera-movements.md)
- [叙事模式参考](../references/story-patterns.md)
- [Skill 文档](../SKILL.md)
- [主 README](../README.md)
