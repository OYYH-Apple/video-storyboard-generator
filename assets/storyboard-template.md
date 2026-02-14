# {{TITLE}} 讲解视频动画分镜脚本

{{VERSION_INFO}}

---

## 视频总体规格

- **时长**：严格{{DURATION}}秒（{{FRAMES}}帧）
- **背景**：{{BACKGROUND_STYLE}}
- **风格**：{{VISUAL_STYLE}}
- **主角**：{{MAIN_CHARACTER}}
- **旁白**：{{NARRATION_STYLE}}

---

## 分镜段落设计

{{SEGMENTS}}

---

## 技术实现提示词

"{{TECH_PROMPT_PREFIX}}，创建一个严格{{DURATION}}秒（durationInFrames: {{FRAMES}}）的{{VIDEO_TYPE}}视频，总时长控制在{{DURATION}}秒以内。

必须优化：
- 画面紧凑：元素满屏分布，多用grid/flex多列布局，文字/图标放大填充80-90%屏幕，减少任何留白。
- 动画流畅自然：所有过渡用spring()高系数弹簧 + interpolate多关键帧 + easeInOut + stagger子元素延迟，避免任何生硬线性或突然出现。
- 运镜专业动态：严格按分镜运镜描述实现（{{CAMERA_MOVEMENTS}}），节奏{{RHYTHM}}。

{{VISUAL_SPECS}}

严格按以下分镜实现，分镜细节：

[上面的分镜脚本]"

---

## 变量说明

生成时替换以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| {{TITLE}} | 视频主题标题 | "MicroGPT原理讲解" |
| {{VERSION_INFO}} | 版本说明 | "针对1分钟版本的运镜设计..." |
| {{DURATION}} | 总时长（秒） | 60 |
| {{FRAMES}} | 总帧数 | 1800 |
| {{BACKGROUND_STYLE}} | 背景描述 | "深蓝渐变+神经网络线条流动+微光粒子" |
| {{VISUAL_STYLE}} | 视觉风格 | "专业风趣（拟人节点表情、气泡调侃）" |
| {{MAIN_CHARACTER}} | 主角/吉祥物 | "拟人化AI机器人" |
| {{NARRATION_STYLE}} | 旁白风格 | "成熟中文男声，专业自信+偶尔风趣" |
| {{SEGMENTS}} | 分镜段落内容 | 多个段落的具体描述 |
| {{SHOTS_SEQUENCE}} | 镜头序列内容 | 多个镜头的详细描述 |
| {{TECH_PROMPT_PREFIX}} | 技术提示前缀 | "remotion-best-practices" |
| {{VIDEO_TYPE}} | 视频类型 | "专业风趣教学" |
| {{CAMERA_MOVEMENTS}} | 运镜类型列表 | "推近、环绕、跟拍、摇移、拉远" |
| {{RHYTHM}} | 节奏描述 | "快而流畅" |
| {{VISUAL_SPECS}} | 视觉规范详情 | 颜色、字体、动画等详细规范 |
| {{SHOT_TYPE}} | 镜头类型 | "推近 (Dolly In)" |
| {{SHOT_TIME_RANGE}} | 镜头时间范围 | "0-3秒" |
| {{SHOT_TRANSITION}} | 过渡方式 | "无缝过渡" |
| {{CAMERA_MOVEMENT}} | 单个镜头运镜描述 | "快速 spring dolly in" |
| {{SHOT_LAYOUT}} | 单个镜头布局 | "主角占屏40%，标题满幅" |
| {{SHOT_VISUAL}} | 单个镜头视觉元素 | "标题文字飞入" |

---

## 段落模板

### 段落X：{{SEGMENT_TITLE}}（{{START_TIME}}-{{END_TIME}}秒）

**段落目标**：{{SEGMENT_GOAL}}

**画面顺序**：
{{SHOTS_SEQUENCE}}

**旁白**："{{NARRATION_CONTENT}}"

---

## 镜头模板

### 镜头Y：{{SHOT_TITLE}}/{{SHOT_TYPE}}（{{SHOT_TIME_RANGE}}）

- **运镜**：{{CAMERA_MOVEMENT}}
- **布局**：{{SHOT_LAYOUT}}
- **视觉**：{{SHOT_VISUAL}}
- **过渡**：{{SHOT_TRANSITION}}

---

## 头脑风暴清单（生成前确认）

- [ ] 主题内容明确了吗？
- [ ] 目标受众是谁？
- [ ] 核心信息是什么？
- [ ] 视频时长确定了吗？
- [ ] 视觉风格选好了吗？
- [ ] 需要主角/吉祥物吗？
- [ ] 旁白风格确定了吗？
- [ ] 运镜节奏偏好？
- [ ] 段落结构根据主题设计好了吗？
