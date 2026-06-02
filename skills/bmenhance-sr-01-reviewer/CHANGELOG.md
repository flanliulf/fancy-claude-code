# Changelog

本文件记录 `bmenhance-sr-01-reviewer` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [1.0.0] - 2026-04-13

### 初始版本

- 并行三层审查：通过 Agent 工具同时启动 Structure & Completeness Hunter、Consistency Checker、Contract & Boundary Auditor 三个独立子代理
- 双粒度审查：支持 Epic 模式（审查 Epic 下全部 Story）和 Story 模式（审查单个 Story）
- 四桶分类：将发现分入 decision_needed / patch / defer / dismiss 四个桶
- 严重性标签映射：四桶分类与 [高/中/低] 严重性标签并存
- 自动轮次检测：自动扫描已有审查结果文件确定当前轮次
- 首轮/复审自适应：首轮聚焦全量文档，复审聚焦修复点和残留问题
- 大批量分批处理：Epic 模式下 Story > 5 时自动分批
- 子审查失败降级：任一子代理失败时使用剩余层继续，全部失败时降级为单一 LLM 审查
- 统一路径配置：引用 `references/sr-config.md` 避免硬编码

### 已知限制

- 三层子代理复用 review-adversarial-general、review-edge-case-hunter、review-acceptance-auditor，通过 prompt 定向而非 SR 专用子 Skills
- Story 模式下跳过 Story 间冲突与依赖维度，可能遗漏部分关联问题

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
已知问题修复后，用删除线标注并注明修复版本，如：
- ~~**问题描述**~~ → 已在 vX.Y.Z 修复
