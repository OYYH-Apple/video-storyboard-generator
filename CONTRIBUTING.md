# 贡献指南

感谢你考虑为 Video Storyboard Generator 贡献！

## 🤝 如何贡献

### 报告问题

发现问题？请创建 Issue，包含：

1. **问题描述** - 清晰描述问题
2. **重现步骤** - 如何复现问题
3. **环境信息** - Python 版本、操作系统
4. **日志或截图** - 相关错误信息或截图

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

- 使用清晰的提交消息（遵循约定式提交）
- 添加必要的注释和文档
- 遵循现有代码风格
- 编写测试（如有新功能）

### 文档贡献

文档同样重要！你可以：

- 修正错别字
- 添加使用示例
- 改进说明和文档结构
- 翻译文档

## 📋 贡献方向

### 优先级高

- [ ] 添加新的视频类型模板
- [ ] 优化镜头序列生成算法
- [ ] 完善测试覆盖
- [ ] 修复 bug

### 欢迎贡献

- [ ] 增加更多模板风格
- [ ] 改进用户体验
- [ ] 性能优化
- [ ] 文档改进
- [ ] 示例扩充

### 实验性功能

- [ ] Web UI 界面
- [ ] Remotion 直接集成
- [ ] AI 辅助生成建议
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

### 生成所有示例

```bash
python ../generate_all_examples.py
```

## 📄 许可

提交代码即表示你同意你的代码将在 MIT 许可下发布。

---

再次感谢你的贡献！🎉
