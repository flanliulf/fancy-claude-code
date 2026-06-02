# Changelog

本文件记录 `bmenhance-sr-02-evaluator` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.0] - 2026-04-13

### 初始版本

- 审查结果评估：对 SR 审查的发现逐条评估其合理性和准确性
- 四桶分类感知：识别并利用审查结果中的来源和分类增强字段辅助评估
- 自动定位最新结果：自动扫描并定位最新一轮的审查总结文件
- 评估轮次管理：自动检测已有评估轮次，正确编号新一轮评估
- 双粒度适配：自动从审查总结文件的 Scope 字段识别 Epic/Story 粒度
- 结构化评估输出：生成规范化的评估文档，包含逐条评估结论和整体评估结论
- 统一路径配置：引用 `references/sr-config.md` 避免硬编码

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
已知问题修复后，用删除线标注并注明修复版本，如：
- ~~**问题描述**~~ → 已在 vX.Y.Z 修复
