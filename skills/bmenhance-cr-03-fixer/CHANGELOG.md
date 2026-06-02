# Changelog

本文件记录 `bmenhance-cr-03-fixer` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.1] - 2026-04-10

### Changed

- `references/cr-config.md` 路径配置适配 bmad 文档目录重构：Story 文件移至 `stories/`、CR 目录移至 `code-reviews/`、CR 规则文件移至 `cr-rules/`、回顾文件移至 `retrospectives/`
- `metadata.version` 从 `"1.0.0"` 升级为 `"1.0.1"`

## [1.0.0] - 2026-04-02

### 初始版本

- 评估驱动修复：严格按照《代码审查结果评估文件》的结论执行修复，不自行扩大修复范围
- 自动定位评估文件：自动扫描并定位最新一轮的《代码审查结果评估文件》
- 精准定点修复：针对评估确认需要修复的问题逐一处理
- 修复记录追踪：将修复执行总结追加到评估文件的指定章节
- 修复验证：修复后验证代码编译/运行是否正常
- 路径约定引用 `references/cr-config.md` 统一配置

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
