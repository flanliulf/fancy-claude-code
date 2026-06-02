---
name: bmenhance-cr-02-evaluator
description: "Evaluate code review results from a cross-LLM review round and generate a structured evaluation document. Use when user mentions 'CR evaluate', 'CR evaluation', 'evaluate CR', 'review assessment', 'code review evaluation', '评估审查结果', '评估 CR', '评估 CR 结果', 'CR 评估', '审查结果评估', 'CR 结果评估', '代码审查评估', or wants to assess code review findings. Capable of reading latest review results, assessing finding validity, and producing evaluation documents with round numbering."
allowed-tools: Read, Write, Grep, Glob
metadata:
  version: "1.2.1"
---

[技能说明]
    对跨 LLM 代码审查的结果进行独立评估，判断审查发现的合理性和准确性，生成结构化的评估文档。作为审查工作流的质量把关环节，确保 CR 发现的客观性。

[核心能力]
    - **审查结果评估**：对 CR 代码审查的发现逐条评估其合理性和准确性
    - **四桶分类感知**：识别并利用审查结果中的「来源」（blind/edge/auditor）和「分类」（decision_needed/patch/defer）增强字段，辅助评估判断
    - **自动定位最新结果**：自动扫描并定位最新一轮的《代码审查结果文件》
    - **评估轮次管理**：自动检测已有评估轮次，正确编号新一轮评估
    - **历史参考**：在有明确异议时可参考过往轮次的审查结果
    - **结构化评估输出**：生成规范化的评估文档，包含逐条评估结论
    - **只读安全保障**：严格禁止修改源码、Story 文档和执行修复操作

[执行流程]
    路径约定和文件名格式以 `references/cr-config.md` 为准。

    Step 1：定位代码审查目录和文件
        - 读取 `references/cr-config.md` 获取路径约定
        - 按配置中的 Story ID 规则提取 `{story-id}`
        - 按配置中的代码审查目录格式确定路径
        - 生成数据：story-id、code-review-dir

    Step 2：定位最新一轮审查结果
        - 按配置中的审查总结文件名格式，扫描 code-review-dir 下匹配的文件
        - 找到 round 值（n）最大的文件作为本次评估对象
        - 读取该文件的完整内容
        - 生成数据：latest-review-file、review-round-number

    Step 3：检测评估轮次
        - 按配置中的审查评估文件名格式，扫描 code-review-dir 下匹配的文件
        - 统计已有的评估轮次数量，确定本轮评估轮次号 m = 已有评估轮次 + 1
        - 生成数据：evaluation-round-number（m）

    Step 4：执行评估
        - 逐条审阅 CR 审查结果中的发现（Findings）
        - 若发现包含「来源」字段（如 blind/edge/auditor/blind+edge），将其作为评估参考：
            - 多来源命中（如 blind+edge）的发现可信度更高，应优先确认
            - 单来源发现需更谨慎验证，尤其关注是否为误报
        - 若发现包含「分类」字段（如 decision_needed/patch/defer），将其作为评估参考：
            - `decision_needed`：重点评估是否确实需要人工裁决
            - `patch`：验证修复方案的可行性和完整性
            - `defer`：确认是否确实为既有问题而非本次改动引入
        - 对每条发现进行评估：
            - 问题描述是否准确？
            - 严重性判断是否合理？
            - 修复建议是否可行？
            - 是否存在误报（false positive）？
        - 如有明确异议，可参考过往轮次的《代码审查结果文件》进行交叉验证
        - 给出整体评估结论：
            - 哪些发现需要修复（分优先级）
            - 哪些发现可以忽略（说明理由）
            - 哪些发现需要进一步讨论
        - 生成数据：evaluation-findings（评估结论列表）

    Step 5：保存评估结果
        - 读取输出格式模板：`assets/output-format.md`
        - 按照模板中定义的章节结构生成评估文档
        - 确定今天日期，格式为 YYYYMMDD
        - 按 `references/cr-config.md` 中的文件名格式保存文件
        - 严格按照模板中定义的章节结构和格式规范输出，包括：
            - YAML 元信息头部（含 Review Source 和 Review Model）
            - 评估总结
            - 上轮问题回顾确认（被评估审查为复审时）
            - 逐条发现评估（审查原文、评估结论、评估分析）
            - 整体评估结论（需修复表格、CR TODO 表格、评估决定）
        - 向用户展示评估结论要点
        - 完成后返回："✅ CR 代码审查结果评估完成（第 m 轮），结果已保存"

[注意事项]
    - **绝对禁止**修改任何源码文件
    - **绝对禁止**修改 Story 文档内容
    - **绝对禁止**自行执行修复操作
    - 只对最新一轮（n 值最大）的《代码审查结果文件》进行评估
    - 只有在有明确异议时才允许参考过往轮次的《代码审查结果文件》
    - 路径约定和文件名格式以 `references/cr-config.md` 为准，不硬编码
    - 始终使用中文输出评估结果
    - 评估要客观公正，对误报要明确标注并给出理由
    - 审查结果中的「来源」和「分类」字段为可选增强信息，若存在则利用其辅助评估，若不存在则按原有逻辑评估
    - 输出文件头部的 `Model Used` 字段必须如实填写当前执行评估的模型名称；`Review Model` 字段从被评估的审查结果文件头部读取，便于跨 LLM 追溯
    - 如果找不到审查结果文件，立即停止并告知用户
