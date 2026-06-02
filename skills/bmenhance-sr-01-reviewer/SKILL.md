---
name: bmenhance-sr-01-reviewer
description: "Execute Story design review for an Epic or single Story using parallel three-layer adversarial analysis (Structure Hunter, Consistency Checker, Contract Auditor) with four-bucket triage, and save review summary to a structured result file. Use when user mentions 'SR', 'story review', 'story design review', 'epic review', 'story check', 'design review', 'Story 审查', 'SR 审查', '设计审查', 'Story 设计审查', 'Epic 审查', '审查 Story', '审查 Epic', or wants to review Story design documents before development. Capable of dual-granularity review (Epic-level or single-Story), parallel three-layer adversarial analysis, four-bucket triage, auto-detecting review history, batch processing, and generating structured review result documents with round numbering."
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
metadata:
  version: "1.0.0"
  author: "fancyliu"
---

[技能说明]
    针对指定 Epic 或单个 Story 执行设计文档审查（SR），通过并行三层对抗式审查（Structure & Completeness Hunter、Consistency Checker、Contract & Boundary Auditor）对 Story 设计文档进行多维度分析，将发现进行四桶分类和严重性标签映射后，输出结构化的审查总结并保存到规范化的结果文件中。支持 Epic 粒度和 Story 粒度的双模式审查，以及多轮审查的自动编号和历史记录追踪。

[核心能力]
    - **并行三层审查**：通过 Agent 工具同时启动 Structure & Completeness Hunter、Consistency Checker、Contract & Boundary Auditor 三个独立子代理，从结构完整性、跨文档一致性、契约边界三个正交维度并行分析，天然实现上下文隔离
    - **双粒度审查**：支持 Epic 模式（审查 Epic 下全部 Story，启用跨 Story 维度）和 Story 模式（审查单个 Story，跳过 Story 间冲突维度），根据用户输入自动判定
    - **四桶分类**：将所有发现去重后分入 decision_needed / patch / defer / dismiss 四个桶，每个桶有明确的判定条件
    - **严重性标签映射**：四桶分类与 [高/中/低] 严重性标签并存，基于来源数量和安全关键词进行映射
    - **自动轮次检测**：自动扫描已有审查结果文件，确定当前轮次编号
    - **首轮/复审自适应**：首轮审查聚焦全量文档，复审聚焦上轮修复点和残留问题
    - **大批量分批处理**：Epic 模式下 Story > 5 时自动分批（每批 ≤ 5 个），确保审查质量
    - **子审查失败降级**：任一子代理失败时使用剩余层继续；全部失败时降级为单一 LLM 审查
    - **只读安全保障**：严格禁止修改 Story 文档和源码，仅输出审查总结

[执行流程]

    路径约定和文件名格式以 `references/sr-config.md` 为准。
    运行时变量使用 `$snake_case` 格式标识，与 sr-config.md 中的文件名模板占位符 `{花括号}` 区分。

    Step 1：判定审查粒度并定位目录
        - 接收用户指定的审查目标（Epic 标识或 Story 标识）
        - 读取 `references/sr-config.md` 获取路径约定和双粒度判定规则
        - 根据用户输入判定 `$review_scope`：
            - 匹配 `epic {N}` / `epic-{N}` → `$review_scope = "epic"`，`$epic_id = N`
            - 匹配 `story {N-M}` / `{N-M}` / Story 文件路径 → `$review_scope = "story"`，`$story_id = N-M`，从前缀提取 `$epic_id`
        - 按 `$review_scope` 和配置中的目录格式确定 `$sr_dir`
        - 创建临时文件目录：`$sr_dir/.tmp/`（如不存在）

    Step 2：检测审查轮次
        - 读取 `references/sr-config.md` 获取审查总结文件名格式
        - 按配置中的轮次检测规则，扫描 `$sr_dir` 下已有的审查总结文件
        - 统计已有轮次数量，确定本轮轮次号 → `$round_number` = 已有轮次 + 1
        - 判断审查类型 → `$review_type`：
            - `$round_number` == 1 → 首轮审查
            - `$round_number` > 1 → 复审（需参考历史记录）

    Step 3：收集审查上下文
        - IF 复审（`$round_number` > 1）：
            - 读取历次 SR 结果文件（按配置中的文件名格式匹配）
            - 读取历次评估文件（按配置中的文件名格式匹配）
            - 重点关注最新一轮评估文件中的 "## 修订执行记录" 章节
            - 建立"已修复问题清单" → 写入 `$sr_dir/.tmp/review-context.md`
        - 读取 Epic 定义文件：按配置中的 Epic 文件目录定位 `epic-{$epic_id}.md`
        - IF Epic 模式：
            - 按配置中的 Story 匹配规则扫描该 Epic 下全部 Story 文件 → `$story_files`
            - 统计 Story 数量
        - IF Story 模式：
            - 按配置中的 Story 匹配规则定位指定 Story 文件 → `$story_files`
        - 确定对照基准文件清单 → `$baseline_files`：
            - 必需：`project-context.md`
            - 必需：`epic-{$epic_id}.md`
            - 按需：架构文档（`03-core-decisions.md`、`04-implementation-patterns.md`）
            - 按需：前序 Epic 的相关 Story（当本 Epic 引用了前序 Epic 接口时）
        - 若 Epic 文件不存在：终止执行，告知用户

    Step 4：执行 Story 审查（三层并行审查引擎）
        - 传入 review-engine.md 的变量：
            - `$review_scope`、`$epic_id`、`$story_id`、`$sr_dir`、`$round_number`、`$review_type`
            - `$story_files`、`$epic_file`、`$baseline_files`
        - 传入 review-engine.md 的文件（复审时）：
            - `$sr_dir/.tmp/review-context.md`
        - 读取并执行 `references/review-engine.md`
        - 该引擎将完成：构建审查输入 → 并行三层审查 → 规范化去重 → 四桶分类 + 严重性标签映射
        - 引擎执行完毕后获取：
            - `$failed_layers`（上下文传回，失败的审查层名称列表）
            - `$review_findings`（从 `$sr_dir/.tmp/classified-findings.json` 读取）

    Step 5：生成并保存审查总结
        - 读取 `$sr_dir/.tmp/classified-findings.json` 获取 `$review_findings`
        - 读取输出格式模板：`assets/output-format.md`
        - 根据 `$review_scope`（epic/story）和 `$review_type`（首轮/复审）选择对应模板变体
        - 将 `$review_findings` 整理为结构化总结
        - 只保存总结/结论部分，不保存完整审查过程
        - 确定今天日期，格式为 YYYYMMDD
        - 创建 `$sr_dir` 目录（如不存在）
        - 按 `references/sr-config.md` 中的文件名格式保存文件
        - 严格按照模板中定义的章节结构和格式规范输出，包括：
            - YAML 元信息头部（含 Scope 字段）
            - 审查结论（含审查层状态标注，引用 `$failed_layers`）
            - 审查范围
            - 上轮问题回顾（复审时）
            - 新发现（含严重性标签、四桶分类、审查来源、证据、影响、建议）
            - 逐篇审查结论（仅 Epic 模式）
            - 通过项（含 defer 桶的已知既有问题）
        - 清理临时文件：删除 `$sr_dir/.tmp/` 目录及其所有内容（删除失败不阻断流程）
        - 向用户展示审查总结要点
        - 完成后返回："✅ SR Story 设计审查完成（第 `$round_number` 轮），结果已保存"

[注意事项]
    - **绝对禁止**修改任何 Story 文档
    - **绝对禁止**修改任何源码文件
    - **绝对禁止**自行执行修订操作
    - Bash 工具仅用于 `git log` 辅助判断文件变更历史，禁止用于任何文件修改操作
    - 结果文件中只保存总结/结论部分，禁止保存完整的审查输出过程，避免内容篇幅过大
    - 路径约定和文件名格式以 `references/sr-config.md` 为准，不硬编码
    - 三层子审查的详细执行逻辑见 `references/review-engine.md`
    - 子审查失败时使用剩余层继续；全部失败时降级为单一 LLM 自行审查，并向用户明确告知降级
    - 始终使用中文输出审查结果
    - 复审时必须标注哪些问题是新发现的、哪些是上轮遗留的
    - 输出文件头部的 `Model Used` 字段必须如实填写当前执行审查的模型名称，便于跨 LLM 追溯和质量归因
    - 如果找不到 Epic 文件或 Story 文件，立即停止并告知用户
    - Epic 模式下 Story > 5 时必须分批（每批 ≤ 5 个），每批结果追加写入同一份 summary 文件
    - 分批审查时需确保审查口径一致（同类问题给出同级别结论），跨批次依赖和冲突被识别
    - Story 模式下审查范围章节需注明"Story 间冲突与依赖维度未启用"

[生成信息]
    本 Skill 由 skills-creator 自动生成。如需修改，建议同步更新 forge/ 和 .claude/skills/ 两份副本，或通过 skills-upgrade 管理版本。
