# Changelog

本文件记录 `review-acceptance-auditor` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.0] - 2026-04-07

### 初始版本

- AC 逐条对照：将代码变更与 Story 验收标准逐条对照
- 违规检测：识别违反验收条件的代码实现
- 偏差检测：识别偏离规格意图的行为
- 缺失检测：识别规格中指定但未实现的行为
- 矛盾检测：识别规格约束与实际代码之间的矛盾
- 结构化输出：每条发现包含标题、AC 引用、代码证据
- 从 bmenhance-cr-01-reviewer 的 review-engine.md B3 内嵌提示词独立为完整 Skill

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
