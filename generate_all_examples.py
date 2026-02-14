#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成所有示例文件"""

import sys
import os
from pathlib import Path

# 设置 Windows 控制台输出为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加 scripts 目录到 Python 路径
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate_storyboard import generate_storyboard

def generate_examples():
    """生成所有示例文件"""

    examples_dir = Path(__file__).parent / "examples"

    # 1. 短视频示例 (30秒)
    print("\n[1/4] 生成短视频示例...")
    short_video = generate_storyboard(
        title="产品快速介绍",
        duration_seconds=30,
        background_style="明亮色彩 + 卡通元素 + 活泼背景粒子",
        visual_style="活泼轻松（明亮色彩+卡通元素）",
        main_character="产品吉祥物",
        narration_style="风趣调侃型，快速节奏"
    )
    (examples_dir / "short-video" / "product-intro-storyboard.md").write_text(
        short_video, encoding='utf-8'
    )
    print("   [OK] product-intro-storyboard.md")

    # 2. 中等视频示例 (60秒)
    print("\n[2/4] 生成中等视频示例...")
    medium_video = generate_storyboard(
        title="MicroGPT 原理讲解",
        duration_seconds=60,
        background_style="深蓝渐变 + 神经网络线条流动 + 微光粒子",
        visual_style="专业风趣（拟人节点表情、气泡调侃）",
        main_character="拟人化AI机器人",
        narration_style="成熟中文男声，专业自信+偶尔风趣"
    )
    (examples_dir / "medium-video" / "microGPT-storyboard.md").write_text(
        medium_video, encoding='utf-8'
    )
    print("   [OK] microGPT-storyboard.md")

    # 3. 长视频示例 (180秒/3分钟)
    print("\n[3/4] 生成长视频示例...")
    long_video = generate_storyboard(
        title="完整教学教程：AI模型训练基础",
        duration_seconds=180,
        background_style="温暖柔和渐变 + 情感化元素",
        visual_style="温暖柔和（渐变色彩+情感化）",
        main_character="角色人物小导师",
        narration_style="亲和教学型，耐心细致"
    )
    (examples_dir / "long-video" / "guide-tutorial-storyboard.md").write_text(
        long_video, encoding='utf-8'
    )
    print("   [OK] guide-tutorial-storyboard.md")

    # 4. 技术视频示例 (90秒) - 补充一个中等长度技术视频
    print("\n[4/4] 生成技术视频示例...")
    tech_video = generate_storyboard(
        title="神经网络可视化演示",
        duration_seconds=90,
        background_style="深蓝科技背景 + 电路板线条 + 数据流动",
        visual_style="严肃专业（简洁+数据可视化）",
        main_character=None,  # 无角色，抽象图形为主
        narration_style="专业权威型，冷静客观"
    )
    (examples_dir / "medium-video" / "neural-network-demo.md").write_text(
        tech_video, encoding='utf-8'
    )
    print("   [OK] neural-network-demo.md")

    print("\n" + "="*50)
    print("[SUCCESS] 所有示例生成完成！")
    print("="*50)

if __name__ == "__main__":
    generate_examples()

if __name__ == "__main__":
    generate_examples()
