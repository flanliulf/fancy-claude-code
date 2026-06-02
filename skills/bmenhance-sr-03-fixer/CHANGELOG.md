# Changelog

本文件记录 `bmenhance-sr-03-fixer` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.0] - 2026-04-13

### 初始版本

- 评估驱动修订：严格按照审查评估文件的结论执行修订，不自行扩大范围
- 自动定位评估文件：自动扫描并定位最新一轮的审查评估文件
- 双粒度适配：Epic 模式可修改多个 Story 文件，Story 模式仅修改单个 Story 文件
- 精准定点修订：针对评估确认需要修订的问题逐一处理
- 修订记录追踪：将修订执行总结追加到评估文件的指定章节
- 范围边界控制：Story 模式下超出范围的修订标记为"超出范围"提醒用户
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
