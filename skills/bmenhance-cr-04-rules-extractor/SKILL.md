---
name: bmenhance-cr-04-rules-extractor
description: "Analyze historical code review, evaluation, and fix records to extract reusable development guidelines and best practices for project-level documentation. Use when user mentions 'extract CR rules', 'CR summary', 'extract CR guidelines', 'CR best practices', 'code review lessons', '提炼 CR 规则', 'CR 总结', '提取 CR 最佳实践', 'CR 经验总结', '代码审查规则提炼', '总结 CR 经验', or wants to distill patterns from CR history. Capable of analyzing multi-round CR findings, identifying recurring issues, and proposing updates to global project documents like project-context.md and architect.md."
allowed-tools: Read, Write, Edit, Grep, Glob
metadata:
    version: "1.2.1"
    author: "fancyliu"
---

[技能说明]
    从指定 Story 的历史代码审查、评估及修正记录中提炼共性问题和最佳实践，判断是否可以补充到项目全局文档中，避免同类问题在后续 Story 开发中重复出现。

[核心能力]
    - **CR 历史分析**：系统性阅读和分析 Story 的全部 CR 审查、评估及修正记录
    - **四桶分类感知**：识别审查结果中的「来源」和「分类」增强字段，按审查层维度（blind/edge/auditor）和四桶分类（decision_needed/patch/defer）进行交叉统计分析
    - **共性问题识别**：从多轮 CR 发现中识别重复出现的模式和共性问题
    - **规则提炼**：将共性问题转化为可操作的开发规约、指导原则或最佳实践
    - **量化升格判定**：用硬性门槛、评分矩阵和阈值去向判断规则是否值得升格为全局文档约束
    - **全局文档建议**：评估提炼的规则是否适合补充到 project-context.md、architect.md 等全局文档
    - **规则总结沉淀与模板化输出**：按 `assets/output-format.md` 初始化和追加 `cr-rules-summary.md`，保持字段、编号和同步状态一致
    - **结构化输出**：以清晰的结构输出分析结果和建议，供用户确认

[执行模式]
    - **analysis-only（默认）**：只读分析 CR 历史、提炼规则、给出量化判定和文档更新建议，不修改任何文件。
    - **apply-confirmed**：用户明确确认全局文档更新范围后，才按确认内容更新全局文档，并同步记录规则总结。
    - **record-only**：用户只要求沉淀 CR 规则时，仅更新 `cr-rules-summary.md`，不修改 project-context、architecture 或 CLAUDE 等全局文档。
    - 未获得用户明确确认前，禁止执行 `apply-confirmed` 或 `record-only` 写入动作。

[规则升格判定机制]
    每条候选规则必须按 `references/promotion-rules.md` 执行硬性门槛、6 维 0-2 分评分和阈值去向判定。输出时必须展示每条候选规则的评分、总分、建议去向和是否需要用户确认。

[执行流程]
    路径约定和文件名格式以 `references/cr-config.md` 为准。

    Step 1：收集 CR 历史记录
        - 接收用户指定的 Story 标识
        - 读取 `references/cr-config.md` 获取路径约定
        - 按配置中的 Story ID 规则提取 `{story-id}`
        - 按配置中的代码审查目录格式确定路径
        - 读取该目录下所有文件：
            - 按配置中的审查总结文件名格式匹配 CR 代码审查结果
            - 按配置中的审查评估文件名格式匹配 CR 评估结果（含 "## 修复执行记录" 章节）
        - 生成数据：all-cr-records（全部 CR 历史记录）

    Step 2：梳理各轮次模型信息
        - 从每个 CR 文件的头部元信息中提取 `Model Used` 字段
        - 构建模型使用时间线：哪一轮审查/评估/修复分别由哪个模型执行
        - 生成数据：model-timeline（模型使用记录）

    Step 3：分析 Findings 情况
        - 系统性分析所有 CR 发现（Findings），分类统计：
            - AC 验收标准审核摘要中的问题
            - 测试充分性相关问题
            - 质量门禁相关问题
            - 代码逻辑和设计问题
            - 安全性和性能问题
        - 若发现包含「来源」字段，按审查层维度统计各层的发现分布和命中率
        - 若发现包含「分类」字段，按四桶分类维度统计各分类的占比和修复率
        - 标记哪些问题在多轮 CR 中重复出现
        - 标记哪些问题的修复引入了新问题
        - 生成数据：findings-analysis（发现分析报告）

    Step 4：提炼共性规则
        - 从分析结果中提炼出 Story 开发过程中容易重复出现的共性问题
        - 将共性问题转化为以下形式：
            - **规避指南**：明确告诉开发者应避免什么
            - **指导原则**：描述推荐的做法和原因
            - **最佳实践**：提供可直接参照的代码模式或流程
            - **豁免说明**：记录合理的例外情况和豁免理由
        - 生成数据：extracted-rules（提炼的规则列表）

    Step 5：执行规则升格判定
        - 对每条 extracted-rule 先检查硬性门槛，不通过则标记为“不沉淀”或“交给 05 TODO Tracker”
        - 对通过门槛的候选规则按 6 个维度逐项评分，计算总分
        - 按阈值去向给出建议：全局文档规则 / `cr-rules-summary.md` / 05 TODO Tracker / 不沉淀
        - 对建议升格为全局文档规则的候选项，记录建议写入的文档、章节和理由
        - 生成数据：promotion-decisions（规则升格判定表）

    Step 6：评估全局文档更新建议
        - 扫描项目中的全局文档（包括但不限于）：
            - `project-context.md`
            - `architect.md` 或 `architect/` 目录下的文档
            - `CLAUDE.md` 等开发指南文档
        - 对 promotion-decisions 中建议升格的规则，评估：
            - 是否已有等价或相近规则？
            - 应新增、补充细化还是不写入？
            - 适合补充到哪个全局文档和哪个章节？
            - 是否需要同步多份镜像文档或规则计数？
        - 生成数据：update-suggestions（文档更新建议列表）

    Step 7：输出总结供用户确认
        - 将分析结果、提炼的规则和文档更新建议整理为结构化总结
        - 包含以下部分：
            - 模型使用时间线（各轮次使用的模型及其角色）
            - CR Findings 概况统计（含审查层分布和四桶分类占比，如有）
            - 识别的共性问题（含出现频次）
            - 提炼的规则/指南/最佳实践
            - 规则升格判定表（硬性门槛、6 维评分、总分、建议去向）
            - 全局文档更新建议（含具体文档和章节）
            - 可选执行方案（例如：只记录规则总结 / 更新指定全局文档 / 暂不落地）
        - 向用户展示总结，等待确认后再执行任何写入动作
        - analysis-only 完成后返回："✅ CR 历史分析和规则提炼完成，请确认是否需要更新全局文档或记录规则总结"

    Step 8：按确认结果落地规则
        - 仅当用户明确确认后执行
        - 写入或更新 `cr-rules-summary.md` 前，必须读取 `assets/output-format.md` 获取文件初始化模板、Story 记录格式和单条规则格式
        - IF 用户选择 apply-confirmed：
            - 只更新用户确认范围内的全局文档
            - 若存在多份镜像文档或规则计数，必须同步更新并说明
            - 将最终升格结果记录到 `cr-rules-summary.md`
        - IF 用户选择 record-only：
            - 只更新 `cr-rules-summary.md`
            - 不修改全局文档
        - IF 用户只要求交给 TODO：
            - 输出交接给 05 TODO Tracker 的候选项，不在本 Skill 中写入 `cr-todo-backlog.md`
        - 生成数据：applied-rule-updates（已落地的规则更新）

    Step 9：输出落地结果
        - 展示实际修改的文件清单、每条规则的最终去向和未处理项
        - 如未执行写入，明确说明本次为只读分析
        - 完成后返回："✅ CR 规则提炼流程完成"

[注意事项]
    - 默认只输出分析结果和建议，不自动修改全局文档或规则总结，需等待用户明确确认
    - 确认后只能修改用户确认范围内的文档；不得顺手修改无关文件或扩大落地范围
    - 路径约定和文件名格式以 `references/cr-config.md` 为准，不硬编码
    - 始终使用中文输出
    - 提炼的规则要具体可操作，避免过于抽象的描述（如 "注意代码质量"）
    - 每条候选规则必须输出量化评分和建议去向，禁止只用主观描述判断是否升格
    - 如果某条规则只在特定技术栈或场景下适用，需要明确标注适用范围
    - 如果 CR 历史记录较少（只有 1 轮），可能不足以提炼共性规则，需如实告知用户
    - 避免将仅适用于当前 Story 的特殊情况泛化为全局规则
    - 首次创建或追加 `cr-rules-summary.md` 时，必须遵循 `assets/output-format.md`，不得临时自创字段结构
    - `cr-rules-summary.md` 只记录已验证、已解决或已确认可沉淀的复用规则；未解决的非阻塞改进项应交由 05 TODO Tracker 管理
    - 审查结果中的「来源」和「分类」字段为可选增强信息，若存在则利用其进行交叉统计分析，若不存在则按原有逻辑分析
