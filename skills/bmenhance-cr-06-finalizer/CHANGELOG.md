# Changelog

本文件记录 `bmenhance-cr-06-finalizer` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.1.1] - 2026-04-10

### Changed

- `references/cr-config.md` 路径配置适配 bmad 文档目录重构：Story 文件移至 `stories/`、CR 目录移至 `code-reviews/`、CR 规则文件移至 `cr-rules/`、回顾文件移至 `retrospectives/`
- SKILL.md Step 1 移除 `story-dir` 生成数据项，改为引用配置中的 Story 文件目录
- `metadata.version` 从 `"1.1.0"` 升级为 `"1.1.1"`

## [1.1.0] - 2026-04-02

### Added

- 新增 `references/cr-config.md` 通用配置文件，统一路径约定和文件名格式

### Changed

- Step 1 将硬编码的 Story ID 规则和代码审查目录路径替换为引用 `references/cr-config.md`
- Step 2 将硬编码的评估文件名格式替换为引用配置
- Step 5 sprint-status.yaml 路径改为引用 cr-config.md 中的实现产物目录配置
- Step 6 bmm-workflow-status.yaml 路径改为引用 cr-config.md 中的规划产物目录配置

## [1.0.0] - 2026-04-02

### 初始版本

- CR 审批确认：读取最新一轮 CR 评估文件，验证结论为 Approved
- Story 状态更新：将 Story 文件中的状态字段更新为 Done
- Sprint 状态同步：更新 sprint-status.yaml 中对应 Story 的状态
- 工作流状态同步：更新 bmm-workflow-status.yaml 中对应 Story 的状态
- Epic 状态联动：检测所属 Epic 下所有 Story 是否均已 Done 并提示用户
- 防重复执行：检测 Story 已是 Done 状态时避免重复操作
- 操作审计：输出完整的状态变更清单

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
已知问题修复后，用删除线标注并注明修复版本，如：
- ~~**问题描述**~~ → 已在 vX.Y.Z 修复
