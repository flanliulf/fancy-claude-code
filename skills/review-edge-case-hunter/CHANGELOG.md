# Changelog

本文件记录 `review-edge-case-hunter` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.0] - 2026-04-02

### 初始版本

- 对代码 diff、完整文件、函数进行穷举式边界条件分析
- diff 模式：仅扫描 diff 块中直接可达且缺少显式防守的边界
- 全文件/函数模式：将整个内容作为分析范围
- 支持可选 `also_consider` 参数，将指定领域纳入分析维度
- Step 3 完整性二次验证，确保边缘类别无遗漏
- 输出严格的四字段 JSON 数组（location、trigger_condition、guard_snippet、potential_consequence）
- 内容为空或无法解码时返回结构化错误 JSON 并停止

### 已知限制

- 无（初始版本）

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在 [1.0.0] 之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
