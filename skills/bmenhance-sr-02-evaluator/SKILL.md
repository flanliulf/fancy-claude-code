---
name: bmenhance-sr-02-evaluator
description: "Evaluate Story design review results and generate a structured evaluation document. Use when user mentions 'SR evaluate', 'SR evaluation', 'evaluate SR', 'story review evaluation', 'design review evaluation', '评估 SR', '评估审查结果', 'SR 评估', '设计审查评估', 'Story 审查评估', '评估 Story 审查', or wants to assess Story design review findings. Capable of reading latest review results, assessing finding validity with source and bucket awareness, and producing evaluation documents with round numbering."
allowed-tools: Read, Write, Grep, Glob
metadata:
  version: "1.0.0"
  author: "fancyliu"
---

[技能说明]
    对 Story 设计审查的结果进行独立评估，判断审查发现的合理性和准确性，生成结构化的评估文档。作为 SR 审查工作流的质量把关环节，确保审查发现的客观性。

[核心能力]
    - **审查结果评估**：对 SR 审查的发现逐条评估其合理性和准确性
    - **四桶分类感知**：识别并利用审查结果中的「来源」（structure/consistency/contract）和「分类」（decision_needed/patch/defer）增强字段，辅助评估判断
    - **自动定位最新结果**：自动扫描并定位最新一轮的审查总结文件
    - **评估轮次管理**：自动检测已有评估轮次，正确编号新一轮评估
    - **双粒度适配**：自动从审查总结文件的 Scope 字段识别粒度，适配 Epic 和 Story 两种模式
    - **历史参考**：在有明确异议时可参考过往轮次的审查结果
    - **结构化评估输出**：生成规范化的评估文档，包含逐条评估结论
    - **只读安全保障**：严格禁止修改 Story 文档、源码和执行修订操作

[执行流程]
    路径约定和文件名格式以 `references/sr-config.md` 为准。

    Step 1：定位 Story 审查目录和文件
        - 接收用户指定的 Epic 或 Story 标识
        - 读取 `references/sr-config.md` 获取路径约定和双粒度判定规则
        - 根据用户输入判定 `$review_scope`（逻辑与 SR-01 一致）
        - 按 `$review_scope` 确定 `$sr_dir`
        - 生成数据：`$review_scope`、`$epic_id`、`$story_id`（Story 模式）、`$sr_dir`

    Step 2：定位最新一轮审查结果
        - 按配置中的审查总结文件名格式，扫描 `$sr_dir` 下匹配的文件
        - 找到 round 值最大的文件作为本次评估对象
        - 读取该文件的完整内容
        - 从 YAML 头部 `Scope` 字段确认粒度（epic/story），验证与 Step 1 判定一致
        - 生成数据：`$latest_review_file`、`$review_round_number`

    Step 3：检测评估轮次
        - 按配置中的审查评估文件名格式，扫描 `$sr_dir` 下匹配的文件
        - 统计已有的评估轮次数量，确定本轮评估轮次号 `$evaluation_round_number` = 已有轮次 + 1
        - 生成数据：`$evaluation_round_number`

    Step 4：执行评估
        - 逐条审阅 SR 审查结果中的发现（Findings）
        - 若发现包含「来源」字段（如 structure/consistency/contract/structure+consistency），将其作为评估参考：
            - 多来源命中的发现可信度更高，应优先确认
            - 单来源发现需更谨慎验证，尤其关注是否为误报
        - 若发现包含「分类」字段（如 decision_needed/patch/defer），将其作为评估参考：
            - `decision_needed`：重点评估是否确实需要人工裁决
            - `patch`：验证修订方案的可行性和完整性
            - `defer`：确认是否确实为既有问题而非本次引入
        - 对每条发现进行评估：
            - 问题描述是否准确？
            - 严重性判断是否合理？
            - 修订建议是否可行？
            - 是否存在误报（false positive）？
        - 如有明确异议，可参考过往轮次的审查总结文件进行交叉验证
        - 给出整体评估结论：
            - 哪些发现需要修订（分优先级）
            - 哪些发现可以忽略（说明理由）
            - 哪些发现需要进一步讨论
        - 生成数据：`$evaluation_findings`（评估结论列表）

    Step 5：保存评估结果
        - 读取输出格式模板：`assets/output-format.md`
        - 按 `$review_scope` 选择对应模板变体（元信息头部 Epic/Story 字段）
        - 按照模板中定义的章节结构生成评估文档
        - 确定今天日期，格式为 YYYYMMDD
        - 按 `references/sr-config.md` 中的文件名格式保存文件
        - 严格按照模板中定义的章节结构和格式规范输出，包括：
            - YAML 元信息头部（含 Scope、Review Source 和 Review Model）
            - 评估总结
            - 上轮问题回顾确认（被评估审查为复审时）
            - 逐条发现评估（审查原文、评估结论、评估分析）
            - 整体评估结论（需修订表格、后续改善表格、评估决定）
        - 向用户展示评估结论要点
        - 完成后返回："✅ SR 审查结果评估完成（第 `$evaluation_round_number` 轮），结果已保存"

[注意事项]
    - **绝对禁止**修改任何 Story 文档
    - **绝对禁止**修改任何源码文件
    - **绝对禁止**自行执行修订操作
    - 只对最新一轮（round 值最大）的审查总结文件进行评估
    - 只有在有明确异议时才允许参考过往轮次的审查总结文件
    - 路径约定和文件名格式以 `references/sr-config.md` 为准，不硬编码
    - 始终使用中文输出评估结果
    - 评估要客观公正，对误报要明确标注并给出理由
    - 审查结果中的「来源」和「分类」字段为可选增强信息，若存在则利用其辅助评估，若不存在则按原有逻辑评估
    - 输出文件头部的 `Model Used` 字段必须如实填写当前执行评估的模型名称；`Review Model` 字段从被评估的审查结果文件头部读取，便于跨 LLM 追溯
    - 如果找不到审查结果文件，立即停止并告知用户

[生成信息]
    本 Skill 由 skills-creator 自动生成。如需修改，建议同步更新 forge/ 和 .claude/skills/ 两份副本，或通过 skills-upgrade 管理版本。
