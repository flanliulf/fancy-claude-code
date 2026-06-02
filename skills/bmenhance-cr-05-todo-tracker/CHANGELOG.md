# Changelog

本文件记录 `bmenhance-cr-05-todo-tracker` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.2.1] - 2026-04-10

### Changed

- `references/cr-config.md` 路径配置适配 bmad 文档目录重构：Story 文件移至 `stories/`、CR 目录移至 `code-reviews/`、CR 规则文件移至 `cr-rules/`、回顾文件移至 `retrospectives/`
- SKILL.md [技能说明] 中 `cr-todo-backlog.md` 路径从 `implementation-artifacts/` 根更新为 `implementation-artifacts/cr-rules/`
- SKILL.md [注意事项] 中 backlog 默认位置引用从"实现产物目录"更正为"CR 规则目录"
- `metadata.version` 从 `"1.2.0"` 升级为 `"1.2.1"`

## [1.2.0] - 2026-04-02

### Added

- 新增 `references/cr-config.md` 通用配置文件，统一路径约定和文件名格式

### Changed

- 模式 A Step 1、模式 E Step 1 将硬编码的代码审查目录路径和文件名格式替换为引用 `references/cr-config.md`
- cr-todo-backlog.md 的默认位置改为引用 cr-config.md 中的实现产物目录配置

## [1.1.0] - 2026-04-01

### Added

- 新增 `assets/output-format.md` 输出格式模板，包含文件初始化骨架、单个条目标准格式、字段说明和文档操作规范
- 首次创建 backlog 文件时自动按模板初始化，无需手动创建

### Changed

- 模式 A Step 3 条目生成流程改为引用 `assets/output-format.md` 中的条目模板
- backlog 文件不存在时的行为从"提示用户先创建"改为"按模板自动创建"

## [1.0.0] - 2026-03-29

### 初始版本

- 添加条目 (add)：从 CR evaluation/summary 中提取非阻塞改进项
- 检查相关条目 (check)：根据当前 story 涉及文件查找匹配的 open 条目
- 标记解决 (resolve)：将条目状态改为 resolved 并归档
- 查看摘要 (list)：展示所有 open/in-progress 条目概览
- 批量提取 (extract)：从指定 story 的所有 CR 文件中批量识别可延迟项

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
