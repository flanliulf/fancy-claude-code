---
name: bmenhance-sr-03-fixer
description: "Execute Story document revisions based on SR evaluation conclusions and append revision summary to the evaluation document. Use when user mentions 'SR fix', 'SR revise', 'story revision', 'apply SR fixes', 'story review fix', 'design fix', '执行修订', 'SR 修订', '修订 Story', '执行 SR 修正', 'Story 设计修订', '修订 Story 文档', or wants to implement revisions from SR evaluation. Capable of reading evaluation conclusions, executing targeted document revisions, and recording revision summaries in evaluation documents."
allowed-tools: Read, Write, Edit, Grep, Glob
metadata:
  version: "1.0.0"
  author: "fancyliu"
---

[技能说明]
    根据 Story 设计审查评估的结论执行 Story 文档修订，并将修订执行总结追加到评估文档中。是 SR 审查工作流中唯一允许修改 Story 文档的环节。

[核心能力]
    - **评估驱动修订**：严格按照审查评估文件的结论执行修订，不自行扩大修订范围
    - **自动定位评估文件**：自动扫描并定位最新一轮的审查评估文件
    - **双粒度适配**：自动从评估文件的 Scope 字段识别粒度，适配 Epic 和 Story 两种模式的修订范围
    - **精准定点修订**：针对评估确认需要修订的问题逐一处理
    - **修订记录追踪**：将修订执行总结追加到评估文件的指定章节
    - **范围边界控制**：Story 模式下仅修改指定 Story 文件，超出范围的修订标记为"超出范围"提醒用户

[执行流程]
    路径约定和文件名格式以 `references/sr-config.md` 为准。

    Step 1：定位最新评估文件
        - 接收用户指定的 Epic 或 Story 标识
        - 读取 `references/sr-config.md` 获取路径约定和双粒度判定规则
        - 根据用户输入判定 `$review_scope`
        - 按 `$review_scope` 确定 `$sr_dir`
        - 按配置中的审查评估文件名格式，扫描 `$sr_dir` 下匹配的文件
        - 找到 round 值最大的文件作为修订依据
        - 读取该文件的完整内容，提取需要修订的问题列表
        - 从 YAML 头部 `Scope` 字段确认粒度
        - 生成数据：`$evaluation_file_path`、`$fix_items`（待修订问题列表）

    Step 2：制定修订计划
        - 根据评估结论中"需要修订"的条目，制定修订计划
        - 按优先级排序修订顺序
        - 确认每个修订项的：
            - 涉及的 Story 文件和章节
            - 具体修订方案
            - 预期效果
        - 范围控制：
            - Epic 模式：可修改该 Epic 下多个 Story 文件，以及必要时的 Epic 定义文件和架构文档
            - Story 模式：仅修改该单个 Story 文件；如评估指出需修改 Epic 文件或架构文档，标记为"⚠️ 超出范围 — 需在 Epic 模式下处理"
        - 向用户展示修订计划供确认
        - 生成数据：`$fix_plan`（修订计划）

    Step 3：逐项执行修订
        - 按修订计划逐项执行文档修改
        - 每项修订完成后记录：
            - 修改了哪个文件的哪个章节
            - 修改前后的关键差异
            - 修订是否成功
        - 生成数据：`$fix_results`（修订执行结果列表）

    Step 4：记录修订总结
        - 将修订执行总结整理为结构化内容
        - 将总结内容**追加**到最新一轮审查评估文件的 "## 修订执行记录" 章节中
        - 如果该章节不存在，在文件末尾创建该章节
        - 修订执行记录的开头必须包含元信息：
            ```
            ### 修订执行记录
            - **Date**: <YYYY-MM-DD>
            - **Model Used**: <当前执行本次修订的模型名称>
            - **Fix Items**: <修订条目数>
            ```
        - 逐项记录：
            ```
            #### 修订项 #{n}: {问题标题}
            - **文件**: {修改的文件路径}
            - **章节**: {修改的章节}
            - **修改摘要**: {修改前后的关键差异}
            - **状态**: {已完成 / 待确认}
            ```
        - 完成后返回："✅ SR 修订执行完成，修订记录已追加到评估文件"

[注意事项]
    - 只修订评估结论中明确标记为"需要修订"的问题，禁止自行扩大修订范围
    - **禁止**修改任何源码文件
    - 修订总结追加到最新一轮（round 值最大）的审查评估文件中
    - 路径约定和文件名格式以 `references/sr-config.md` 为准，不硬编码
    - 始终使用中文输出修订记录
    - 如果某项修订无法完成（如缺少上下文信息或超出范围），标记为"待确认"并说明原因
    - 修订后应重新检查修改内容与 Epic 定义和架构文档的一致性
    - 修订执行记录中的 `Model Used` 字段必须如实填写当前执行修订的模型名称，便于跨 LLM 追溯
    - 如果找不到评估文件，立即停止并告知用户
    - Story 模式下超出范围的修订项必须明确标记，不得静默跳过

[生成信息]
    本 Skill 由 skills-creator 自动生成。如需修改，建议同步更新 forge/ 和 .claude/skills/ 两份副本，或通过 skills-upgrade 管理版本。
