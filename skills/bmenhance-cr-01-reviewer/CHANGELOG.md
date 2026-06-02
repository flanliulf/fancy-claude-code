# Changelog

本文件记录 `bmenhance-cr-01-reviewer` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [3.0.1] - 2026-04-10

### Changed

- `references/cr-config.md` 路径配置适配 bmad 文档目录重构：Story 文件移至 `stories/`、CR 目录移至 `code-reviews/`、CR 规则文件移至 `cr-rules/`、回顾文件移至 `retrospectives/`
- SKILL.md Step 1 移除 `$story_dir` 中间变量，改为直接引用配置中的 Story 文件目录
- `references/review-engine.md` 隔离机制说明中的 `$cr_dir` 示例路径更新
- `metadata.version` 从 `"3.0.0"` 升级为 `"3.0.1"`

## [3.0.0] - 2026-04-07

### Added

- 新增 Agent 并行调度机制：通过 Agent 工具在同一条消息中同时启动三个独立子代理（Blind Hunter、Edge Case Hunter、Acceptance Auditor），实现真正的并行执行和上下文隔离
- 新增 review-acceptance-auditor 独立 Skill（从 review-engine.md B3 内嵌提示词提取），使三个审查层完全对称
- 新增 B0 执行模式选择：Agent 并行 → 串行降级 → 部分层降级 → 单一 LLM 兜底，四级降级策略
- `allowed-tools` 新增 `Agent`（用于子审查调度）

### Changed

- Phase B 全部重写：B1/B2/B3 从当前上下文内串行模拟改为 Agent 子代理独立调用（**破坏性变更**：审查执行方式根本性改变）
- B3 Acceptance Auditor 从内嵌提示词改为调用独立的 `review-acceptance-auditor` Skill
- 核心能力描述更新：明确标注 Agent 工具并行调度和上下文隔离特性
- 降级策略更新：新增 Agent 工具不可用时的串行降级路径
- `metadata.version` 从 `"2.1.0"` 升级为 `"3.0.0"`

## [2.1.0] - 2026-04-07

### Added

- 新增临时文件存储机制（`$cr_dir/.tmp/`）：大体积中间数据（diff、子审查输出、规范化结果、分类结果）写入临时文件，避免上下文窗口溢出
- cr-config.md 新增临时文件目录配置和变量标识约定说明
- SKILL.md Step 4 新增显式的变量传入/传出声明（SKILL.md ↔ review-engine.md 边界）
- SKILL.md Step 5 新增临时文件清理步骤

### Changed

- 统一全部运行时变量命名为 `$snake_case` 格式，与文件名模板占位符 `{花括号}` 区分
- review-engine.md 各 Phase 增加临时文件写入/读取指令：Phase A 写入 review-input.diff 和 spec-content.md，Phase B 各层写入输出文件，Phase C 写入 normalized-findings.json，Phase D 写入 classified-findings.json
- review-engine.md Phase E4 输出交接方式从隐式上下文改为文件（classified-findings.json）+ 上下文（$failed_layers）组合

## [2.0.0] - 2026-04-03

### Added

- 新增三层并行审查引擎（`references/review-engine.md`），替代原有的单一 LLM 自行审查
  - 盲猎手（review-adversarial-general）：对抗式批判审查，仅接收 diff，不接收项目上下文
  - 边界猎手（review-edge-case-hunter）：穷举式边界条件分析，接收 diff + 项目读取权限
  - 验收审计员：验收标准（AC）对照审查，接收 diff + Story AC
- 新增四桶分类体系（decision_needed / patch / defer / dismiss），与严重性标签 [高/中/低] 并存
- 新增 `references/cr-config.md` 通用配置文件，抽取路径约定、文件名格式、Story ID 规则等硬编码项
- 新增子审查失败降级机制：任一层失败时使用剩余层继续；全部失败时降级为单一 LLM 审查
- 新增 allowed-tools: Bash（仅用于 git diff 获取代码差异）
- output-format.md 新增可选的「来源」和「分类」增强字段（向后兼容）

### Changed

- Step 4 从「单一 LLM 自行按 6 维度审查」重写为「读取并执行 references/review-engine.md（三层并行审查引擎）」（**破坏性变更**：审查引擎完全重写）
- Step 1~3 将硬编码的路径约定和文件名格式替换为引用 `references/cr-config.md`
- allowed-tools 从 `Read, Write, Grep, Glob` 扩展为 `Read, Write, Bash, Grep, Glob`

## [1.1.0] - 2026-04-01

### Added

- 新增 `assets/output-format.md` 输出格式模板，定义首轮审查和复审两种场景的标准文档结构
- 模板包含 YAML 元信息头部、审查结论、上轮问题回顾、新发现、验证摘要、通过项等章节规范
- 模板包含严重性标签、新发现标注、证据引用格式等格式规范

### Changed

- Step 5 执行流程从内嵌 YAML 元信息示例改为引用 `assets/output-format.md` 模板
- LLM 执行审查时不再需要搜索已有审查文件来学习输出格式，直接按模板生成

## [1.0.0] - 2026-03-29

### 初始版本

- 跨 LLM 代码审查，对 Story 关联的代码变更进行全面审查
- 自动轮次检测，扫描已有审查结果文件确定轮次编号
- 首轮/复审自适应，首轮聚焦全量代码，复审聚焦修复点和残留问题
- 结构化结果保存，按规范文件名格式自动创建审查结果文件
- 历史记录感知，复审时参考历次 CR 结果和修复记录
- 只读安全保障，严格禁止修改源码和 Story 文档

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
