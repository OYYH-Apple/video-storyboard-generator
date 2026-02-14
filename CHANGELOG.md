# Changelog

所有对 Video Storyboard Generator 的重大更改都会记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

## [2.0.0] - 2024-12-14

### 新增功能

#### 核心功能
- ✨ **画面顺序字段** - 在分镜段落中增加镜头序列（shots），支持段落内多镜头切换设计
  - 每个镜头独立指定时间范围、运镜方式、布局、视觉和过渡
  - 开场段落：3个镜头（快速切入 → 主体展示 → 细节特写）
  - 核心段落：2-4个镜头（环绕展示 → 流程跟踪 → 特写强调）
  - 结尾段落：2个镜头（汇聚元素 → 拉远全景）
  - 详见 SKILL.md "画面顺序" 章节

#### 配置化
- ⚙️ **YAML 配置文件支持**
  - `config/default-config.yaml` - 默认配置（FPS、时长、风格等）
  - `config/video-types.yaml` - 视频类型配置（技术教程、产品推广、故事讲述、数据洞察）
  - 支持自定义视频类型模板

#### CLI 工具
- 💻 **交互式 CLI 应用** (`scripts/cli.py`)
  - `interactive` - 向导式生成模式（5步骤：基本信息→视频类型→视觉设置→输出格式→确认）
  - `generate` - 命令行参数生成（支持 `--title`, `--duration`, `--video-type`, `--format`, `--output` 等）
  - `batch` - 批量生成（从 YAML 配置文件）
  - `convert` - 格式转换（Markdown → JSON/YAML）

#### 多格式导出
- 📊 **JSON/YAML 支持**
  - `scripts/export.py` - 导出模块，支持三种格式输出
  - 便于程序化处理和集成
  - 支持 Markdown ↔ JSON/YAML 双向转换
  - 可用于自动化脚本和处理流程

#### 示例合集
- 📁 **examples/ 文件夹**
  - 短视频示例（30秒）- `product-intro-storyboard.md`
  - 中等视频示例（60秒）- `microGPT-storyboard.md`
  - 中等视频示例（90秒）- `neural-network-demo.md`
  - 长视频示例（3分钟）- `guide-tutorial-storyboard.md`
  - `examples/README.md` - 示例使用说明文档

#### 文档增强
- 📚 **README.md** - 完整的使用指南
  - 快速开始（3种方式）
  - 项目结构说明
  - 视频类型表格
  - 分镜结构图示
  - CLI 命令参考
- 📚 **examples/README.md** - 示例合集说明
- 📚 **scripts/INSTALL.md** - 详细安装使用指南
- 📖 SKILL.md - 增加 CLI 使用方法章节、配置文件章节、输出格式说明
- 🖼️ `camera-movements.md` - 增加 ASCII 镜头序列组合示意图

#### 测试支持
- ✅ **test_full_workflow.py** - 端到端测试脚本
  - Markdown 生成测试
  - 镜头序列结构测试
  - 多时长视频测试
  - 文件生成和保存测试
- ✅ **generate_all_examples.py** - 自动生成所有示例文件

#### 其他新增
- 📦 `generate_storyboard_data()` 函数 - 生成结构化数据供导出
- 📦 `load_config()` / `load_video_type_config()` 配置加载函数
- 📦 `parse_markdown_to_dict()` Markdown 解析器（用于格式转换）

### 技术改进
- 🔧 **数据结构升级** - 从单一运镜扩展为镜头序列
  - 保持向后兼容：旧格式（单一运镜）仍然支持
  - 新结构：每个段落包含多个镜头，每个镜头独立配置

- 🔧 **render_markdown()** - Markdown 渲染函数分离

- 🔧 **段落生成函数改进**
  - `_generate_short_segments()` - 短视频镜头序列（2-3镜头/段落）
  - `_generate_medium_segments()` - 中等视频镜头序列（2-4镜头/段落）
  - `_generate_long_segments()` - 长视频镜头序列（2-3镜头/段落）

- 🔧 **_format_segment()** - 支持新旧两种格式的格式化函数

- 🔧 **generate_opencode_prompt()** - 更新提示词生成，支持镜头序列描述

### 重构

- 🔄 完全重构数据结构，从单一运镜扩展为镜头序列
- 🔄 模板 `storyboard-template.md` 更新以支持 shots 字段
- 🔄 输出格式统一 API（同一函数支持多种输出）
- 🔄 代码模块化（导出功能、测试、示例生成分离）

### 依赖变更

- 新增：`click >= 8.0.0` - CLI 框架
- 新增：`PyYAML >= 6.0` - YAML 配置和导出

### 兼容性

- ⚠️ **重大变更** - 段落数据结构变更（增加 shots 字段）
- ⚠️ **重大变更** - Python 脚本 API 变更（新增 video_type, config_path, output_format 等参数）
- ✅ 向后兼容：仍支持简化模式（自动生成默认镜头序列）
- ✅ 向后兼容：原有单一运镜格式仍然可用

---

## [1.0.0] - 2024-XX-XX

### 初始版本

#### 核心功能
- 🎬 头脑风暴引导和需求澄清
- 📋 分镜段落结构设计
- 🎬 运镜指导和画面布局
- 📝 Markdown 格式输出
- 🔗 OpenCode 提示词生成
- 💾 文件保存确认

#### 参考文档
- 运镜类型参考 (`references/camera-movements.md`)
- 常见叙事模式 (`references/story-patterns.md`)
- 分镜模板 (`assets/storyboard-template.md`)

#### 脚本
- `generate_storyboard.py` - 基础生成器（CLI 参数式）

---

## 版本对照

| 版本 | 主要变化 | 备注 |
|------|----------|------|
| 2.0.0 | +画面顺序、+配置化、+CLI、+多格式 | 激进全面重构 |
| 1.0.0 | 基础分镜生成 | 初始版本 |
