#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
视频分镜脚本生成器
根据用户提供的信息和头脑风暴结果生成分镜脚本
支持 YAML 配置文件加载
"""

import sys
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# 尝试导入 yaml，如果不可用则提供简化功能
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("警告: PyYAML 未安装，配置文件功能不可用。使用 pip install PyYAML 安装。")

def load_config(config_path: Optional[str] = None) -> Dict:
    """加载配置文件"""
    if not HAS_YAML:
        return {}

    if config_path is None:
        # 默认配置文件路径
        script_dir = Path(__file__).resolve().parent
        config_path = script_dir.parent / "config" / "default-config.yaml"

    config_file = Path(config_path)
    if not config_file.exists():
        return {}

    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}

def load_video_type_config(video_type: str) -> Dict:
    """加载视频类型配置"""
    if not HAS_YAML:
        return {}

    script_dir = Path(__file__).resolve().parent
    config_path = script_dir.parent / "config" / "video-types.yaml"

    config_file = Path(config_path)
    if not config_file.exists():
        return {}

    with open(config_file, 'r', encoding='utf-8') as f:
        all_types = yaml.safe_load(f) or {}
        return all_types.get(video_type, {})


def generate_storyboard_data(
    title: str,
    duration_seconds: Optional[int] = None,
    background_style: Optional[str] = None,
    visual_style: Optional[str] = None,
    main_character: Optional[str] = None,
    narration_style: Optional[str] = None,
    segments: Optional[List[Dict]] = None,
    fps: Optional[int] = None,
    video_type: Optional[str] = None,
    config_path: Optional[str] = None
) -> Dict:
    """生成分镜脚本数据（结构化）- 用于 JSON/YAML 导出"""

    # 加载配置
    config = load_config(config_path)

    # 应用配置值（命令行参数优先）
    duration_seconds = duration_seconds or config.get('video', {}).get('default_duration', 60)
    fps = fps or config.get('video', {}).get('fps', 30)

    # 加载视频类型配置
    if video_type and HAS_YAML:
        type_config = load_video_type_config(video_type)
        # 如果参数未提供，则从视频类型配置中获取
        background_style = background_style or type_config.get('background_style') or type_config.get('visual_style', '')
        visual_style = visual_style or type_config.get('visual_style', '')
        main_character = main_character if main_character is not None else type_config.get('character')
        narration_style = narration_style or type_config.get('narration_style', '')

    # 如果仍然为 None，使用默认值
    background_style = background_style or config.get('visual', {}).get('background_style', "深蓝渐变 + 神经网络线条流动 + 微光粒子")
    visual_style = visual_style or config.get('visual', {}).get('visual_style', "专业风趣（拟人节点表情、气泡调侃）")
    main_character = main_character if main_character is not None else "拟人化AI机器人"
    narration_style = narration_style or config.get('narration', {}).get('style', "成熟中文男声，专业自信 + 偶尔风趣")

    total_frames = duration_seconds * fps

    # 默认段落
    if segments is None:
        if duration_seconds <= 30:
            segments = _generate_short_segments(duration_seconds, title, main_character)
        elif duration_seconds <= 90:
            segments = _generate_medium_segments(duration_seconds, title, main_character)
        else:
            segments = _generate_long_segments(duration_seconds, title, main_character)

    # 生成段落数据（包含镜头序列）
    segments_data = []
    for i, seg in enumerate(segments, 1):
        segment_data = {
            "index": i,
            "title": seg['title'],
            "goal": seg['goal'],
            "start": seg['start'],
            "end": seg['end'],
            "shots": seg.get('shots', []),
            "narration": seg['narration']
        }
        segments_data.append(segment_data)

    data = {
        "title": title,
        "duration_seconds": duration_seconds,
        "total_frames": total_frames,
        "fps": fps,
        "background_style": background_style,
        "visual_style": visual_style,
        "main_character": main_character,
        "narration_style": narration_style,
        "segments": segments_data
    }

    return data

def generate_storyboard(
    title: str,
    duration_seconds: Optional[int] = None,
    background_style: Optional[str] = None,
    visual_style: Optional[str] = None,
    main_character: Optional[str] = None,
    narration_style: Optional[str] = None,
    segments: Optional[List[Dict]] = None,
    fps: Optional[int] = None,
    video_type: Optional[str] = None,
    config_path: Optional[str] = None
) -> str:
    """生成分镜脚本（支持配置文件）"""

    # 加载配置
    config = load_config(config_path)

    # 应用配置值（命令行参数优先）
    duration_seconds = duration_seconds or config.get('video', {}).get('default_duration', 60)
    fps = fps or config.get('video', {}).get('fps', 30)

    # 加载视频类型配置
    if video_type and HAS_YAML:
        type_config = load_video_type_config(video_type)
        # 如果参数未提供，则从视频类型配置中获取
        background_style = background_style or type_config.get('background_style')
        visual_style = visual_style or type_config.get('visual_style')
        main_character = main_character if main_character is not None else type_config.get('character')
        narration_style = narration_style or type_config.get('narration_style')

    # 如果仍然为 None，使用默认值
    background_style = background_style or config.get('visual', {}).get('background_style', "深蓝渐变 + 神经网络线条流动 + 微光粒子")
    visual_style = visual_style or config.get('visual', {}).get('visual_style', "专业风趣（拟人节点表情、气泡调侃）")
    main_character = main_character if main_character is not None else "拟人化AI机器人"
    narration_style = narration_style or config.get('narration', {}).get('style', "成熟中文男声，专业自信 + 偶尔风趣")

    total_frames = duration_seconds * fps

    # 默认段落（仅作为示例，实际应根据主题定制）
    if segments is None:
        if duration_seconds <= 30:
            segments = _generate_short_segments(duration_seconds, title, main_character)
        elif duration_seconds <= 90:
            segments = _generate_medium_segments(duration_seconds, title, main_character)
        else:
            segments = _generate_long_segments(duration_seconds, title, main_character)
    
    # 生成段落内容
    segments_content = "\n\n---\n\n".join([
        _format_segment(seg, i+1) for i, seg in enumerate(segments)
    ])
    
    # 构建分镜脚本
    char_display = main_character if main_character else "无特定角色，抽象图形为主"
    
    # 生成安全文件名
    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in title)
    
    # 生成OpenCode提示词
    opencode_prompt = generate_opencode_prompt(
        title=title,
        duration_seconds=duration_seconds,
        segments=segments,
        background_style=background_style,
        visual_style=visual_style,
        narration_style=narration_style
    )
    
    storyboard = f"""# {title} 讲解视频动画分镜脚本

针对{duration_seconds}秒（{total_frames}帧）版本，每个分镜都明确指定运镜类型、节奏和过渡，确保画面动态、专业不单调。

---

## 视频总体规格

- **时长**：严格{duration_seconds}秒（{total_frames}帧）
- **背景**：{background_style}
- **风格**：{visual_style}
- **主角**：{char_display}
- **旁白**：{narration_style}

---

## 分镜段落设计

{segments_content}

---

## 技术实现提示词

"remotion-best-practices，创建一个严格{duration_seconds}秒（durationInFrames: {total_frames}）的讲解视频。

必须优化：
- 画面紧凑：元素满屏分布，多用grid/flex多列布局，文字/图标放大填充80-90%屏幕，减少任何留白。
- 动画流畅自然：所有过渡用spring()高系数弹簧 + interpolate多关键帧 + easeInOut + stagger子元素延迟，避免任何生硬线性或突然出现。
- 运镜专业动态：严格按分镜运镜描述实现，节奏流畅。

背景{background_style}，主色蓝色，代码高亮专业，{visual_style}，中速电子背景音乐，{narration_style}，自动生成旁白同步字幕。

严格按以上分镜实现。"

---

## OpenCode执行提示词（直接复制使用）

{opencode_prompt}

---

## 文件保存位置

**建议保存位置：** `./docs/{safe_title}_storyboard.md`

**确认保存位置：** 请确认是否将分镜脚本保存在上述位置，或提供其他路径。

---

*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    return storyboard


def generate_opencode_prompt(
    title: str,
    duration_seconds: int,
    segments: List[Dict],
    background_style: str,
    visual_style: str,
    narration_style: str,
    camera_movements: str = "推近、环绕、跟拍、摇移、拉远等",
    rhythm: str = "快而流畅",
    main_color: str = "蓝色",
    fps: int = 30
) -> str:
    """生成可在OpenCode中直接使用的提示词"""

    total_frames = duration_seconds * fps
    duration_minutes = duration_seconds / 60

    # 构建分镜细节（压缩格式）
    segments_text_parts = []
    for seg in segments:
        # 检查是否有镜头序列
        if 'shots' in seg and seg['shots']:
            # 使用镜头序列 - 每个镜头都有独立的运镜描述
            shots_desc = []
            for shot in seg['shots']:
                shot_desc = f"镜头{shot['shot_id']}({shot['time_range']})-{shot['shot_type']}"
                shots_desc.append(shot_desc)
            shots_str = ",".join(shots_desc)

            segment_text = f"段落{seg['title']}（{seg['start']}-{seg['end']}秒）："
            segment_text += f"目标-{seg['goal']}；"
            segment_text += f"镜头序列-{shots_str}；"
            segment_text += f"旁白-{seg['narration']}"
        else:
            # 向后兼容：使用旧格式（单一运镜）
            segment_text = f"段落{seg['title']}（{seg['start']}-{seg['end']}秒）："
            segment_text += f"目标-{seg['goal']}；"
            segment_text += f"运镜-{seg.get('camera', '')}；"
            segment_text += f"布局-{seg.get('layout', '')}；"
            segment_text += f"视觉-{seg.get('visual', '')}；"
            segment_text += f"旁白-{seg['narration']}"

        segments_text_parts.append(segment_text)

    # 将所有段落合并为一个长字符串
    segments_long_text = " | ".join(segments_text_parts)

    # 生成OpenCode提示词
    prompt = f"""remotion，创建一个严格{duration_seconds}秒（durationInFrames: {total_frames}）的{visual_style.replace("（", "").replace("）", "")}视频，总时长控制在{duration_minutes:.1f}分钟以内。

必须优化：
- 画面紧凑：元素满屏分布，多用grid/flex多列布局，文字/图标放大填充80-90%屏幕，减少任何留白。
- 动画流畅自然：所有过渡用spring()高系数弹簧 + interpolate多关键帧 + easeInOut + stagger子元素延迟，避免任何生硬线性或突然出现。
- 运镜专业动态：严格按分镜运镜描述实现（{camera_movements}），节奏{rhythm}，按镜头序列切换画面。

背景{background_style}，主色{main_color}，代码高亮专业，{visual_style}，中速电子背景音乐，{narration_style}，自动生成旁白同步字幕。

严格按以下分镜实现，分镜细节：{segments_long_text}"""

    return prompt


def _generate_short_segments(duration: int, title: str, character: Optional[str]) -> List[Dict]:
    """生成短视频（30秒内）的默认段落（包含镜头序列）"""
    seg_duration = duration // 3
    char_desc = character if character else "主角图标"
    seg2_duration = duration - seg_duration

    return [
        {
            "title": "开场引入",
            "goal": "快速抓住注意力，介绍主题",
            "start": 0,
            "end": seg_duration,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"0-{max(1, seg_duration // 2)}秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": f"从全黑快速 spring dolly in，{char_desc}从底部升起",
                    "layout": f"{char_desc}占屏40%，标题满幅覆盖",
                    "visual": f"标题文字飞入，{char_desc}轻微旋转落地",
                    "transition": "无缝过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{max(1, seg_duration // 2)}-{seg_duration}秒",
                    "shot_type": "环绕 (Orbiting)",
                    "camera": f"环绕展示{char_desc}360°",
                    "layout": f"{char_desc}居中，周围出现关键词气泡",
                    "visual": f"{char_desc}表情变化，气泡逐个出现",
                    "transition": "快速过渡"
                }
            ],
            "narration": f"快速介绍{title}的核心价值！"
        },
        {
            "title": "核心展示",
            "goal": "展示主要内容或效果",
            "start": seg_duration,
            "end": seg_duration * 2,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{seg_duration}-{seg_duration + max(2, seg_duration // 3)}秒",
                    "shot_type": "环绕 (Orbiting)",
                    "camera": "环绕展示核心元素",
                    "layout": "核心元素居中，周围环绕图标",
                    "visual": "关键图形/数据环绕流动",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{seg_duration + max(2, seg_duration // 3)}-{seg_duration * 2}秒",
                    "shot_type": "推近特写 (Close-up)",
                    "camera": "快速推近到重点元素",
                    "layout": "重点元素占屏60%",
                    "visual": "关键数据高亮，特效闪烁",
                    "transition": "快速过渡"
                }
            ],
            "narration": "简明扼要地说明核心要点！"
        },
        {
            "title": "结尾号召",
            "goal": "强化记忆点，引导行动",
            "start": seg_duration * 2,
            "end": duration,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{seg_duration * 2}-{duration - 2}秒",
                    "shot_type": "汇聚 (Converge)",
                    "camera": "所有元素快速汇聚到中央",
                    "layout": "CTA文字居中，其余元素汇聚",
                    "visual": "CTA文字强调显示",
                    "transition": "弹跳过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{duration - 2}-{duration}秒",
                    "shot_type": "拉远 (Dolly Out)",
                    "camera": "快速拉远展示完整信息",
                    "layout": "二维码/链接占屏40%",
                    "visual": "二维码或链接出现",
                    "transition": "快速结束"
                }
            ],
            "narration": "快速总结并给出行动建议！"
        }
    ]


def _generate_medium_segments(duration: int, title: str, character: Optional[str]) -> List[Dict]:
    """生成中等时长视频（30-90秒）的默认段落（包含镜头序列）"""
    char_desc = character if character else "主角图标"

    intro_end = min(12, duration // 5)
    concept_start = intro_end
    concept_end = min(28, duration * 2 // 5)
    detail_start = concept_end
    detail_end = min(44, duration * 3 // 5)
    effect_start = detail_end
    effect_end = min(52, duration * 4 // 5)
    outro_start = effect_end

    return [
        {
            "title": "开场+介绍",
            "goal": "建立兴趣，介绍主题背景",
            "start": 0,
            "end": intro_end,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "0-3秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": f"从全黑快速 spring dolly in，{char_desc}从底部升起",
                    "layout": f"{char_desc}占屏40%，标题满幅覆盖",
                    "visual": f"标题文字从四角stagger飞入汇聚，{char_desc}轻微旋转落地",
                    "transition": "无缝过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"3-{intro_end}秒",
                    "shot_type": "环绕 (Orbiting)",
                    "camera": f"360°环绕展示{char_desc}，背景粒子加速流动",
                    "layout": f"{char_desc}居中，周围环绕关键信息气泡",
                    "visual": f"{char_desc}表情变化，背景粒子动态流动",
                    "transition": "平滑过渡"
                }
            ],
            "narration": f"大家好！今天介绍{title}！"
        },
        {
            "title": "核心概念",
            "goal": "解释核心概念或机制",
            "start": concept_start,
            "end": concept_end,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{concept_start}-{concept_start + 4}秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": "快速 spring dolly in，核心概念图从底部升起",
                    "layout": "概念图占屏50%，周围环绕关键词气泡",
                    "visual": "核心概念文字飞入，关键词从四周stagger出现",
                    "transition": "无缝过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{concept_start + 4}-{concept_end}秒",
                    "shot_type": "环绕 (Orbiting)",
                    "camera": "360°环绕展示概念结构",
                    "layout": "核心概念居中，子概念环绕分布",
                    "visual": "连接线波纹扩散，节点图标旋转",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "核心概念清晰，原理简单优雅！"
        },
        {
            "title": "详细解析",
            "goal": "深入展示细节或效果",
            "start": detail_start,
            "end": detail_end,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{detail_start}-{detail_start + 5}秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": "缓慢推近到结构中心",
                    "layout": "网格布局分层展示，节点满屏分布",
                    "visual": "详细结构逐层展开，代码/动画演示出现",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{detail_start + 5}-{detail_end}秒",
                    "shot_type": "环绕 + 推近 (Orbiting + Dolly In)",
                    "camera": "环绕展示同时缓慢推近，轻摇强调重点",
                    "layout": "逐层放大展示细节",
                    "visual": "关键节点高亮，箭头指示流动方向",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "深入解析内部机制！"
        },
        {
            "title": "效果展示",
            "goal": "展示实际效果或应用场景",
            "start": effect_start,
            "end": effect_end,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{effect_start}-{effect_start + 4}秒",
                    "shot_type": "跟拍 (Tracking Shot)",
                    "camera": "跟拍流程箭头横贯全屏",
                    "layout": "流程箭头从左至右横贯，占屏70%",
                    "visual": "输入→处理→输出的数据流动过程",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{effect_start + 4}-{effect_end}秒",
                    "shot_type": "特写 (Close-up)",
                    "camera": "推近到结果展示区域特写",
                    "layout": "结果展示占屏60%，周围环绕小图标",
                    "visual": "实际效果、数据结果或应用截图，特效闪烁",
                    "transition": "渐隐过渡"
                }
            ],
            "narration": "实际效果显著，应用场景广泛！"
        },
        {
            "title": "结尾号召",
            "goal": "总结并引导行动",
            "start": outro_start,
            "end": duration,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{outro_start}-{duration - 3}秒",
                    "shot_type": "汇聚 (Converge)",
                    "camera": "所有元素 spring converge 到中央",
                    "layout": "元素从四周汇聚到中央",
                    "visual": "总结文字、CTA文字出现",
                    "transition": "弹跳过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{duration - 3}-{duration}秒",
                    "shot_type": "拉远 (Dolly Out)",
                    "camera": "缓慢 dolly out 展示全景",
                    "layout": "CTA按钮/二维码居中，背景元素扩散",
                    "visual": "CTA按钮或二维码，背景淡化出现关键信息",
                    "transition": "渐隐结束"
                }
            ],
            "narration": "这就是核心要点，快去实践体验吧！"
        }
    ]


def _generate_long_segments(duration: int, title: str, character: Optional[str]) -> List[Dict]:
    """生成长视频（90秒以上）的默认段落（包含镜头序列）"""
    char_desc = character if character else "主角图标"

    # 长视频通常有更多段子，这里保持7个段落，每个段落2-3个镜头
    return [
        {
            "title": "开场引入",
            "goal": "建立情境，引发兴趣",
            "start": 0,
            "end": 15,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "0-5秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": f"快速推近到{char_desc}出现",
                    "layout": f"{char_desc}从底部升起，占屏50%",
                    "visual": f"{char_desc}戏剧性登场，背景充满张力",
                    "transition": "无缝过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": "5-15秒",
                    "shot_type": "环绕 (Orbiting)",
                    "camera": f"环绕展示{char_desc}和环境",
                    "layout": f"{char_desc}居中，背景场景展开",
                    "visual": f"{char_desc}表情生动，引人注目的视觉效果",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "引人入胜的开场白！"
        },
        {
            "title": "问题背景",
            "goal": "说明问题背景或现状",
            "start": 15,
            "end": 35,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "15-25秒",
                    "shot_type": "摇移 (Pan)",
                    "camera": "从左到右摇移展示问题场景",
                    "layout": "问题场景占屏80%",
                    "visual": "问题场景逐步展开，数据图表出现",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": "25-35秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": "推近到关键数据展示",
                    "layout": "关键数据图表占屏60%",
                    "visual": "数据图表动态展示，关键指标高亮",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "详细说明问题背景！"
        },
        {
            "title": "核心内容1",
            "goal": "第一部分核心内容",
            "start": 35,
            "end": 65,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "35-45秒",
                    "shot_type": "推近 (Dolly In)",
                    "camera": "深入推近到核心结构",
                    "layout": "核心图形占屏60%，周围环绕文字说明",
                    "visual": "核心图形逐层出现，文字说明同步",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": "45-55秒",
                    "shot_type": "环绕 + 推近 (Orbiting + Dolly In)",
                    "camera": "环绕展示同时逐渐推近",
                    "layout": "结构分层展示，箭头指示",
                    "visual": "动画演示逻辑流程",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 3,
                    "time_range": "55-65秒",
                    "shot_type": "特写 (Close-up)",
                    "camera": "特写关键部分",
                    "layout": "关键细节占屏70%",
                    "visual": "高亮显示关键细节",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "详细讲解第一部分！"
        },
        {
            "title": "核心内容2",
            "goal": "第二部分核心内容",
            "start": 65,
            "end": 95,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "65-75秒",
                    "shot_type": "对比展示",
                    "camera": "分屏或并列展示两种状态",
                    "layout": "左右对比或上下对比",
                    "visual": "两种情况并列展示，差异高亮",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": "75-95秒",
                    "shot_type": "推近强调",
                    "camera": "推近到优势部分",
                    "layout": "优势部分占屏60%",
                    "visual": "高亮优势细节",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "继续深入第二部分！"
        },
        {
            "title": "应用案例",
            "goal": "展示实际应用或案例",
            "start": 95,
            "end": 120,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "95-105秒",
                    "shot_type": "场景切换",
                    "camera": "切换到应用场景",
                    "layout": "应用截图占屏80%",
                    "visual": "实际应用界面展示",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": "105-120秒",
                    "shot_type": "跟拍 (Tracking Shot)",
                    "camera": "跟随操作流程",
                    "layout": "流程横贯全屏",
                    "visual": "操作步骤逐个出现",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "看看实际应用效果！"
        },
        {
            "title": "总结回顾",
            "goal": "总结要点，强化记忆",
            "start": 120,
            "end": duration - 10,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": "120-135秒",
                    "shot_type": "拉远 (Dolly Out)",
                    "camera": "从近景到全景回顾",
                    "layout": "要点列表占屏60%",
                    "visual": "要点逐个出现并高亮",
                    "transition": "平滑过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"135-{duration - 10}秒",
                    "shot_type": "环绕 (Orbiting)",
                    "camera": "环绕展示所有要点",
                    "layout": "要点环绕分布",
                    "visual": "所有要点同时显示",
                    "transition": "平滑过渡"
                }
            ],
            "narration": "回顾今天的核心要点！"
        },
        {
            "title": "结尾号召",
            "goal": "引导下一步行动",
            "start": duration - 10,
            "end": duration,
            "shots": [
                {
                    "shot_id": 1,
                    "time_range": f"{duration - 10}-{duration - 2}秒",
                    "shot_type": "汇聚 (Converge)",
                    "camera": "所有元素汇聚到中央",
                    "layout": "CTA居中",
                    "visual": "行动指引文字出现",
                    "transition": "弹跳过渡"
                },
                {
                    "shot_id": 2,
                    "time_range": f"{duration - 2}-{duration}秒",
                    "shot_type": "定格",
                    "camera": "最后定格在CTA",
                    "layout": "二维码/链接",
                    "visual": "二维码和联系信息",
                    "transition": "定格结束"
                }
            ],
            "narration": "现在就开始行动吧！"
        }
    ]


def _format_segment(seg: Dict, index: int) -> str:
    """格式化单个段落（支持多镜头序列）"""

    # 检查是否有镜头序列（shots 字段），如果没有则使用旧格式向后兼容
    if 'shots' in seg and seg['shots']:
        # 构建镜头序列
        shots_content = []
        for shot in seg.get('shots', []):
            shot_text = f"""#### 镜头{shot['shot_id']}：{shot['shot_type']}（{shot['time_range']}）

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
    else:
        # 向后兼容：旧格式（单一运镜）
        return f"""### 段落{index}：{seg['title']}（{seg['start']}-{seg['end']}秒）

**段落目标**：{seg['goal']}

-> 运镜：{seg['camera']}

-> 画面布局：{seg['layout']}

-> 视觉元素：{seg['visual']}

-> 旁白：\"{seg['narration']}\"\" """


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python generate_storyboard.py <标题> [时长(秒)]")
        print("示例: python generate_storyboard.py 'MicroGPT原理' 60")
        print("\n提示：这是基础生成器。如需定制化分镜，")
        print("请先进行头脑风暴确定具体需求。")
        sys.exit(1)
    
    title = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    
    storyboard = generate_storyboard(
        title=title,
        duration_seconds=duration
    )
    
    # 输出到文件
    safe_title = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in title)
    filename = f"{safe_title}_storyboard.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(storyboard)
    
    print(f"分镜脚本已生成: {filename}")
    print(f"\n提示：这是基于默认模板的生成结果。")
    print(f"如需定制化分镜，请先进行头脑风暴确定具体需求。")


if __name__ == "__main__":
    main()
