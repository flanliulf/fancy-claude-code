# Changelog

本文件记录 `bmenhance-cr-04-rules-extractor` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.2.1] - 2026-05-15

### Added

- 新增 `references/promotion-rules.md`，承载规则升格判定的硬性门槛、6 维评分矩阵和阈值去向细则
- 新增 `metadata.author` 字段，记录作者为 `fancyliu`

### Changed

- 精简 `SKILL.md` 正文，将升格判定细则外移到 references，以满足正文长度规范
- 合并核心能力中的规则总结沉淀和模板化输出，控制核心能力条数在规范范围内
- `metadata.version` 从 `"1.2.0"` 升级为 `"1.2.1"`

## [1.2.0] - 2026-05-15

### Added

- 新增执行模式：`analysis-only`、`apply-confirmed`、`record-only`，明确只读分析、确认后全局文档落地和仅记录规则总结三种路径
- 新增量化规则升格判定机制：硬性门槛、6 维 0-2 分评分矩阵、阈值去向和禁止升格条件
- 新增 `cr-rules-summary.md` 作为 04-rules-extractor 的正式规则沉淀输出物
- 新增 `assets/output-format.md`，定义 `cr-rules-summary.md` 的文件初始化模板、Story 记录格式、单条规则格式和文档操作规范
- 新增与 05 TODO Tracker 的职责边界：已验证可复用规则进入规则总结，未解决非阻塞改进交由 TODO backlog 管理

### Changed

- Step 5-9 重构为规则升格判定、全局文档建议、用户确认、确认后落地和结果输出的双阶段流程
- `metadata.version` 从 `"1.1.1"` 升级为 `"1.2.0"`

## [1.1.1] - 2026-04-10

### Changed

- `references/cr-config.md` 路径配置适配 bmad 文档目录重构：Story 文件移至 `stories/`、CR 目录移至 `code-reviews/`、CR 规则文件移至 `cr-rules/`、回顾文件移至 `retrospectives/`
- `metadata.version` 从 `"1.1.0"` 升级为 `"1.1.1"`

## [1.1.0] - 2026-04-02

### Added

- 新增四桶分类感知能力：识别审查结果中的「来源」和「分类」增强字段，按审查层维度和四桶分类进行交叉统计分析
- 新增 `references/cr-config.md` 通用配置文件，统一路径约定和文件名格式

### Changed

- Step 1 将硬编码的路径约定和文件名格式替换为引用 `references/cr-config.md`
- Step 3 增加审查层分布和四桶分类占比的统计维度
- Step 6 输出总结增加审查层分布和四桶分类占比信息

## [1.0.0] - 2026-04-02

### 初始版本

- CR 历史分析：系统性阅读和分析 Story 的全部 CR 审查、评估及修正记录
- 共性问题识别：从多轮 CR 发现中识别重复出现的模式和共性问题
- 规则提炼：将共性问题转化为可操作的开发规约、指导原则或最佳实践
- 全局文档建议：评估提炼的规则是否适合补充到 project-context.md、architect.md 等全局文档
- 结构化输出：以清晰的结构输出分析结果和建议，供用户确认
- 路径约定引用 `references/cr-config.md` 统一配置

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
