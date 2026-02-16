# {{TITLE}} 视频分镜脚本

{{VERSION_INFO}}

---

## 视频总体规格

- **视频类型**：{{VIDEO_TYPE}}
- **时长**：严格{{DURATION}}秒（{{FRAMES}}帧）
- **背景**：{{BACKGROUND_STYLE}}
- **风格**：{{VISUAL_STYLE}}
- **主角**：{{MAIN_CHARACTER}}
- **旁白**：{{NARRATION_STYLE}}

---

## 用户画像参考

本次生成参考了用户的偏好设置：
- 偏好风格：{{USER_PREFERRED_STYLE}}
- 偏好节奏：{{USER_PREFERRED_RHYTHM}}

---

## 分镜段落设计

{{SEGMENTS}}

---

## 镜头拆分说明

**镜头时长规则**：所有镜头时长均不超过{{SHOT_TIME_LIMIT}}秒（可自定义），确保视觉节奏紧凑。

| 段落 | 原始时长 | 拆分镜头数 | 单镜头时长 |
|------|---------|-----------|-----------|
{{SHOT_BREAKDOWN_TABLE}}

---

## 技术实现提示词

"{{TECH_PROMPT_PREFIX}}，创建一个严格{{DURATION}}秒（durationInFrames: {{FRAMES}}）的{{VIDEO_TYPE}}视频，总时长控制在{{DURATION}}秒以内。

必须优化：
- 画面紧凑：元素满屏分布，多用grid/flex多列布局，文字/图标放大填充80-90%屏幕，减少任何留白。
- 动画流畅自然：所有过渡用spring()高系数弹簧 + interpolate多关键帧 + easeInOut + stagger子元素延迟，避免任何生硬线性或突然出现。
- 运镜专业动态：严格按分镜运镜描述实现（{{CAMERA_MOVEMENTS}}），节奏{{RHYTHM}}。
- 镜头时长：单个镜头不超过{{SHOT_TIME_LIMIT}}秒，超过则拆分为多个镜头。

{{VISUAL_SPECS}}

严格按以下分镜实现，分镜细节：

[上面的分镜脚本]"

---

## 变量说明

生成时替换以下变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| {{TITLE}} | 视频主题标题 | "MicroGPT原理讲解" |
| {{VIDEO_TYPE}} | 视频类型 | concept_teaching / book_intro / hot_comment / story_board / product_intro / data_report / tutorial |
| {{VERSION_INFO}} | 版本说明 | "针对1分钟版本的运镜设计..." |
| {{DURATION}} | 总时长（秒） | 60 |
| {{FRAMES}} | 总帧数 | 1800 |
| {{BACKGROUND_STYLE}} | 背景描述 | "深蓝渐变+神经网络线条流动+微光粒子" |
| {{VISUAL_STYLE}} | 视觉风格 | "专业风趣（拟人节点表情、气泡调侃）" |
| {{MAIN_CHARACTER}} | 主角/吉祥物 | "拟人化AI机器人" |
| {{NARRATION_STYLE}} | 旁白风格 | "成熟中文男声，专业自信+偶尔风趣" |
| {{USER_PREFERRED_STYLE}} | 用户偏好风格 | "科技感" |
| {{USER_PREFERRED_RHYTHM}} | 用户偏好节奏 | "快速动感" |
| {{SHOT_TIME_LIMIT}} | 单镜头时长上限（秒） | 15（默认值，可自定义） |
| {{SEGMENTS}} | 分镜段落内容 | 多个段落的具体描述 |
| {{SHOT_BREAKDOWN_TABLE}} | 镜头拆分表 | 段落拆分统计 |
| {{TECH_PROMPT_PREFIX}} | 技术提示前缀 | "remotion-best-practices" |
| {{CAMERA_MOVEMENTS}} | 运镜类型列表 | "推近、环绕、跟拍、摇移、拉远" |
| {{RHYTHM}} | 节奏描述 | "快而流畅" |
| {{VISUAL_SPECS}} | 视觉规范详情 | 颜色、字体、动画等详细规范 |

---

## 段落模板

### 段落X：{{SEGMENT_TITLE}}（{{START_TIME}}-{{END_TIME}}秒）

**段落目标**：{{SEGMENT_GOAL}}

**镜头序列**（共{{SHOT_COUNT}}个镜头，每个≤{{SHOT_TIME_LIMIT}}秒）：

```
{{SHOTS_SEQUENCE}}
```

**旁白**："{{NARRATION_CONTENT}}"

---

## 镜头模板

```
镜头Y：{{SHOT_TYPE}}（{{SHOT_TIME_RANGE}}）
- 运镜：{{CAMERA_MOVEMENT}}
- 布局：{{SHOT_LAYOUT}}
- 视觉：{{SHOT_VISUAL}}
- 过渡：{{SHOT_TRANSITION}}
```

---

## 视频类型说明

| 类型代码 | 类型名称 | 典型场景 |
|---------|---------|---------|
| concept_teaching | 概念讲解 | AI原理、区块链机制、物理定律 |
| book_intro | 书籍介绍 | 书籍推荐、章节导读、读书笔记 |
| hot_comment | 热点评论 | 新闻解读、事件分析、观点表达 |
| story_board | 剧情分镜 | 短片分镜、动画脚本、故事板 |
| product_intro | 产品介绍 | 产品发布、功能演示、App介绍 |
| data_report | 数据报告 | 数据可视化、研究报告、趋势分析 |
| tutorial | 教程指南 | 操作指南、软件教程、流程说明 |

---

## 头脑风暴清单（生成前确认）

- [ ] 视频类型确定了吗？
- [ ] 主题内容明确了吗？
- [ ] 目标受众是谁？
- [ ] 核心信息是什么？
- [ ] 视频时长确定了吗？
- [ ] 镜头时长限制确定了吗？（默认15秒，可自定义）
- [ ] 视觉风格选好了吗？
- [ ] 需要主角/吉祥物吗？
- [ ] 旁白风格确定了吗？
- [ ] 旁白/台词呈现方式确定了吗？
- [ ] 运镜节奏偏好？
- [ ] 段落结构根据主题设计好了吗？
- [ ] 需要音效/BGM建议吗？
- [ ] 需要生成OpenCode提示词吗？（专业版）
- [ ] 故事类视频的角色设定确定了吗？
- [ ] 角色提示词比例确定了吗？（默认9:16）
- [ ] 所有镜头时长≤设定的上限？
