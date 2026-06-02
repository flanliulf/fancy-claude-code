---
name: bmenhance-cr-01-reviewer
description: "Execute cross-LLM code review for a Story using parallel adversarial review layers (Blind Hunter, Edge Case Hunter, Acceptance Auditor) with structured triage, and save review summary to a structured result file. Use when user mentions 'CR', 'code review', 'crossllm review', 're-review', 'code review summary', '代码审查', 'CR 审查', '跨模型审查', '代码复审', '代码评审', '审查代码', or wants to review Story code changes. Capable of first-round and subsequent-round code reviews, parallel three-layer adversarial analysis, four-bucket triage, auto-detecting review history, and generating structured review result documents with round numbering."
allowed-tools: Read, Write, Bash, Grep, Glob, Agent
metadata:
  version: "3.0.1"
---

[技能说明]
    针对指定 Story 执行跨 LLM 代码审查（CR），通过并行三层对抗式审查（Blind Hunter、Edge Case Hunter、Acceptance Auditor）对代码变更进行多维度分析，将发现进行四桶分类和严重性标签映射后，输出结构化的审查总结并保存到规范化的结果文件中。支持多轮审查的自动编号和历史记录追踪。

[核心能力]
    - **并行三层审查**：通过 Agent 工具同时启动 Blind Hunter（review-adversarial-general）、Edge Case Hunter（review-edge-case-hunter）、Acceptance Auditor（review-acceptance-auditor）三个独立子代理，从对抗式批判、边界条件穷举、验收标准对照三个正交维度并行分析，天然实现上下文隔离
    - **四桶分类**：将所有发现去重后分入 decision_needed / patch / defer / dismiss 四个桶，每个桶有明确的判定条件
    - **严重性标签映射**：四桶分类与 [高/中/低] 严重性标签并存，基于来源数量和安全关键词进行映射
    - **自动轮次检测**：自动扫描已有审查结果文件，确定当前轮次编号（n）
    - **首轮/复审自适应**：首轮审查聚焦全量代码，复审聚焦上轮修复点和残留问题
    - **结构化结果保存**：按规范文件名格式自动创建审查结果文件
    - **历史记录感知**：复审时自动参考历次 CR 结果和修复记录，避免重复指出已修复的问题
    - **子审查失败降级**：任一子代理失败时使用剩余层继续；Agent 工具不可用时降级为串行模式；全部失败时降级为单一 LLM 审查
    - **只读安全保障**：严格禁止修改源码和 Story 文档，仅输出审查总结（Bash 仅用于 git diff，Agent 仅用于子审查调度）

[执行流程]

    路径约定和文件名格式以 `references/cr-config.md` 为准。
    运行时变量使用 `$snake_case` 格式标识，与 cr-config.md 中的文件名模板占位符 `{花括号}` 区分。

    Step 1：定位 Story 和代码审查目录
        - 接收用户指定的 Story 标识（如 Story 文件路径或 Story ID）
        - 读取 `references/cr-config.md` 获取路径约定
        - 按配置中的 Story 文件目录定位 Story 文件
        - 按配置中的 Story ID 规则提取 → `$story_id`
        - 按配置中的代码审查目录格式确定路径 → `$cr_dir`
        - 创建临时文件目录：`$cr_dir/.tmp/`（如不存在）

    Step 2：检测审查轮次
        - 读取 `references/cr-config.md` 获取审查总结文件名格式
        - 按配置中的轮次检测规则，扫描 `$cr_dir` 下已有的审查总结文件
        - 统计已有的审查轮次数量，确定本轮轮次号 → `$round_number` = 已有轮次 + 1
        - 判断审查类型 → `$review_type`：
            - `$round_number` == 1 → 首轮审查
            - `$round_number` > 1 → 复审（需参考历史记录）

    Step 3：收集审查上下文（复审场景）
        - IF 复审（`$round_number` > 1）：
            - 读取历次 CR 结果文件（按配置中的文件名格式匹配）
            - 读取历次评估文件（按配置中的文件名格式匹配）
            - 重点关注最新一轮评估文件中的 "## 修复执行记录" 章节
            - 建立"已修复问题清单" → `$review_context`
            - 将 `$review_context` 写入 `$cr_dir/.tmp/review-context.md`
        - IF 首轮（`$round_number` == 1）：
            - 跳过此步骤

    Step 4：执行代码审查（三层并行审查引擎）
        - 传入 review-engine.md 的变量（上下文传递）：
            - `$story_id`、`$cr_dir`、`$round_number`、`$review_type`
        - 传入 review-engine.md 的文件（复审时）：
            - `$cr_dir/.tmp/review-context.md`
        - 读取并执行 `references/review-engine.md`
        - 该引擎将完成：构建审查输入（diff/文件内容）→ 并行三层审查 → 规范化去重 → 四桶分类 + 严重性标签映射
        - 引擎执行完毕后获取：
            - `$failed_layers`（上下文传回，失败的审查层名称列表）
            - `$review_findings`（从 `$cr_dir/.tmp/classified-findings.json` 读取）

    Step 5：生成并保存审查总结
        - 读取 `$cr_dir/.tmp/classified-findings.json` 获取 `$review_findings`
        - 读取输出格式模板：`assets/output-format.md`
        - 根据 `$review_type`（首轮/复审）选择对应模板，将 `$review_findings` 整理为结构化总结
        - 只保存总结/结论部分，不保存完整审查过程
        - 确定今天日期，格式为 YYYYMMDD
        - 创建 `$cr_dir` 目录（如不存在）
        - 按 `references/cr-config.md` 中的文件名格式保存文件
        - 严格按照模板中定义的章节结构和格式规范输出，包括：
            - YAML 元信息头部
            - 审查结论（含审查层状态标注，引用 `$failed_layers`）
            - 上轮问题回顾（复审时）
            - 新发现（含严重性标签、四桶分类、审查来源、证据、影响、建议）
            - 验证摘要
            - 通过项（含 defer 桶的已知既有问题）
            - 结论（复审时）
        - 清理临时文件：删除 `$cr_dir/.tmp/` 目录及其所有内容（删除失败不阻断流程）
        - 向用户展示审查总结要点
        - 完成后返回："✅ CR 代码审查完成（第 `$round_number` 轮），结果已保存"

[注意事项]
    - **绝对禁止**修改任何源码文件
    - **绝对禁止**修改 Story 文档内容
    - **绝对禁止**自行执行修复操作
    - Bash 工具仅用于执行 `git diff` 获取代码差异，禁止用于任何代码修改操作
    - 结果文件中只保存总结/结论部分，禁止保存完整的审查输出过程，避免内容篇幅过大
    - 路径约定和文件名格式以 `references/cr-config.md` 为准，不硬编码
    - 三层子审查的详细执行逻辑见 `references/review-engine.md`
    - 子审查失败时使用剩余层继续；全部失败时降级为单一 LLM 自行按 6 维度审查，并向用户明确告知降级
    - 始终使用中文输出审查结果
    - 复审时必须标注哪些问题是新发现的、哪些是上轮遗留的
    - 输出文件头部的 `Model Used` 字段必须如实填写当前执行审查的模型名称，便于跨 LLM 追溯和质量归因
    - 如果找不到 Story 文件或关联代码，立即停止并告知用户
    - 禁止对同一 Story 同时发起多次审查——同一 Story 的临时文件共享同一 `$cr_dir/.tmp/` 目录，并行执行会导致文件互相覆盖
