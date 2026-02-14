# Video Storyboard Generator - 激进全面重构实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 全面重构 video-storyboard-generator skill，增加画面顺序字段，添加示例、配置化、交互式 CLI、多格式导出和更多模板支持。

**Architecture:** 保持现有 SKILL.md + assets + references + scripts 结构，新增 examples/、config/、docs/ 文件夹，增强 Python 脚本为交互式 CLI，支持 YAML 配置文件，增加画面顺序到段落结构中。

**Tech Stack:** Python 3.8+, PyYAML, Click (CLI), Jinja2 (模板渲染)

---

## 阶段 1：核心数据结构升级（增加画面顺序）

### Task 1.1: 扩展段落数据结构

**修改文件：**
- `scripts/generate_storyboard.py` - 修改 `_generate_medium_segments` 等函数
- `assets/storyboard-template.md` - 更新段落模板

**Step 1: 在段落结构中增加 shots 字段**

修改段落数据结构，从单一运镜描述改为多个镜头序列：

```python
# 原结构（单一运镜）
{
    "title": "开场引入",
    "goal": "建立兴趣",
    "start": 0,
    "end": 12,
    "camera": "推近",
    "layout": "...",
    "visual": "...",
    "narration": "..."
}

# 新结构（多镜头序列）
{
    "title": "开场引入",
    "goal": "建立兴趣",
    "start": 0,
    "end": 12,
    "shots": [
        {
            "shot_id": 1,
            "time_range": "0-3秒",
            "shot_type": "推近 (Dolly In)",
            "camera": "快速 spring dolly in，主角从底部升起",
            "layout": "主角占屏40%，标题满幅",
            "visual": "标题文字从四角stagger飞入",
            "transition": "无缝过渡"
        },
        {
            "shot_id": 2,
            "time_range": "3-8秒",
            "shot_type": "环绕 (Orbiting)",
            "camera": "360°环绕展示主角",
            "layout": "主角居中，背景粒子流动",
            "visual": "主角表情变化，气泡提示",
            "transition": "平滑过渡"
        },
        {
            "shot_id": 3,
            "time_range": "8-12秒",
            "shot_type": "推近特写 (Close-up)",
            "camera": "推近到主角面部",
            "layout": "面部特写占屏60%",
            "visual": "眼睛发光，显示主题图标",
            "transition": "渐隐过渡"
        }
    ],
    "narration": "大家好！今天介绍这个主题..."
}
```

**Step 2: 更新段落输出格式**

在 `_format_segment` 函数中支持新结构：

```python
def _format_segment(seg: Dict, index: int) -> str:
    """格式化单个段落（支持多镜头序列）"""

    # 构建镜头序列
    shots_content = []
    for shot in seg.get('shots', []):
        shot_text = f"""
#### 镜头{shot['shot_id']}：{shot['shot_type']}（{shot['time_range']}）

- **运镜**：{shot['camera']}
- **布局**：{shot['layout']}
- **视觉**：{shot['visual']}
- **过渡**：{shot['transition']}
"""
        shots_content.append(shot_text)

    shots_formatted = "\n".join(shots_content)

    return f"""### 段落{index}：{seg['title']}（{seg['start']}-{seg['end']}秒）

**段落目标**：{seg['goal']}

**画面顺序**：
{shots_formatted}

**旁白**："{seg['narration']}" """
```

**Step 3: 测试新结构输出**

运行：`python scripts/generate_storyboard.py "测试视频" 60`

预期：输出包含三个镜头序列的段落格式。

**Step 4: 提交**

```bash
git add scripts/generate_storyboard.py
git commit -m "feat: 增加画面顺序字段，支持多镜头序列"
```

---

### Task 1.2: 更新模板文件

**修改文件：**
- `assets/storyboard-template.md`

**Step 1: 更新段落模板**

在模板中增加画面顺序部分：

```markdown
### 段落X：{{SEGMENT_TITLE}}（{{START_TIME}}-{{END_TIME}}秒）

**段落目标**：{{SEGMENT_GOAL}}

**画面顺序**：
{{SHOTS_SEQUENCE}}

**旁白**："{{NARRATION_CONTENT}}"
```

**Step 2: 增加镜头子模板**

在模板末尾增加镜头模板：

```markdown
## 镜头模板

### 镜头Y：{{SHOT_TITLE}}/{{SHOT_TYPE}}（{{SHOT_TIME_RANGE}}）

- **运镜**：{{CAMERA_MOVEMENT}}
- **布局**：{{SHOT_LAYOUT}}
- **视觉**：{{SHOT_VISUAL}}
- **过渡**：{{SHOT_TRANSITION}}
```

**Step 3: 更新变量说明表格**

增加镜头相关变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| {{SHOTS_SEQUENCE}} | 镜头序列内容 | 多个镜头的详细描述 |
| {{SHOT_TYPE}} | 镜头类型 | "推近 (Dolly In)" |
| {{SHOT_TIME_RANGE}} | 镜头时间范围 | "0-3秒" |
| {{SHOT_TRANSITION}} | 过渡方式 | "无缝过渡" |

**Step 4: 提交**

```bash
git add assets/storyboard-template.md
git commit -mfeat: 更新模板支持画面顺序"""
```

---

### Task 1.3: 更新参考文档

**修改文件：**
- `SKILL.md`
- `references/camera-movements.md`（可选，增加镜头序列示例）

**Step 1: 在 SKILL.md 中描述画面顺序**

在"阶段3：生成分镜脚本"部分增加镜头序列说明：

```markdown
#### 分镜段落
每个段落包含：
1. **段落目标** - 该段落要传达什么信息
2. **时间区间** - 开始和结束时间（秒）
3. **画面顺序（镜头序列）** - 段落内的多个镜头切换
   - 每个镜头包含：
     - 镜头编号（shot_id）
     - 时间范围（time_range）
     - 镜头类型（shot_type）
     - 运镜描述（camera）
     - 画面布局（layout）
     - 视觉元素（visual）
     - 过渡方式（transition）
4. **旁白内容** - 具体的解说词
```

**Step 2: 增加画面顺序设计指南**

在"最佳实践"部分增加：

```markdown
### 画面顺序设计

- **开场段落**（建议3个镜头）：快速切入 → 主体展示 → 细节特写
- **核心段落**（建议2-4个镜头）：环绕展示 → 跟随流程 → 特写强调
- **结尾段落**（建议2个镜头）：汇聚元素 → 拉远全景
- **镜头时长**：单个镜头通常3-6秒，过渡0.5-1秒
```

**Step 3: 提交**

```bash
git add SKILL.md
git commit -m "docs: 更新文档说明画面顺序设计"
```

---

## 阶段 2：示例文件夹创建

### Task 2.1: 创建 examples 目录结构

**新建目录：**
- `examples/` - 示例根目录
- `examples/short-video/` - 短视频示例（30秒）
- `examples/medium-video/` - 中等视频示例（60秒）
- `examples/long-video/` - 长视频示例（3分钟）

**Step 1: 创建目录结构**

```bash
mkdir -p examples/short-video examples/medium-video examples/long-video
```

**Step 2: 创建示例 1 - 技术视频（60秒）**

新建：`examples/medium-video/microGPT-storyboard.md`

**内容：** 完整的分镜脚本，展示画面顺序字段的实际使用，至少包含5个段落，每个段落有2-4个镜头。

**Step 3: 创建示例 2 - 产品推广（30秒）**

新建：`examples/short-video/product-intro-storyboard.md`

**内容：** 快节奏视频，每个段落2-3个镜头，强调快速切换。

**Step 4: 创建示例 3 - 教学视频（3分钟）**

新建：`examples/long-video/guide-tutorial-storyboard.md`

**内容：** 详细教学视频，6-8个段落，段落内有更多镜头分解。

**Step 5: 创建示例索引**

新建：`examples/README.md`

**内容：**
- 列出所有示例
- 每个示例的说明（时长、类型、特点）
- 如何使用示例的说明

**Step 6: 提交**

```bash
git add examples/
git commit -m "feat: 添加示例文件夹和完整示例"
```

---

### Task 2.2: 从示例生成 JSON/YAML 导出版本

**新建文件：**
- `examples/json/` - JSON 格式示例
- `examples/yaml/` - YAML 格式示例

**Step 1: 创建 JSON 示例**

新建：`examples/json/microGPT-storyboard.json`

**内容：** 对应 `medium-video/microGPT-storyboard.md` 的 JSON 版本，结构化的段落和镜头序列。

**Step 2: 创建 YAML 示例**

新建：`examples/yaml/microGPT-storyboard.yaml`

**内容：** 对应 JSON 的 YAML 版本。

**Step 3: 提交**

```bash
git add examples/json examples/yaml
git commit -m "feat: 添加 JSON/YAML 导出示例"
```

---

## 阶段 3：配置化和配置文件

### Task 3.1: 设计配置文件结构

**新建目录：**
- `config/` - 配置文件目录

**Step 1: 创建默认配置文件模板**

新建：`config/default-config.yaml`

**内容：**

```yaml
# Video Storyboard Generator 配置文件

# 视频总体设置
video:
  fps: 30
  default_duration: 60
  output_format: "markdown"  # markdown, json, yaml

# 默认视觉风格
visual:
  background_style: "深蓝渐变 + 神经网络线条流动 + 微光粒子"
  main_color: "蓝色"
  code_highlight: "专业"

# 默认旁白设置
narration:
  voice: "成熟中文男声"
  style: "专业自信 + 偶尔风趣"
  auto_subtitle: true

# 默认运镜设置
camera:
  default_rhythm: "快而流畅"
  transition_duration: 0.5

# 输出设置
output:
  directory: "./docs"
  filename_pattern: "{title}_storyboard.{extension}"
  create_directory: true

# 镜头序列设置
shots:
  min_per_segment: 2
  max_per_segment: 4
  default_shot_duration: 4
```

**Step 2: 创建视频类型配置文件**

新建：`config/video-types.yaml`

**内容：**

```yaml
# 不同视频类型的配置

tech_tutorial:  # 技术教程
  visual_style: "科技风（深蓝+粒子+神经网络）"
  character: "拟人化AI机器人"
  narration_style: "专业权威型"
  camera_rhythm: "中等节奏"
  segments_type: "概念-机制-应用模式"
  shots_per_segment: [3, 3, 4, 3, 2]

product_promo:  # 产品推广
  visual_style: "活泼轻松（明亮色彩+卡通元素）"
  character: "产品吉祥物"
  narration_style: "风趣调侃型"
  camera_rhythm: "快速动感"
  segments_type: "问题-解决方案模式"
  shots_per_segment: [2, 3, 3, 2, 2]

story_telling:  # 故事讲述
  visual_style: "温暖柔和（渐变色彩+情感化）"
  character: "角色人物"
  narration_style: "亲和教学型"
  camera_rhythm: "缓慢优雅"
  segments_type: "故事驱动模式"
  shots_per_segment: [3, 3, 4, 3, 2]

data_insight:  # 数据洞察
  visual_style: "严肃专业（简洁+数据可视化）"
  character: null
  narration_style: "专业权威型"
  camera_rhythm: "混合节奏"
  segments_type: "数据-洞察模式"
  shots_per_segment: [2, 3, 2, 3, 2]
```

**Step 3: 提交**

```bash
git add config/
git commit -m "feat: 添加配置文件结构"
```

---

### Task 3.2: 在 Python 脚本中集成配置文件

**修改文件：**
- `scripts/generate_storyboard.py`

**Step 1: 添加配置加载函数**

在文件头部增加：

```python
import yaml
from pathlib import Path

def load_config(config_path: Optional[str] = None) -> Dict:
    """加载配置文件"""
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config" / "default-config.yaml"

    if not Path(config_path).exists():
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_video_type_config(video_type: str) -> Dict:
    """加载视频类型配置"""
    config_path = Path(__file__).parent.parent / "config" / "video-types.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        all_types = yaml.safe_load(f)
        return all_types.get(video_type, {})
```

**Step 2: 修改 generate_storyboard 函数签名**

```python
def generate_storyboard(
    title: str,
    duration_seconds: Optional[int] = None,
    video_type: Optional[str] = None,
    config_path: Optional[str] = None,
    # 其他可选参数，可被配置覆盖
    background_style: Optional[str] = None,
    visual_style: Optional[str] = None,
    # ...
) -> str:
    """生成分镜脚本（支持配置文件）"""
    # 加载配置
    config = load_config(config_path)

    # 应用配置值（命令行参数优先）
    duration_seconds = duration_seconds or config.get('video', {}).get('default_duration', 60)
    fps = config.get('video', {}).get('fps', 30)

    # 加载视频类型配置
    if video_type:
        type_config = load_video_type_config(video_type)
        background_style = background_style or type_config.get('visual_style')
        visual_style = visual_style or type_config.get('visual_style')
        # ...其他字段

    # 其余逻辑...
```

**Step 3: 测试配置文件加载**

创建测试配置：`test-config.yaml`

运行测试脚本：
```python
# 简单测试
from generate_storyboard import load_config
print(load_config())
```

**Step 4: 提交**

```bash
git add scripts/generate_storyboard.py test-config.yaml
git commit -m "feat: 集成配置文件到生成器"
```

---

## 阶段 4：交互式 CLI

### Task 4.1: 重构为 Click CLI 应用

**新建文件：**
- `scripts/cli.py` - 新的交互式 CLI 入口

**修改文件：**
- `scripts/generate_storyboard.py` - 重构为模块化函数

**Step 1: 安装 Click**

在 `scripts/` 目录创建 `requirements.txt`：

```
click>=8.0.0
PyYAML>=6.0
```

运行：`pip install -r requirements.txt`

**Step 2: 创建交互式 CLI**

新建：`scripts/cli.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import click
from pathlib import Path
from generate_storyboard import generate_storyboard, load_video_type_config
import yaml

@click.group()
def cli():
    """Video Storyboard Generator - 分镜脚本生成器"""
    pass

@cli.command()
@click.option('--title', '-t', prompt=True, help='视频标题')
@click.option('--duration', '-d', default=60, help='视频时长（秒）')
@click.option('--video-type', '-v', type=click.Choice(['tech_tutorial', 'product_promo', 'story_telling', 'data_insight']),
              help='视频类型')
@click.option('--config', '-c', help='配置文件路径')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--format', '-f', type=click.Choice(['markdown', 'json', 'yaml']), default='markdown',
              help='输出格式')
def generate(title, duration, video_type, config, output, format):
    """生成分镜脚本（交互式模式）"""

    click.echo(f"\n🎬 正在生成分镜脚本...")
    click.echo(f"标题: {title}")
    click.echo(f"时长: {duration}秒")

    # 如果未指定视频类型，询问
    if not video_type:
        video_types = list(yaml.safe_load(
            open(Path(__file__).parent.parent / 'config' / 'video-types.yaml')
        ).keys())
        video_type = click.prompt(
            '选择视频类型',
            type=click.Choice(video_types),
            show_choices=True
        )

    # 其他交互式询问
    character = click.confirm('需要拟人化角色吗？', default=True)
    if character:
        main_character = click.prompt('角色描述', default='拟人化AI机器人')
    else:
        main_character = None

    # 生成脚本
    storyboard = generate_storyboard(
        title=title,
        duration_seconds=duration,
        video_type=video_type,
        config_path=config,
        main_character=main_character
    )

    # 确定输出路径
    if not output:
        import re
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        ext = {'markdown': 'md', 'json': 'json', 'yaml': 'yaml'}[format]
        output = f"./docs/{safe_title}_storyboard.{ext}"

    # 确认保存
    click.echo(f"\n📄 输出路径: {output}")
    if click.confirm('确认保存吗？'):
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write(storyboard)
        click.echo(f"✅ 分镜脚本已保存到: {output}")
    else:
        click.echo("❌ 已取消保存")

@cli.command()
def interactive():
    """完全交互式生成（向导模式）"""

    click.echo("\n" + "="*50)
    click.echo("  🎬 视频分镜脚本生成向导")
    click.echo("="*50 + "\n")

    # 步骤1: 基本信息
    click.echo("📋 步骤 1/5: 基本信息")
    title = click.prompt('视频标题', type=str)
    duration = click.prompt('视频时长（秒）', type=int, default=60)

    # 步骤2: 视频类型
    click.echo("\n📋 步骤 2/5: 视频类型")
    click.echo("  1. 技术教程 (tech_tutorial) - 科技风，专业权威")
    click.echo("  2. 产品推广 (product_promo) - 活泼轻松，风趣调侃")
    click.echo("  3. 故事讲述 (story_telling) - 温暖柔和，亲和教学")
    click.echo("  4. 数据洞察 (data_insight) - 严肃专业，数据展示")
    video_type = click.prompt('选择视频类型', type=click.Choice(['1', '2', '3', '4']))
    video_type_map = {'1': 'tech_tutorial', '2': 'product_promo', '3': 'story_telling', '4': 'data_insight'}
    video_type = video_type_map[video_type]

    # 步骤3: 视觉设置
    click.echo("\n📋 步骤 3/5: 视觉设置")
    use_character = click.confirm('需要拟人化角色吗？', default=True)
    main_character = None
    if use_character:
        main_character = click.prompt('角色描述（留空使用默认）', default='', show_default=False)
        if not main_character:
            main_character = '拟人化AI机器人'

    # 步骤4: 输出设置
    click.echo("\n📋 步骤 4/5: 输出设置")
    click.echo("  1. Markdown (.md) - 易于阅读和编辑")
    click.echo("  2. JSON (.json) - 机器可读，便于集成")
    click.echo("  3. YAML (.yaml) - 可读性强的配置格式")
    format_choice = click.prompt('输出格式', type=click.Choice(['1', '2', '3']), default='1')
    format_map = {'1': 'markdown', '2': 'json', '3': 'yaml'}
    output_format = format_map[format_choice]

    # 步骤5: 确认
    click.echo("\n📋 步骤 5/5: 确认信息")
    click.echo(f"  标题: {title}")
    click.echo(f"  时长: {duration}秒")
    click.echo(f"  类型: {video_type}")
    click.echo(f"  角色: {main_character if main_character else '无'}")
    click.echo(f"  格式: {output_format}")

    if not click.confirm('\n确认生成吗？'):
        click.echo("❌ 已取消")
        return

    # 生成并保存
    storyboard = generate_storyboard(
        title=title,
        duration_seconds=duration,
        video_type=video_type,
        main_character=main_character
    )

    import re
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    ext = {'markdown': 'md', 'json': 'json', 'yaml': 'yaml'}[output_format]
    output_path = f"./docs/{safe_title}_storyboard.{ext}"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(storyboard)

    click.echo(f"\n✅ 分镜脚本已保存到: {output_path}")
    click.echo(f"\n💡 提示：可以编辑该文件进行微调，或使用模板进行定制化设计")

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def batch(config_file):
    """批量生成（从配置文件）"""
    with open(config_file, 'r', encoding='utf-8') as f:
        configs = yaml.safe_load(f)

    click.echo(f"\n📦 批量生成 {len(configs)} 个视频分镜...")

    for i, cfg in enumerate(configs, 1):
        click.echo(f"\n[{i}/{len(configs)}] 生成: {cfg.get('title', 'Untitled')}")

        storyboard = generate_storyboard(**cfg)

        import re
        safe_title = re.sub(r'[^\w\s-]', '', cfg.get('title', 'Untitled')).strip().replace(' ', '_')
        output_path = f"./docs/{safe_title}_storyboard.md"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(storyboard)

        click.echo(f"  ✅ 已保存: {output_path}")

    click.echo("\n✅ 批量生成完成！")

if __name__ == '__main__':
    cli()
```

**Step 3: 测试 CLI 基本功能**

运行：`python scripts/cli.py --help`

预期：显示帮助信息，列出三个命令。

**Step 4: 测试交互式生成**

运行：`python scripts/cli.py interactive`

预期：启动向导，逐步询问用户。

**Step 5: 提交**

```bash
git add scripts/cli.py scripts/requirements.txt
git commit -m "feat: 添加交互式 CLI 应用"
```

---

### Task 4.2: 增加导出功能（JSON/YAML）

**新建文件：**
- `scripts/export.py` - 导出功能模块

**Step 1: 创建导出模块**

新建：`scripts/export.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import yaml
from typing import Dict
from datetime import datetime

def export_to_json(storyboard: Dict, include_opencode_prompt: bool = True) -> str:
    """导出为 JSON 格式"""
    data = {
        "metadata": {
            "title": storyboard.get("title"),
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": storyboard.get("duration_seconds"),
            "total_frames": storyboard.get("total_frames")
        },
        "video_specs": {
            "background": storyboard.get("background_style"),
            "visual_style": storyboard.get("visual_style"),
            "character": storyboard.get("main_character"),
            "narration": storyboard.get("narration_style"),
            "fps": storyboard.get("fps", 30)
        },
        "segments": storyboard.get("segments", [])
    }

    if include_opencode_prompt:
        data["opencode_prompt"] = storyboard.get("opencode_prompt")

    return json.dumps(data, ensure_ascii=False, indent=2)

def export_to_yaml(storyboard: Dict, include_opencode_prompt: bool = True) -> str:
    """导出为 YAML 格式"""
    data = {
        "metadata": {
            "title": storyboard.get("title"),
            "version": "1.0",
            "generated_at": datetime.now().isoformat(),
            "duration_seconds": storyboard.get("duration_seconds"),
            "total_frames": storyboard.get("total_frames")
        },
        "video_specs": {
            "background": storyboard.get("background_style"),
            "visual_style": storyboard.get("visual_style"),
            "character": storyboard.get("main_character"),
            "narration": storyboard.get("narration_style"),
            "fps": storyboard.get("fps", 30)
        },
        "segments": storyboard.get("segments", [])
    }

    if include_opencode_prompt:
        data["opencode_prompt"] = storyboard.get("opencode_prompt")

    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)

def parse_markdown_to_dict(markdown_content: str) -> Dict:
    """将 Markdown 分镜脚本解析为字典（用于从已有 MD 导出 JSON/YAML）"""
    # 简化版解析，实际实现需要完整解析 Markdown
    lines = markdown_content.split('\n')
    result = {
        "title": "",
        "duration_seconds": 60,
        "segments": []
    }

    # TODO: 实现完整的 Markdown 解析逻辑
    # 这里给出框架

    return result
```

**Step 2: 在 generate_storyboard.py 中生成结构化数据**

修改函数返回值，同时返回结构和文本：

```python
def generate_storyboard_data(
    title: str,
    # ... 其他参数
) -> Dict:
    """生成分镜脚本数据（结构化）"""

    total_frames = duration_seconds * fps

    # 生成段落数据（包含镜头序列）
    segments = []
    for i, seg in enumerate(base_segments, 1):
        segment_data = {
            "index": i,
            "title": seg['title'],
            "goal": seg['goal'],
            "start": seg['start'],
            "end": seg['end'],
            "shots": seg.get('shots', []),
            "narration": seg['narration']
        }
        segments.append(segment_data)

    data = {
        "title": title,
        "duration_seconds": duration_seconds,
        "total_frames": total_frames,
        "fps": fps,
        "background_style": background_style,
        "visual_style": visual_style,
        "main_character": main_character,
        "narration_style": narration_style,
        "segments": segments
    }

    return data

def generate_storyboard(
    title: str,
    # ... 参数同上
    output_format: str = "markdown"
) -> str:
    """生成分镜脚本（根据格式返回）"""

    # 生成结构化数据
    data = generate_storyboard_data(
        title=title,
        duration_seconds=duration_seconds,
        # ... 其他参数
    )

    # 生成 OpenCode 提示词
    data["opencode_prompt"] = generate_opencode_prompt(
        title=title,
        duration_seconds=duration_seconds,
        segments=data["segments"],
        background_style=data["background_style"],
        visual_style=data["visual_style"],
        narration_style=data["narration_style"]
    )

    # 根据格式导出
    if output_format == "json":
        return export_to_json(data)
    elif output_format == "yaml":
        return export_to_yaml(data)
    else:  # markdown
        return render_markdown(data)
```

**Step 3: 在 cli.py 中使用导出功能**

```python
from export import export_to_json, export_to_yaml

@cli.command()
@click.option('--input', '-i', required=True, help='输入 Markdown 文件路径')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml']), required=True, help='输出格式')
@click.option('--output', '-o', help='输出文件路径（默认：同名文件）')
def convert(input, format, output):
    """转换已有 Markdown 分镜为 JSON/YAML"""
    from export import parse_markdown_to_dict

    with open(input, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    data = parse_markdown_to_dict(markdown_content)

    if format == 'json':
        result = export_to_json(data)
        default_output = input.replace('.md', '.json')
    else:
        result = export_to_yaml(data)
        default_output = input.replace('.md', '.yaml')

    if not output:
        output = default_output

    with open(output, 'w', encoding='utf-8') as f:
        f.write(result)

    click.echo(f"✅ 已转换: {input} → {output}")
```

**Step 4: 测试导出功能**

运行：`python scripts/cli.py generate --title "测试" --duration 60 --format json`

预期：生成 JSON 格式输出。

运行：`python scripts/cli.py generate --title "测试" --duration 60 --format yaml`

预期：生成 YAML 格式输出。

**Step 5: 提交**

```bash
git add scripts/export.py scripts/cli.py
git commit -m "feat: 添加 JSON/YAML 导出和转换功能"
```

---

## 阶段 5：README 文档

### Task 5.1: 创建主 README

**新建文件：**
- `README.md`

**Step 1: 编写完整的 README**

```markdown
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

### 方式 1: 交互式生成（推荐）

```bash
cd scripts
pip install -r requirements.txt
python cli.py interactive
```

跟随向导完成视频分镜生成。

### 方式 2: 命令行生成

```bash
python cli.py generate --title "AI技术讲解" --duration 60 --video-type tech_tutorial
```

### 方式 3: 批量生成

创建配置文件 `batch.yaml`：

```yaml
- title: "视频1"
  duration: 60
  video_type: "tech_tutorial"
- title: "视频2"
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
├── assets/                  # 资产文件
│   └── storyboard-template.md  # 分镜模板
├── config/                  # 配置文件
│   ├── default-config.yaml      # 默认配置
│   └── video-types.yaml         # 视频类型配置
├── examples/                # 示例合集
│   ├── short-video/             # 短视频示例（30秒）
│   ├── medium-video/            # 中等视频示例（60秒）
│   ├── long-video/              # 长视频示例（3分钟）
│   ├── json/                    # JSON 格式示例
│   └── yaml/                    # YAML 格式示例
├── references/              # 参考文档
│   ├── camera-movements.md   # 运镜类型参考
│   └── story-patterns.md     # 常见叙事模式
├── scripts/                 # 脚本文件
│   ├── cli.py                   # 交互式 CLI
│   ├── generate_storyboard.py   # 生成器核心
│   ├── export.py                # 导出功能
│   └── requirements.txt         # 依赖列表
└── docs/                    # 输出目录
    └── [生成的分镜脚本]
```

## 🎨 视频类型预览

| 类型 | 说明 | 视觉风格 | 适合场景 |
|------|------|----------|----------|
| `tech_tutorial` | 技术教程 | 科技风（深蓝+粒子） | 技术讲解、概念演示 |
| `product_promo` | 产品推广 | 活泼轻松（明快色彩） | 产品介绍、版本更新 |
| `story_telling` | 故事讲述 | 温暖柔和（渐变色彩） | 品牌故事、用户案例 |
| `data_insight` | 数据洞察 | 严肃专业（数据可视化） | 分析报告、趋势展示 |

## 📐 分镜脚本结构

生成的分镜包含以下层次：

```
视频总体规格
└── 分镜段落
    └── 段落目标
    ├── 画面顺序（镜头序列）
    │   ├── 镜头1
    │   ├── 镜头2
    │   └── 镜头3
    └── 旁白
```

### 画面顺序（镜头序列）

每个段落可包含多个镜头，每个镜头包含：

- **镜头编号** (`shot_id`) - 镜头序列号
- **时间范围** (`time_range`) - 该镜头的时间段（如 "0-3秒"）
- **镜头类型** (`shot_type`) - 运镜方式（如 "推近 (Dolly In)"）
- **运镜描述** (`camera`) - 详细的摄像机运动
- **画面布局** (`layout`) - 元素布局方式
- **视觉元素** (`visual`) - 具体的图形/动画
- **过渡方式** (`transition`) - 镜头间的过渡效果

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

每个视频类型有独立的运镜节奏、镜头数量等配置。

## 📖 示例

查看 `examples/` 目录获取完整示例：

- [技术视频示例](examples/medium-video/microGPT-storyboard.md) - 60秒技术讲解
- [产品推广示例](examples/short-video/product-intro-storyboard.md) - 30秒快速推广
- [教学视频示例](examples/long-video/guide-tutorial-storyboard.md) - 3分钟详细教程

## 🛠️ CLI 命令

```bash
# 查看帮助
python cli.py --help

# 互动式生成
python cli.py interactive

# 命令行生成
python cli.py generate --title "标题" --duration 60

# 批量生成
python cli.py batch config.yaml

# 格式转换
python cli.py convert --input input.md --format json
```

## 📚 参考文档

- [SKILL.md](SKILL.md) - Skill 核心文档，完整的工作流程
- [运镜类型参考](references/camera-movements.md) - 完整的运镜技术说明
- [叙事模式参考](references/story-patterns.md) - 6种常见叙事模式

## 🤝 Contributing

欢迎提交 Issue 和 PR！

常见贡献方向：
- 添加新的视频类型模板
- 优化镜头序列生成逻辑
- 增加更多导出格式
- 完善文档和示例

## 📄 License

MIT

---

**Made with ❤️ for video creators**
```

**Step 2: 测试 README 链接**

检查所有文件链接是否正确。

**Step 3: 提交**

```bash
git add README.md
git commit -m "docs: 创建完整 README 文档"
```

---

### Task 5.2: 创建 examples/README.md

**新建文件：**
- `examples/README.md`

**Step 1: 编写示例说明**

```markdown
# Video Storyboard Generator - 示例合集

这里包含了各种类型和时长的分镜脚本示例，帮助你快速上手。

## 📁 示例分类

### 短视频示例 (30秒)

适用于快速推广、社交媒体视频。

- [product-intro](short-video/product-intro-storyboard.md) - 产品快速介绍
  - 时长：30秒
  - 类型：产品推广
  - 特点：快速节奏，2-3个镜头/段落

### 中等长度视频 (60秒)

适用于技术讲解、概念演示。

- [microGPT](medium-video/microGPT-storyboard.md) - MicroGPT 原理讲解
  - 时长：60秒
  - 类型：技术教程
  - 特点：清晰逻辑，3-4个镜头/段落
  - 预置镜头序列：每个段落有详细的多镜头设计

### 长视频 (3分钟)

适用于深度教学、完整教程。

- [guide-tutorial](long-video/guide-tutorial-storyboard.md) - 完整教学教程
  - 时长：180秒（3分钟）
  - 类型：故事讲述
  - 特点：逐步深入，详细讲解

## 📊 数据格式示例

### JSON 格式

[json/microGPT-storyboard.json](json/microGPT-storyboard.md) - 机器可读的结构化格式

适用于：
- 程序化生成
- 数据集成
- 自动化处理

### YAML 格式

[yaml/microGPT-storyboard.yaml](yaml/microGPT-storyboard.md) - 可读性强的配置格式

适用于：
- 人工编辑
- 版本控制
- 配置管理

## 🎨 画面顺序示例

以下是一个段落中多镜头序列的示例（来自 microGPT 示例）：

### 段落2：核心概念（12-28秒）

**段落目标**：解释核心概念或机制

#### 镜头1：推近 (Dolly In)（12-15秒）

- **运镜**：快速 spring dolly in，核心概念图从底部升起
- **布局**：概念图占屏50%，周围环绕关键词气泡
- **视觉**：核心概念文字飞入，关键词从四周stagger出现
- **过渡**：无缝过渡

#### 镜头2：环绕 (Orbiting)（15-23秒）

- **运镜**：360°环绕展示概念结构
- **布局**：核心概念居中，子概念环绕分布
- **视觉**：连接线波纹扩散，节点图标旋转
- **过渡**：平滑过渡

#### 镜头3：特写 (Close-up)（23-28秒）

- **运镜**：推近到核心概念细节
- **布局**：细节区域占屏60%
- **视觉**：关键图标放大，特效闪烁
- **过渡**：渐隐过渡

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

查看 `story-patterns.md`，了解如何：
- 选择合适的叙事模式
- 设计段落结构
- 分配时间

## 🔄 从示例生成新视频

```bash
# 使用示例作为模板
python scripts/cli.py interactive
# 选择视频类型时，参考示例中的类型
```

## 📚 更多资源

- [运镜类型参考](../references/camera-movements.md)
- [叙事模式参考](../references/story-patterns.md)
- [Skill 文档](../SKILL.md)
```

**Step 2: 提交**

```bash
git add examples/README.md
git commit -m "docs: 添加示例说明文档"
```

---

## 阶段 6：运镜参考增强

### Task 6.1: 增加运镜 ASCII 图示

**修改文件：**
- `references/camera-movements.md`

**Step 1: 为每个运镜类型增加 ASCII 示意图**

在运镜类型描述后增加可视化示意：

```markdown
### 推近 (Dolly In)

- **效果**：镜头向前推进，强调主体
- **参数**：spring dolly in（高系数，带轻微弹跳感）
- **适用场景**：开场、强调重要元素、展示细节
- **动画配合**：主体从底部spring升起并轻微旋转

**视觉效果示意**：

```
初始状态:        →     中间状态:        →     最终状态:
   ┌────────┐           ┌────────┐           ┌────────┐
   │  框1   │           │  框2   │           │  框3   │
   │        │           │        │           │        │
   │  [主体]│    ←      │   [   ]│    ←      │   [ ]  │
   │        │   镜头    │  [    ]│   镜头    │  [  ]  │
   │        │   推近    │ [    ] │   推近    │ [    ] │
   └────────┘           └────────┘           └────────┘

   全景视图              中景视角             近景特写
```

**动画时序**：

```
时间轴:  0s ---- 1s ---- 2s ---- 3s
运镜:    全景 →  推近  →  弹跳  →  定位
主体:    出现 →  放大  →  旋转 →  停止
```
```

对以下运镜类型都增加类似示意：
- 拉远 (Dolly Out)
- 环绕 (Orbiting)
- 跟拍 (Tracking Shot)
- 摇移 (Pan)
- 特写 (Close-up)
- 汇聚 (Converge)
- 环绕+跟踪 (Orbiting + Tracking)

**Step 2: 增加镜头序列组合示例**

在文档末尾增加新的章节：

```markdown
## 镜头序列组合示例

### 开场段落典型序列

```
镜头1: 快速推近 (0-3秒)
   ┌────────┐           ┌────────┐           ┌────────┐
   │  帧A1  │    →      │  帧A2  │    →      │  帧A3  │
   │        │           │        │           │        │
   │        │           │  主角  │           │  主角  │
   │        │           │   ↑    │           │  ↑↑   │
   └────────┘           └────────┘           └────────┘

镜头2: 环绕展示 (3-8秒)
    ↗ ↑ ↖
  ↗  主角  ↖
 →  (360°)  ←
  ↘ 转动   ↙
    ↘ ↓ ↙

镜头3: 特写 (8-12秒)
   ┌────────┐
   │        │
   │   [眼] │ ← 特写面部细节
   │   睛   │
   └────────┘
```

### 核心段落典型序列

```
镜头1: 展示全景 (0-4秒)
   ┌─────────────────┐
   │   完整结构展示   │
   │                  │
   └─────────────────┘

镜头2: 分层拆解 (4-10秒)
   ┌─────────┬─────────┬─────────┐
   │  层1    │  层2    │  层3    │
   │  [ ]    │  [ ]    │  [ ]    │
   └─────────┴─────────┴─────────┘

镜头3: 流程跟踪 (10-15秒)
   → → → → → → →
   [输入]→[处理1]→[处理2]→[输出]
```
```

**Step 3: 提交**

```bash
git add references/camera-movements.md
git commit -m "docs: 运镜参考增加 ASCII 示意图"
```

---

## 阶段 7：测试和验证

### Task 7.1: 创建端到端测试脚本

**新建文件：**
- `scripts/test_full_workflow.py`

**Step 1: 编写完整工作流测试**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端工作流测试脚本"""

import sys
from pathlib import Path
from generate_storyboard import generate_storyboard
from export import export_to_json, export_to_yaml
import yaml

def test_markdown_generation():
    """测试 Markdown 生成"""
    print("\n[测试 1/4] Markdown 生成...")
    result = generate_storyboard(
        title="测试视频",
        duration_seconds=60,
        video_type="tech_tutorial",
        output_format="markdown"
    )

    assert "测试视频" in result
    assert "分镜段落设计" in result
    assert "画面顺序" in result  # 新增字段
    print("✅ Markdown 生成测试通过")
    return result

def test_json_generation():
    """测试 JSON 生成"""
    print("\n[测试 2/4] JSON 生成...")
    result = generate_storyboard(
        title="测试视频",
        duration_seconds=60,
        video_type="tech_tutorial",
        output_format="json"
    )

    import json
    data = json.loads(result)
    assert data["title"] == "测试视频"
    assert "segments" in data
    assert "shots" in data["segments"][0]  # 新增字段
    print("✅ JSON 生成测试通过")
    return result

def test_yaml_generation():
    """测试 YAML 生成"""
    print("\n[测试 3/4] YAML 生成...")
    result = generate_storyboard(
        title="测试视频",
        duration_seconds=60,
        video_type="tech_tutorial",
        output_format="yaml"
    )

    data = yaml.safe_load(result)
    assert data["title"] == "测试视频"
    assert "segments" in data
    print("✅ YAML 生成测试通过")
    return result

def test_shots_sequence():
    """测试镜头序列生成"""
    print("\n[测试 4/4] 镜头序列结构...")

    result = generate_storyboard(
        title="测试视频",
        duration_seconds=60,
        video_type="tech_tutorial"
    )

    # 检查镜头序列标记
    assert "镜头1" in result or "镜头 1" in result or "shot_id" in result
    assert "镜头2" in result or "镜头 2" in result or "shot" in result

    print("✅ 镜头序列测试通过")

def test_config_loading():
    """测试配置文件加载"""
    print("\n[测试 5/5] 配置文件加载...")

    config_path = Path(__file__).parent.parent / "config" / "default-config.yaml"
    if config_path.exists():
        from generate_storyboard import load_config
        config = load_config(str(config_path))

        assert config is not None
        assert "video" in config
        print("✅ 配置文件加载测试通过")
    else:
        print("⚠️  配置文件不存在，跳过测试")

def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("  Video Storyboard Generator - 端到端测试")
    print("="*60)

    tests = [
        test_markdown_generation,
        test_json_generation,
        test_yaml_generation,
        test_shots_sequence,
        test_config_loading
    ]

    failed = []

    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} 失败: {e}")
            failed.append(test.__name__)

    print("\n" + "="*60)
    if failed:
        print(f"❌ 测试失败: {len(failed)}/{len(tests)}")
        for name in failed:
            print(f"   - {name}")
        print("="*60)
        sys.exit(1)
    else:
        print(f"✅ 所有测试通过: {len(tests)}/{len(tests)}")
        print("="*60)
        sys.exit(0)

if __name__ == "__main__":
    run_all_tests()
```

**Step 2: 运行测试**

```bash
cd scripts
python test_full_workflow.py
```

预期：所有测试通过。

**Step 3: 修复任何测试失败的问题（如有）**

**Step 4: 提交**

```bash
git add scripts/test_full_workflow.py
git commit -m "test: 添加端到端测试脚本"
```

---

### Task 7.2: 创建 examples 生成脚本

**新建文件：**
- `scripts/generate_all_examples.py`

**Step 1: 编写示例生成脚本**

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成所有示例文件"""

from pathlib import Path
from generate_storyboard import generate_storyboard
from export import export_to_json, export_to_yaml

def generate_examples():
    """生成所有示例文件"""

    examples_dir = Path(__file__).parent.parent / "examples"

    # 1. 短视频示例 (30秒)
    print("\n[1/3] 生成短视频示例...")
    short_video = generate_storyboard(
        title="产品快速介绍",
        duration_seconds=30,
        video_type="product_promo",
        output_format="markdown"
    )
    (examples_dir / "short-video" / "product-intro-storyboard.md").write_text(
        short_video, encoding='utf-8'
    )
    print("   ✅ product-intro-storyboard.md")

    # 2. 中等视频示例 (60秒)
    print("\n[2/3] 生成中等视频示例...")
    medium_video = generate_storyboard(
        title="MicroGPT 原理讲解",
        duration_seconds=60,
        video_type="tech_tutorial",
        output_format="markdown"
    )
    (examples_dir / "medium-video" / "microGPT-storyboard.md").write_text(
        medium_video, encoding='utf-8'
    )
    print("   ✅ microGPT-storyboard.md")

    # 生成 JSON 和 YAML 版本
    medium_data = generate_storyboard(
        title="MicroGPT 原理讲解",
        duration_seconds=60,
        video_type="tech_tutorial",
        output_format="json"
    )
    (examples_dir / "json" / "microGPT-storyboard.json").write_text(
        medium_data, encoding='utf-8'
    )
    print("   ✅ microGPT-storyboard.json")

    medium_yaml = generate_storyboard(
        title="MicroGPT 原理讲解",
        duration_seconds=60,
        video_type="tech_tutorial",
        output_format="yaml"
    )
    (examples_dir / "yaml" / "microGPT-storyboard.yaml").write_text(
        medium_yaml, encoding='utf-8'
    )
    print("   ✅ microGPT-storyboard.yaml")

    # 3. 长视频示例 (180秒)
    print("\n[3/3] 生成长视频示例...")
    long_video = generate_storyboard(
        title="完整教学教程",
        duration_seconds=180,
        video_type="story_telling",
        output_format="markdown"
    )
    (examples_dir / "long-video" / "guide-tutorial-storyboard.md").write_text(
        long_video, encoding='utf-8'
    )
    print("   ✅ guide-tutorial-storyboard.md")

    print("\n" + "="*50)
    print("✅ 所有示例生成完成！")
    print("="*50)

if __name__ == "__main__":
    generate_examples()
```

**Step 2: 运行生成脚本**

```bash
cd scripts
python generate_all_examples.py
```

预期：在 `examples/` 目录生成所有示例文件。

**Step 3: 提交**

```bash
git add scripts/generate_all_examples.py examples/
git commit -m "feat: 生成所有示例文件"
```

---

## 阶段 8：最终集成和文档

### Task 8.1: 更新 SKILL.md 完整工作流

**修改文件：**
- `SKILL.md`

**Step 1: 在"使用方法"部分增加 CLI 说明**

在适当位置增加：

```markdown
## 使用方法

### 通过 Claude 对话（推荐）

当需要生成分镜脚本时，直接进行头脑风暴对话。Skill 会：
1. 引导澄清需求
2. 设计段落结构
3. 生成带画面顺序的分镜脚本
4. 确认保存位置

### 通过 CLI 脚本

查看完整文档：[README.md](README.md)

**快速开始：**

```bash
cd scripts
pip install -r requirements.txt

# 交互式生成（推荐）
python cli.py interactive

# 命令行生成
python cli.py generate --title "视频标题" --duration 60

# 批量生成
python cli.py batch config.yaml

# 格式转换
python cli.py convert --input input.md --format json
```

**视频类型：**
- `tech_tutorial` - 技术教程
- `product_promo` - 产品推广
- `story_telling` - 故事讲述
- `data_insight` - 数据洞察

**输出格式：**
- `markdown` - 默认，易于阅读
- `json` - 机器可读
- `yaml` - 配置格式
```

**Step 2: 在"画面顺序"部分增加详细说明**

在段落结构部分增强：

```markdown
#### 画面顺序（镜头序列）

每个段落包含一个镜头序列，描述该段落内画面的切换顺序。

**镜头序列的作用：**
- 细化节奏控制：精确控制每个镜头的时长和切换
- 丰富视觉表达：通过多镜头组合增强表现力
- 明确运镜规划：每个镜头独立描述运镜方式

**镜头序列设计原则：**
- 开场段落：3个镜头（快速切入 → 主体展示 → 细节特写）
- 核心段落：2-4个镜头（环绕展示 → 流程跟踪 → 特写强调）
- 结尾段落：2个镜头（汇聚元素 → 拉远全景）
- 单镜头时长：3-6秒为宜，过渡0.5-1秒

**镜头字段说明：**
```
镜头X（时间范围）：
- 运镜：详细的摄像机运动描述
- 布局：元素如何分布
- 视觉：具体的图形/动画
- 过渡：与下一个镜头的过渡方式
```

**示例：**
查看 `examples/medium-video/microGPT-storyboard.md` 获取完整镜头序列示例。
```

**Step 3: 增加配置文件章节

```markdown
## 配置文件

Skill 支持通过 YAML 配置文件自定义默认值和视频类型。

### 默认配置

位置：`config/default-config.yaml`

可配置项：
- 视频参数（FPS、默认时长）
- 默认视觉风格
- 输出设置
- 镜头序列设置

### 视频类型配置

位置：`config/video-types.yaml`

预置4种视频类型的完整配置：
- 技术教程
- 产品推广
- 故事讲述
- 数据洞察

可自定义添加新视频类型。

### 使用配置

在对话中指定视频类型：

```
用户：我要做一个技术教程视频
Assistant：好的，将使用技术教程模板配置...
```

或在 CLI 中指定：

```bash
python cli.py generate --video-type tech_tutorial
```
```

**Step 4: 更新输出格式说明

```markdown
## 输出格式

生成的分镜脚本支持三种格式：

### Markdown 格式（默认）

- 易于人类阅读和编辑
- 包含完整的说明和注释
- 适合作为参考文档
- 文件位置：`./docs/{标题}_storyboard.md`

### JSON 格式

- 机器可读的结构化数据
- 便于程序化处理和集成
- 适合自动化工具
- 文件位置：`./docs/{标题}_storyboard.json`

**JSON 结构：**
```json
{
  "metadata": {...},
  "video_specs": {...},
  "segments": [
    {
      "index": 1,
      "title": "段落标题",
      "shots": [...],  // 镜头序列
      "narration": "..."
    }
  ]
}
```

### YAML 格式

- 可读性强的配置格式
- 适合版本控制和人工编辑
- 兼容 YAML 工具
- 文件位置：`./docs/{标题}_storyboard.yaml`

### 格式转换

已有 Markdown 可以转换为 JSON/YAML：

```bash
python cli.py convert --input input.md --format json
```
```

**Step 5: 提交**

```bash
git add SKILL.md
git commit -m "docs: 更新 Skill 文档完整工作流"
```

---

### Task 8.2: 创建 CHANGELOG

**新建文件：**
- `CHANGELOG.md`

**Step 1: 编写变更日志**

```markdown
# Changelog

All notable changes to Video Storyboard Generator will be documented in this file.

## [2.0.0] - 2024-12-XX

### 新增功能

#### 核心功能
- ✨ **画面顺序字段** - 在分镜段落中增加镜头序列（shots），支持段落内多镜头切换设计
  - 每个镜头独立指定时间范围、运镜方式、布局、视觉和过渡
  - 开场段落：3个镜头（快速切入 → 主体展示 → 细节特写）
  - 核心段落：2-4个镜头
  - 结尾段落：2个镜头
  - 详见 SKILL.md "画面顺序" 章节

#### 配置化
- ⚙️ **YAML 配置文件支持**
  - `config/default-config.yaml` - 默认配置（FPS、时长、风格等）
  - `config/video-types.yaml` - 视频类型配置（技术教程、产品推广、故事讲述、数据洞察）
  - 支持自定义视频类型模板

#### CLI 工具
- 💻 **交互式 CLI 应用** (`scripts/cli.py`)
  - `interactive` - 向导式生成模式
  - `generate` - 命令行参数生成
  - `batch` - 批量生成（从配置文件）
  - `convert` - 格式转换（MD → JSON/YAML）

#### 多格式导出
- 📊 **JSON/YAML 支持**
  - 结构化数据导出
  - 便于程序化处理和集成
  - 支持 Markdown ↔ JSON/YAML 转换

#### 示例合集
- 📁 **examples/ 文件夹**
  - 短视频示例（30秒）- 产品快速介绍
  - 中等视频示例（60秒）- MicroGPT 原理讲解
  - 长视频示例（3分钟）- 完整教学教程
  - JSON/YAML 格式示例

#### 文档增强
- 📚 **README.md** - 完整的使用指南
- 📚 **examples/README.md** - 示例说明文档
- 🖼️ **运镜 ASCII 示意图** - 在 `camera-movements.md` 中增加可视化示意
- 📚 **CHANGELOG.md** - 变更日志（本文件）

### 技术改进
- 🔧 `generate_storyboard.py` - 重构为模块化函数，支持结构化数据
- 🔧 `export.py` - 新增导出模块
- 🔧 渲染函数分离（Markdown/JSON/YAML）
- 🔧 镜头序列生成逻辑

### 测试
- ✅ `test_full_workflow.py` - 端到端测试套件
- ✅ `generate_all_examples.py` - 自动生成所有示例

### 重构
- 🔄 完全重构数据结构，从单一运镜扩展为镜头序列
- 🔄 模板更新以支持 shots 字段
- 🔄 输出格式统一 API（同一函数支持多种输出）

### 兼容性
- ⚠️ **重大变更** - 段落数据结构变更（增加 shots 字段）
- ⚠️ **重大变更** - Python 脚本 API 变更
- ✅ 向后兼容：仍支持简化模式（自动生成默认镜头序列）

---

## [1.0.0] - �2024-XX-XX

### 初始版本

#### 核心功能
- 🎬头脑风暴引导和需求澄清
- 📋分镜段落结构设计
- 🎬运镜指导和画面布局
- 📝Markdown 格式输出
- 🔗OpenCode 提示词生成
- 💾文件保存确认

#### 参考文档
- 运镜类型参考 (`references/camera-movements.md`)
- 常见叙事模式 (`references/story-patterns.md`)
- 分镜模板 (`assets/storyboard-template.md`)

#### 脚本
- `generate_storyboard.py` - 基础生成脚本（CLI 参数式）

---

## 版本对照

| 版本 | 主要变化 | 备注 |
|------|----------|------|
| 2.0.0 | +画面顺序、+配置化、+CLI、+多格式 | 激进全面重构 |
| 1.0.0 | 基础分镜生成 | 初始版本 |
```

**Step 2: 提交**

```bash
git add CHANGELOG.md
git commit -m "docs: 创建变更日志"
```

---

### Task 8.3: 创建贡献指南

**新建文件：**
- `CONTRIBUTING.md`

**Step 1: 编写贡献指南**

```markdown
# 贡献指南

感谢你考虑为 Video Storyboard Generator 贡献！

## 🤝 如何贡献

### 报告问题

发现问题？请创建 Issue：

1. 描述问题的具体步骤
2. 期望的行为和实际行为的区别
3. 环境信息（Python 版本、操作系统）
4. 相关日志或截图

### 提交代码

#### 开发流程

1. **Fork 仓库**
   ```bash
   git clone https://github.com/your-username/video-storyboard-generator.git
   cd video-storyboard-generator
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **运行测试**
   ```bash
   cd scripts
   python test_full_workflow.py
   ```

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

5. **推送分支**
   ```bash
   git push origin feature/amazing-feature
   ```

6. **创建 Pull Request**

#### 代码规范

- 使用有意义的提交消息（遵循 Conventional Commits）
- 添加必要的注释
- 保持代码简洁清晰
- 更新相关文档

### 文档贡献

文档同样重要！你可以：

- 修正错别字
- 添加使用示例
- 改进说明
- 翻译文档

## 📋 贡献方向

### 优先级高

- [ ] 增加更多视频类型模板
- [ ] 优化镜头序列生成算法
- [ ] 完善测试覆盖

### 欢迎贡献

- [ ] 添加新的运镜类型参考
- [ ] 叙事模式扩展
- [ ] 性能优化
- [ ] 文档改进
- [ ] 示例增加

### 实验性

- [ ] Web UI 界面
- [ ] Remotion 直接集成
- [ ] AI 辅助生成
- [ ] 视频预览功能

## 🔧 开发设置

### 安装依赖

```bash
cd scripts
pip install -r requirements.txt
```

### 运行测试

```bash
cd scripts
python test_full_workflow.py
```

### 生成示例

```bash
cd scripts
python generate_all_examples.py
```

## 📄 许可

提交代码即表示你同意你的代码将在 MIT 许可下发布。

---

再次感谢你的贡献！🎉
```

**Step 2: 提交**

```bash
git add CONTRIBUTING.md
git commit -m "docs: 创建贡献指南"
```

---

## 阶段 9：完成和验证

### Task 9.1: 运行完整测试

**Step 1: 运行所有测试**

```bash
cd scripts
python test_full_workflow.py
```

预期：所有测试通过（5/5）。

**Step 2: 生成所有示例**

```bash
python generate_all_examples.py
```

预期：所有示例文件生成成功。

**Step 3: 测试 CLI 命令**

```bash
python cli.py --help
python cli.py generate --title "测试" --duration 30 --video-type tech_tutorial --format json
```

预期：命令正常执行，输出 JSON 格式。

**Step 4: 验证文件结构**

```bash
# 检查目录结构
tree -L 2
```

预期：包含新增的所有目录和文件。

**Step 5: 检查文档链接**

手动检查 README.md 和 examples/README.md 中的链接是否有效。

**Step 9.2: 最终整理**

**Step 1: 确认所有文件已提交**

```bash
git status
```

确保没有未跟踪的文件。

**Step 2: 创建最终提交（如果需要）**

```bash
git add .
git commit -m "feat: 完成 v2.0.0 激进全面重构"

- 增加画面顺序字段（镜头序列）
- 添加交互式 CLI
- 支持 YAML 配置文件
- 新增 JSON/YAML 导出功能
- 创建完整示例合集
- 增强 README 和文档
- 添加端到端测试
```

**Step 3: 打标签**

```bash
git tag -a v2.0.0 -m "激进全面重构 - 画面顺序 + CLI + 多格式"
git push origin v2.0.0
```

---

## 📊 实施总结

### 完成的任务

#### 阶段 1：核心数据结构升级 ✅
- [x] 扩展段落数据结构，增加 shots 字段
- [x] 更新模板文件支持镜头序列
- [x] 更新 SKILL.md 和参考文档

#### 阶段 2：示例文件夹 ✅
- [x] 创建 examples/ 目录结构
- [x] 生成短视频、中等、长视频示例
- [x] 创建 JSON/YAML 导出示例
- [x] 编写 examples/README.md

#### 阶段 3：配置化 ✅
- [x] 设计配置文件结构
- [x] 创建 default-config.yaml
- [x] 创建 video-types.yaml
- [x] 在 Python 脚本中集成配置文件

#### 阶段 4：交互式 CLI ✅
- [x] 创建基于 Click 的 CLI 应用
- [x] 实现 interactive 命令（向导式）
- [x] 实现 generate 命令（参数式）
- [x] 实现 batch 命令（批量生成）
- [x] 实现导出功能（JSON/YAML）

#### 阶段 5：README 文档 ✅
- [x] 创建主 README.md
- [x] 创建 examples/README.md
- [x] 更新 SKILL.md

#### 阶段 6：运镜参考增强 ✅
- [x] 增加 ASCII 运镜示意图
- [x] 添加镜头序列组合示例

#### 阶段 7：测试和验证 ✅
- [x] 创建端到端测试脚本
- [x] 创建示例生成脚本
- [x] 运行所有测试

#### 阶段 8：最终集成 ✅
- [x] 更新 SKILL.md 完整工作流
- [x] 创建 CHANGELOG.md
- [x] 创建 CONTRIBUTING.md

#### 阶段 9：完成和验证 ✅
- [x] 运行完整测试
- [x] 生成所有示例
- [x] 最终整理

### 新增文件列表

```
video-storyboard-generator/
├── README.md                     [新增] 主文档
├── CHANGELOG.md                  [新增] 变更日志
├── CONTRIBUTING.md               [新增] 贡献指南
├── config/                       [新增] 配置目录
│   ├── default-config.yaml       [新增]
│   └── video-types.yaml          [新增]
├── examples/                     [新增] 示例目录
│   ├── README.md                 [新增]
│   ├── short-video/              [新增]
│   │   └── product-intro-storyboard.md  [新生成]
│   ├── medium-video/             [新增]
│   │   └── microGPT-storyboard.md       [新生成]
│   ├── long-video/               [新增]
│   │   └── guide-tutorial-storyboard.md [新生成]
│   ├── json/                     [新增]
│   │   └── microGPT-storyboard.json     [新生成]
│   └── yaml/                     [新增]
│       └── microGPT-storyboard.yaml     [新生成]
└── scripts/
    ├── cli.py                    [新增] CLI 应用
    ├── export.py                 [新增] 导出模块
    ├── test_full_workflow.py     [新增] 测试脚本
    ├── generate_all_examples.py  [新增] 示例生成
    └── requirements.txt          [新增] 依赖列表
```

### 修改的文件

- SKILL.md - 更新工作流程和文档
- assets/storyboard-template.md - 更新模板支持 shots
- references/camera-movements.md - 增加 ASCII 示意图
- scripts/generate_storyboard.py - 重构支持镜头序列

### 核心改进

1. **画面顺序** - 从单一运镜升级为镜头序列
2. **配置化** - YAML 配置文件支持
3. **交互式 CLI** - 4个命令覆盖所有使用场景
4. **多格式导出** - Markdown / JSON / YAML
5. **完整示例** - 6个示例覆盖不同时长的视频
6. **测试覆盖** - 端到端测试套件

---

## 🎉 版本发布说明

### v2.0.0 - 激进全面重构

**升级亮点：**

- ✨ **新功能：画面顺序字段** - 支持段落内多镜头序列设计
- ⚙️ **新功能：配置化** - YAML 配置文件和视频类型模板
- 💻 **新功能：交互式 CLI** - 向导式、参数式、批量、转换
- 📊 **新功能：多格式导出** - JSON/YAML 支持，便于集成
- 📚 **增强：文档和示例** - README、示例合集、ASCII 示意图

**升级指南：**

1. 安装新依赖：
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

2. 运行测试确保兼容：
   ```bash
   python test_full_workflow.py
   ```

3. 尝试新 CLI：
   ```bash
   python cli.py interactive
   ```

**向后兼容：**

- v1.0.0 的 Markdown 输出格式保持兼容
- 现有用户可直接使用，新功能自动适配

**下一步：**

- 尝试新的交互式生成模式
- 查看新的示例合集
- 配置你的默认视频类型
- 探索 JSON/YAML 集成可能性

---

**Plan Complete!** 🎊

实施计划已保存到 `docs/plans/2024-12-XX-video-storyboard-generator-v2-overhaul.md`

选择执行方式：
1. **Subagent-Driven** - 在当前会话中逐步执行
2. **Parallel Session** - 开启新会话批量执行（推荐，任务量大）

**下一步**：根据你的选择加载对应的执行 skill。
