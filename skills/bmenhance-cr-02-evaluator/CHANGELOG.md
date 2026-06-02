# Changelog

本文件记录 `bmenhance-cr-02-evaluator` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.2.1] - 2026-04-10

### Changed

- `references/cr-config.md` 路径配置适配 bmad 文档目录重构：Story 文件移至 `stories/`、CR 目录移至 `code-reviews/`、CR 规则文件移至 `cr-rules/`、回顾文件移至 `retrospectives/`
- `metadata.version` 从 `"1.2.0"` 升级为 `"1.2.1"`

## [1.2.0] - 2026-04-02

### Added

- 新增四桶分类感知能力：识别并利用审查结果中的「来源」（blind/edge/auditor）和「分类」（decision_needed/patch/defer）增强字段，辅助评估判断
- 新增 `references/cr-config.md` 通用配置文件，统一路径约定和文件名格式
- output-format.md 新增「审查增强字段说明」章节，描述来源和分类字段的含义和评估用法

### Changed

- Step 1~3 将硬编码的路径约定和文件名格式替换为引用 `references/cr-config.md`
- Step 4 增加对多来源命中和四桶分类的评估参考逻辑

## [1.1.0] - 2026-04-01

### Added

- 新增 `assets/output-format.md` 输出格式模板，定义评估文档的标准章节结构
- 模板包含 YAML 元信息头部、评估总结、上轮问题回顾确认、逐条发现评估、整体评估结论等章节规范
- 模板包含优先级定义、评估分析要求、元信息字段说明等格式规范

### Changed

- Step 5 执行流程从内嵌 YAML 元信息示例改为引用 `assets/output-format.md` 模板
- LLM 执行评估时不再需要搜索已有评估文件来学习输出格式，直接按模板生成

## [1.0.0] - 2026-03-29

### 初始版本

- 审查结果评估，对 CR 代码审查的发现逐条评估其合理性和准确性
- 自动定位最新结果，扫描并定位最新一轮的代码审查结果文件
- 评估轮次管理，自动检测已有评估轮次并正确编号
- 历史参考，在有明确异议时参考过往轮次的审查结果
- 结构化评估输出，生成规范化的评估文档包含逐条评估结论
- 只读安全保障，严格禁止修改源码、Story 文档和执行修复操作

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
