# Changelog

本文件记录 `review-adversarial-general` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.0] - 2026-04-02

### 初始版本

- 对代码 diff、规格说明、用户故事、文档等任意制品进行对抗式审查
- 强制找出至少十条发现，防止审查流于表面
- 支持 `also_consider` 可选参数，指定额外关注领域
- 发现数为零时触发中止保护，强制重新分析
- 内容为空或不可读时立即中止并告知用户
- 以 Markdown 无序列表格式输出发现报告（仅描述，不含情绪化语言）

### 已知限制

- 无（初始版本）

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在 [1.0.0] 之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
