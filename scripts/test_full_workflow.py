#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端工作流测试脚本"""

import sys
from pathlib import Path

# 设置 Windows 控制台输出为 UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加 scripts 目录到 Python 路径
scripts_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from generate_storyboard import generate_storyboard

def test_markdown_generation():
    """测试 Markdown 生成"""
    print("\n[测试 1/4] Markdown 生成...")
    result = generate_storyboard(
        title="测试视频",
        duration_seconds=60,
        background_style="深蓝渐变 + 神经网络线条流动 + 微光粒子",
        visual_style="专业风趣（拟人节点表情、气泡调侃）",
        main_character="拟人化AI机器人",
        narration_style="成熟中文男声，专业自信+偶尔风趣"
    )

    assert "测试视频" in result, "标题未正确生成"
    assert "分镜段落设计" in result, "段落设计未正确生成"
    assert "画面顺序" in result, "画面顺序字段缺失"
    print("   [通过] Markdown 生成测试通过")
    return result

def test_shot_structure():
    """测试镜头序列结构"""
    print("\n[测试 2/4] 镜头序列结构...")

    result = generate_storyboard(
        title="测试视频",
        duration_seconds=60
    )

    # 检查镜头序列标记
    has_shots = "镜头1" in result or "镜头 1" in result
    assert has_shots, "镜头序列标记未找到"

    # 检查至少一个镜头有过渡描述
    has_transition = "过渡" in result
    assert has_transition, "过渡描述缺失"

    print("   [通过] 镜头序列结构测试通过")
    return result

def test_multiple_durations():
    """测试不同时长的视频生成"""
    print("\n[测试 3/4] 不同时长视频生成...")

    durations = [30, 60, 120]
    for duration in durations:
        result = generate_storyboard(
            title=f"测试视频{duration}秒",
            duration_seconds=duration
        )
        assert f"{duration}秒" in result, f"{duration}秒视频时长未正确显示"
        print(f"   [通过] {duration}秒视频生成成功")

def test_file_generation_and_save():
    """测试文件生成和保存"""
    print("\n[测试 4/4] 文件生成和保存...")

    # 生成测试内容
    title = "测试输出文件"
    result = generate_storyboard(
        title=title,
        duration_seconds=60
    )

    # 写入临时文件
    test_dir = Path(__file__).parent / "test_output"
    test_dir.mkdir(exist_ok=True)

    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in title)
    test_file = test_dir / f"{safe_title}_storyboard.md"

    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(result)

    # 验证文件存在且内容正确
    assert test_file.exists(), "测试文件未创建"
    content = test_file.read_text(encoding='utf-8')
    assert title in content, "文件内容不正确"
    assert "画面顺序" in content, "画面顺序字段缺失"

    print(f"   [通过] 文件生成和保存测试通过: {test_file}")
    return test_file

def run_all_tests():
    """运行所有测试"""
    print("="*60)
    print("  Video Storyboard Generator - 端到端测试")
    print("="*60)

    tests = [
        test_markdown_generation,
        test_shot_structure,
        test_multiple_durations,
        test_file_generation_and_save
    ]

    failed = []

    for test in tests:
        try:
            result = test()
        except Exception as e:
            print(f"   [失败] {test.__name__}: {e}")
            failed.append(test.__name__)

    print("\n" + "="*60)
    if failed:
        print(f"[失败] 测试失败: {len(failed)}/{len(tests)}")
        for name in failed:
            print(f"   - {name}")
        print("="*60)
        return False
    else:
        print(f"[成功] 所有测试通过: {len(tests)}/{len(tests)}")
        print("="*60)
        return True

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
