---
name: bmenhance-cr-03-fixer
description: "Execute code fixes based on code review evaluation conclusions and append fix summary to the evaluation document. Use when user mentions 'CR fix', 'CR repair', 'execute fix', 'apply CR fixes', 'code review fix', '执行修复', 'CR 修复', '修复 CR 问题', '执行 CR 修正', '代码审查修复', or wants to implement fixes from CR evaluation. Capable of reading evaluation conclusions, executing targeted code fixes, and recording fix summaries in evaluation documents."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
metadata:
  version: "1.0.1"
---

[技能说明]
    根据代码审查结果评估的结论执行代码修复，并将修复执行总结追加到评估文档中。是跨 LLM 代码审查工作流中唯一允许修改源码的环节。

[核心能力]
    - **评估驱动修复**：严格按照《代码审查结果评估文件》的结论执行修复，不自行扩大修复范围
    - **自动定位评估文件**：自动扫描并定位最新一轮的《代码审查结果评估文件》
    - **精准定点修复**：针对评估确认需要修复的问题逐一处理
    - **修复记录追踪**：将修复执行总结追加到评估文件的指定章节
    - **修复验证**：修复后验证代码编译/运行是否正常

[执行流程]
    路径约定和文件名格式以 `references/cr-config.md` 为准。

    Step 1：定位最新评估文件
        - 接收用户指定的 Story 标识
        - 读取 `references/cr-config.md` 获取路径约定
        - 按配置中的 Story ID 规则提取 `{story-id}`
        - 按配置中的代码审查目录格式确定路径
        - 按配置中的审查评估文件名格式，扫描 code-review-dir 下匹配的文件
        - 找到 round 值（n）最大的文件作为修复依据
        - 读取该文件的完整内容，提取需要修复的问题列表
        - 生成数据：evaluation-file-path、fix-items（待修复问题列表）

    Step 2：制定修复计划
        - 根据评估结论中"需要修复"的条目，制定修复计划
        - 按优先级排序修复顺序
        - 确认每个修复项的：
            - 涉及的文件和代码位置
            - 具体修复方案
            - 预期效果
        - 向用户展示修复计划供确认
        - 生成数据：fix-plan（修复计划）

    Step 3：逐项执行修复
        - 按修复计划逐项执行代码修改
        - 每项修复完成后记录：
            - 修改了哪些文件的哪些位置
            - 修改前后的关键差异
            - 修复是否成功
        - 生成数据：fix-results（修复执行结果列表）

    Step 4：记录修复总结
        - 将修复执行总结整理为结构化内容
        - 将总结内容**追加**到最新一轮《代码审查结果评估文件》的 "## 修复执行记录" 章节中
        - 如果该章节不存在，在文件末尾创建该章节
        - 修复执行记录的开头必须包含元信息：
            ```
            ### 修复执行记录
            - **Date**: <YYYY-MM-DD>
            - **Model Used**: <当前执行本次修复的模型名称，如 Claude Opus 4、GPT-4o 等>
            - **Fix Items**: <修复条目数>
            ```
        - 完成后返回："✅ CR 修复执行完成，修复记录已追加到评估文件"

[注意事项]
    - 只修复评估结论中明确标记为"需要修复"的问题，禁止自行扩大修复范围
    - **禁止**修改 Story 文档内容
    - 修复总结追加到最新一轮（n 值最大）的《代码审查结果评估文件》中
    - 路径约定和文件名格式以 `references/cr-config.md` 为准，不硬编码
    - 始终使用中文输出修复记录
    - 如果某项修复无法完成（如缺少上下文信息），标记为"待确认"并说明原因
    - 修复后如有条件应运行相关测试验证修复效果
    - 修复执行记录中的 `Model Used` 字段必须如实填写当前执行修复的模型名称，便于跨 LLM 追溯
    - 如果找不到评估文件，立即停止并告知用户
