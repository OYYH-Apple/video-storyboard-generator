#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Video Storyboard Generator CLI 应用"""

import sys
import os
from pathlib import Path

# 设置 Windows 控制台输出为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 尝试导入 click
try:
    import click
    HAS_CLICK = True
except ImportError:
    HAS_CLICK = False
    print("错误: Click 未安装。请运行: pip install click")
    sys.exit(1)

# 尝试导入 yaml
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# 导入本地模块
from generate_storyboard import generate_storyboard, load_video_type_config
from export import export_to_json, export_to_yaml, parse_markdown_to_dict

@click.group()
def cli():
    """Video Storyboard Generator - 分镜脚本生成器"""
    pass

@cli.command()
@click.option('--title', '-t', prompt=True, help='视频标题')
@click.option('--duration', '-d', default=60, help='视频时长（秒）')
@click.option('--video-type', '-v', type=click.Choice(['tech_tutorial', 'product_promo', 'story_telling', 'data_insight'], case_sensitive=True),
              help='视频类型')
@click.option('--config', '-c', help='配置文件路径')
@click.option('--output', '-o', help='输出文件路径')
@click.option('--format', '-f', type=click.Choice(['markdown', 'json', 'yaml'], case_sensitive=True), default='markdown',
              help='输出格式')
def generate(title, duration, video_type, config, output, format):
    """生成分镜脚本（命令行模式）"""
    click.echo(f"\n[任务] 正在生成分镜脚本...")
    click.echo(f"标题: {title}")
    click.echo(f"时长: {duration}秒")

    # 如果未指定视频类型，询问
    if not video_type and HAS_YAML:
        video_types = list(yaml.safe_load(
            open(Path(__file__).parent.parent / 'config' / 'video-types.yaml', 'r', encoding='utf-8')
        ).keys())
        video_type = click.prompt(
            '选择视频类型',
            type=click.Choice(video_types),
            show_choices=True,
            default='tech_tutorial'
        )

    # 其他交互式询问
    character = click.confirm('需要拟人化角色吗？', default=True)
    if not character:
        main_character = None
    else:
        main_character = click.prompt('角色描述（留空使用默认）', default='')
        if not main_character:
            main_character = '拟人化AI机器人'

    # 生成脚本
    if format == 'json':
        # 需要先生成结构化数据，然后导出
        from generate_storyboard import generate_storyboard_data
        data = generate_storyboard_data(
            title=title,
            duration_seconds=duration,
            video_type=video_type,
            config_path=config,
            main_character=main_character
        )
        storyboard = export_to_json(data)
    elif format == 'yaml':
        from generate_storyboard import generate_storyboard_data
        if not HAS_YAML:
            click.echo("错误: YAML 导出需要 PyYAML。请运行: pip install PyYAML")
            return
        data = generate_storyboard_data(
            title=title,
            duration_seconds=duration,
            video_type=video_type,
            config_path=config,
            main_character=main_character
        )
        storyboard = export_to_yaml(data)
    else:
        storyboard = generate_storyboard(
            title=title,
            duration_seconds=duration,
            video_type=video_type,
            config_path=config,
            main_character=main_character,
            output_format='markdown'
        )

    # 确定输出路径
    if not output:
        import re
        safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
        ext = {'markdown': 'md', 'json': 'json', 'yaml': 'yaml'}[format]
        output = f"./docs/{safe_title}_storyboard.{ext}"

    # 确认保存
    click.echo(f"\n[输出] 路径: {output}")
    if click.confirm('确认保存吗？'):
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        with open(output, 'w', encoding='utf-8') as f:
            f.write(storyboard)
        click.echo(f"[成功] 分镜脚本已保存到: {output}")
    else:
        click.echo("[取消] 已取消保存")

@cli.command()
def interactive():
    """完全交互式生成（向导模式）"""
    click.echo("\n" + "="*50)
    click.echo("  视频分镜脚本生成向导")
    click.echo("="*50 + "\n")

    # 步骤1: 基本信息
    click.echo("[步骤 1/5] 基本信息")
    title = click.prompt('视频标题', type=str)
    duration = click.prompt('视频时长（秒）', type=int, default=60)

    # 步骤2: 视频类型
    click.echo("\n[步骤 2/5] 视频类型")
    if HAS_YAML:
        video_types = list(yaml.safe_load(
            open(Path(__file__).parent.parent / 'config' / 'video-types.yaml', 'r', encoding='utf-8')
        ).keys())
        video_type = click.prompt('选择视频类型', type=click.Choice(video_types, case_sensitive=True), default='tech_tutorial')
    else:
        click.echo("提示: PyYAML 未安装，使用默认技术教程类型。运行: pip install PyYAML")
        video_type = 'tech_tutorial'

    # 步骤3: 视觉设置
    click.echo("\n[步骤 3/5] 视觉设置")
    use_character = click.confirm('需要拟人化角色吗？', default=True)
    main_character = None
    if use_character:
        main_character = click.prompt('角色描述（留空使用默认）', default='', show_default=False)
        if not main_character:
            main_character = '拟人化AI机器人'

    # 步骤4: 输出设置
    click.echo("\n[步骤 4/5] 输出设置")
    click.echo("  1. Markdown (.md) - 易于阅读和编辑")
    click.echo("  2. JSON (.json) - 机器可读，便于集成")
    click.echo("  3. YAML (.yaml) - 可读性强的配置格式")
    format_choice = click.prompt('输出格式', type=click.Choice(['1', '2', '3']), default='1')
    format_map = {'1': 'markdown', '2': 'json', '3': 'yaml'}
    output_format = format_map[format_choice]

    # 步骤5: 确认
    click.echo("\n[步骤 5/5] 确认信息")
    click.echo(f"  标题: {title}")
    click.echo(f"  时长: {duration}秒")
    click.echo(f"  类型: {video_type}")
    click.echo(f"  角色: {main_character if main_character else '无'}")
    click.echo(f"  格式: {output_format}")

    if not click.confirm('\n[确认] 生成吗？'):
        click.echo("[取消] 已取消")
        return

    # 生成并保存
    click.echo("\n[任务] 正在生成分镜脚本...")
    if output_format == 'json':
        from generate_storyboard import generate_storyboard_data
        data = generate_storyboard_data(
            title=title,
            duration_seconds=duration,
            video_type=video_type,
            main_character=main_character
        )
        storyboard = export_to_json(data)
    elif output_format == 'yaml':
        from generate_storyboard import generate_storyboard_data
        if not HAS_YAML:
            click.echo("错误: YAML 导出需要 PyYAML。请运行: pip install PyYAML")
            click.echo("[降级] 改用 Markdown 格式")
            output_format = 'markdown'
            storyboard = generate_storyboard(
                title=title,
                duration_seconds=duration,
                video_type=video_type,
                main_character=main_character,
                output_format='markdown'
            )
        else:
            data = generate_storyboard_data(
                title=title,
                duration_seconds=duration,
                video_type=video_type,
                main_character=main_character
            )
            storyboard = export_to_yaml(data)
    else:
        storyboard = generate_storyboard(
            title=title,
            duration_seconds=duration,
            video_type=video_type,
            main_character=main_character,
            output_format='markdown'
        )

    import re
    safe_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
    ext = {'markdown': 'md', 'json': 'json', 'yaml': 'yaml'}[output_format]
    output_path = f"./docs/{safe_title}_storyboard.{ext}"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(storyboard)

    click.echo(f"\n[成功] 分镜脚本已保存到: {output_path}")
    click.echo(f"\n[提示] 可以编辑该文件进行微调，或使用模板进行定制化设计")

@cli.command()
@click.argument('config_file', type=click.Path(exists=True))
def batch(config_file):
    """批量生成（从配置文件）"""
    if not HAS_YAML:
        click.echo("错误: 批量生成需要 PyYAML。请运行: pip install PyYAML")
        return

    with open(config_file, 'r', encoding='utf-8') as f:
        configs = yaml.safe_load(f)

    click.echo(f"\n[任务] 批量生成 {len(configs)} 个视频分镜...")

    for i, cfg in enumerate(configs, 1):
        click.echo(f"\n[{i}/{len(configs)}] 生成: {cfg.get('title', 'Untitled')}")

        storyboard = generate_storyboard(**cfg)

        import re
        safe_title = re.sub(r'[^\w\s-]', '', cfg.get('title', 'Untitled')).strip().replace(' ', '_')
        output_path = f"./docs/{safe_title}_storyboard.md"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(storyboard)

        click.echo(f"  [OK] 已保存: {output_path}")

    click.echo("\n" + "="*50)
    click.echo(f"[成功] 批量生成完成！共 {len(configs)} 个文件")
    click.echo("="*50)

@cli.command()
@click.option('--input', '-i', required=True, help='输入 Markdown 文件路径')
@click.option('--format', '-f', type=click.Choice(['json', 'yaml'], case_sensitive=True), required=True, help='输出格式')
@click.option('--output', '-o', help='输出文件路径（默认：同名文件）')
def convert(input, format, output):
    """转换已有 Markdown 分镜为 JSON/YAML"""
    with open(input, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    data = parse_markdown_to_dict(markdown_content)

    if format == 'json':
        result = export_to_json(data)
        default_output = input.replace('.md', '.json')
    else:
        if not HAS_YAML:
            click.echo("错误: YAML 导出需要 PyYAML。请运行: pip install PyYAML")
            return
        result = export_to_yaml(data)
        default_output = input.replace('.md', '.yaml')

    if not output:
        output = default_output

    with open(output, 'w', encoding='utf-8') as f:
        f.write(result)

    click.echo(f"[成功] 已转换: {input} -> {output}")

if __name__ == '__main__':
    cli()
