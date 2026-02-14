# 安装和使用指南

## 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

依赖列表：
- click >= 8.0.0 - CLI 框架
- PyYAML >= 6.0 - YAML 配置文件支持

## 使用方法

### 1. 交互式生成（推荐新手）

```bash
python cli.py interactive
```

跟随向导，逐步填写：
1. 视频标题
2. 视频时长
3. 视频类型（4种预置类型）
4. 是否需要角色
5. 输出格式
6. 确认后生成

输出位置：`./docs/{标题}_storyboard.md`

### 2. 命令行生成（推荐高级用户）

```bash
# 基本用法
python cli.py generate --title "视频标题" --duration 60

# 指定视频类型
python cli.py generate --title "技术讲解" --duration 60 --video-type tech_tutorial

# 指定输出格式（JSON/YAML）
python cli.py generate --title "技术讲解" --format json

# 自定义角色
python cli.py generate --title "产品介绍" --duration 30 --video-type product_promo --output ./custom/path.md
```

### 3. 批量生成

创建配置文件 `batch.yaml`：

```yaml
- title: "技术视频1"
  duration: 60
  video_type: "tech_tutorial"
- title: "产品视频2"
  duration: 30
  video_type: "product_promo"
- title: "教学视频3"
  duration: 180
  video_type: "story_telling"
```

运行批量生成：

```bash
python cli.py batch batch.yaml
```

### 4. 格式转换

将已有 Markdown 分镜转换为 JSON 或 YAML：

```bash
# 转换为 JSON
python cli.py convert --input ./docs/example.md --format json

# 转换为 YAML
python cli.py convert --input ./docs/example.md --format yaml --output ./output/example.yaml
```

## 视频类型说明

| 类型 | key | 视觉风格 | 适用场景 |
|------|-----|----------|----------|
| 技术教程 | tech_tutorial | 科技风（深蓝+粒子） | 技术讲解、概念演示 |
| 产品推广 | product_promo | 活泼轻松（明亮色彩） | 产品介绍、版本更新 |
| 故事讲述 | story_telling | 温暖柔和（渐变色彩） | 品牌故事、用户案例 |
| 数据洞察 | data_insight | 严肃专业（数据可视化） | 分析报告、趋势展示 |

## 输出格式

| 格式 | 文件扩展名 | 说明 |
|------|-----------|------|
| Markdown | .md | 易于阅读和编辑，默认格式 |
| JSON | .json | 机器可读，便于程序化处理 |
| YAML | .yaml | 可读性强的配置格式 |

## 配置文件

### 默认配置

位置：`../config/default-config.yaml`

可配置项：
- 视频参数（FPS、默认时长）
- 默认视觉风格
- 输出设置（目录、文件名模式）
- 镜头序列设置

### 视频类型配置

位置：`../config/video-types.yaml`

包含 4 种预置视频类型的完整配置模板。

## 示例

完整示例：`../examples/` 目录

- `short-video/` - 30 秒短视频示例
- `medium-video/` - 60 秒中等视频示例
- `long-video/` - 3 分钟长视频示例

生成所有示例：

```bash
cd ..
python generate_all_examples.py
```

## 故障排查

### PyYAML 未安装

**错误信息：**
```
警告: PyYAML 未安装，配置文件功能不可用
```

**解决方法：**
```bash
pip install PyYAML
```

### Click 未安装

**错误信息：**
```
错误: Click 未安装。请运行: pip install click
```

**解决方法：**
```bash
pip install click
```

### 字符编码问题（Windows 控制台）

**现象：** 控制台输出中文乱码

**解决方法：** 已在代码中处理，但仍建议：
1. 使用支持 UTF-8 的终端
2. 或输出到文件查看

## 命令参考

```bash
# 查看所有命令
python cli.py --help

# 查看 interactive 命令帮助
python cli.py interactive --help

# 查看 generate 命令帮助
python cli.py generate --help

# 查看 batch 命令帮助
python cli.py batch --help

# 查看 convert 命令帮助
python cli.py convert --help
```
