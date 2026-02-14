#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""导出功能模块 - JSON/YAML 格式支持"""

import json
from typing import Dict
from datetime import datetime

# 尝试导入 yaml，如果不可用则提供简化功能
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    print("警告: PyYAML 未安装，YAML 导出功能不可用。使用 pip install PyYAML 安装。")

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

    if include_opencode_prompt and "opencode_prompt" in storyboard:
        data["opencode_prompt"] = storyboard["opencode_prompt"]

    return json.dumps(data, ensure_ascii=False, indent=2)

def export_to_yaml(storyboard: Dict, include_opencode_prompt: bool = True) -> str:
    """导出为 YAML 格式"""
    if not HAS_YAML:
        raise ImportError("PyYAML 未安装，无法导出 YAML 格式")

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

    if include_opencode_prompt and "opencode_prompt" in storyboard:
        data["opencode_prompt"] = storyboard["opencode_prompt"]

    return yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)

def parse_markdown_to_dict(markdown_content: str) -> Dict:
    """将 Markdown 分镜脚本解析为字典（用于从已有 MD 导出 JSON/YAML）"""
    lines = markdown_content.split('\n')
    result = {
        "metadata": {
            "title": "未命名",
            "version": "1.0",
            "generated_at": datetime.now().isoformat()
        },
        "video_specs": {
            "background": "默认背景",
            "visual_style": "默认风格",
            "character": "默认角色",
            "narration": "默认旁白",
            "fps": 30
        },
        "segments": [],
        "duration_seconds": 60,
        "total_frames": 1800
    }

    current_segment = None
    current_shots = []

    for i, line in enumerate(lines):
        # 解析标题
        if line.startswith('# ') and '讲解' in line:
            result["metadata"]["title"] = line.replace('# ', '').replace(' 讲解视频动画分镜脚本', '')
        
        # 解析总体规格
        if '- **时长**：严格' in line:
            # 提取时长和帧数
            parts = line.split('（')[1].split('）')[0].split('（')[1].split('）')[0]
            if '秒' in parts:
                duration_str = parts.split('秒')[0]
                try:
                    result["duration_seconds"] = int(duration_str)
                except:
                    pass
        
        if '- **背景**：' in line:
            result["video_specs"]["background"] = line.split('：', 1)[1].strip()
        
        if '- **风格**：' in line:
            result["video_specs"]["visual_style"] = line.split('：', 1)[1].strip()
        
        if '- **主角**：' in line:
            result["video_specs"]["character"] = line.split('：', 1)[1].strip()
        
        if '- **旁白**：' in line:
            result["video_specs"]["narration"] = line.split('：', 1)[1].strip()
        
        # 解析段落
        if line.startswith('### 段落'):
            # 保存前一个段落
            if current_segment:
                current_segment["shots"] = current_shots if current_shots else []
                result["segments"].append(current_segment)
            
            # 开始新段落
            current_segment = {
                "title": "",
                "goal": "",
                "start": 0,
                "end": 0,
                "narration": ""
            }
            current_shots = []
        
        # 解析段落标题和目标
        if '段落目标**：' in line:
            current_segment["goal"] = line.split('：', 1)[1].strip()
        
        # 解析镜头
        if line.startswith('#### 镜头'):
            shot = {
                "shot_id": len(current_shots) + 1,
                "time_range": "",
                "shot_type": "",
                "camera": "",
                "layout": "",
                "visual": "",
                "transition": ""
            }
            current_shots.append(shot)
        
        # 解析镜头细节
        if '- **运镜**：' in line and current_shots:
            current_shots[-1]["camera"] = line.split('：', 1)[1].strip()
        
        if '- **布局**：' in line and current_shots:
            current_shots[-1]["layout"] = line.split('：', 1)[1].strip()
        
        if '- **视觉**：' in line and current_shots:
            current_shots[-1]["visual"] = line.split('：', 1)[1].strip()
        
        if '- **过渡**：' in line and current_shots:
            current_shots[-1]["transition"] = line.split('：', 1)[1].strip()
        
        # 解析旁白
        if '**旁白**：' in line or '旁白**："' in line:
            if current_segment:
                narr = line.split('："', 1)[1].rstrip('"') if '"' in line else line.split('：', 1)[1]
                current_segment["narration"] = narr.strip()

    # 保存最后一个段落
    if current_segment:
        current_segment["shots"] = current_shots if current_shots else []
        result["segments"].append(current_segment)
    
    # 更新总帧数
    result["total_frames"] = result["duration_seconds"] * result["video_specs"]["fps"]

    return result
