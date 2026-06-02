---
name: bmenhance-cr-05-todo-tracker
description: "Manage CR TODO backlog — add, check, resolve, and list deferred improvement items from code reviews. Use when user mentions 'CR TODO', 'add TODO', 'check TODO', 'resolve TODO', 'list TODO', 'CR backlog', 'extract todos', 'CR 待办', '添加 TODO', '检查 TODO', '解决 TODO', '查看 TODO', 'CR 延迟事项', '批量提取 TODO', or wants to track non-blocking improvements identified during code reviews."
allowed-tools: Read, Write, Glob, Grep, Edit
metadata:
  version: "1.2.1"
---

[技能说明]
    管理 `_bmad-output/implementation-artifacts/cr-rules/cr-todo-backlog.md` 中的跨 Story 延迟事项。
    支持从 CR 评审中提取待办、按上下文检查相关待办、标记完成并归档。
    本技能只管理追踪文档，不直接修改源代码。

[核心能力]
    - **添加条目** (add)：从 CR evaluation/summary 中提取非阻塞改进项，生成标准格式条目
    - **检查相关条目** (check)：根据当前 story 涉及的文件或指定路径，查找匹配的 open 条目
    - **标记解决** (resolve)：将条目状态改为 resolved 并填写解决记录，从 Open 移至 Resolved
    - **查看摘要** (list)：展示当前所有 open/in-progress 条目的概览
    - **批量提取** (extract)：从指定 story 的所有 CR 文件中批量识别可延迟项

[执行流程]

    路径约定和文件名格式以 `references/cr-config.md` 为准。

    ### 模式 A：添加条目 (add)

    Step 1：确定 CR 来源
        - 用户提供 story-id 或 CR 文件路径
        - 读取 `references/cr-config.md` 获取路径约定
        - 按配置中的代码审查目录格式定位 CR 文件目录
        - 读取最新一轮的审查评估文件或审查总结文件（按配置中的文件名格式匹配）
        - 生成数据：cr-source-file

    Step 2：识别延迟候选项
        - 从 CR 文件中筛选出标注为以下特征的改进项：
            - "非阻塞"、"建议后续"、"不阻塞合并"
            - "其他建议"、"持续建议"
            - 评估结论中标记为 "📝 记录" 或 "后续改善"
        - 排除已标记为"必须修复"、"需要修复"的阻塞项
        - 向用户展示候选项列表，确认哪些应加入 TODO backlog
        - 生成数据：confirmed-items

    Step 3：生成条目
        - 读取 `cr-todo-backlog.md`，找到当前最大编号
        - 为每个确认的条目分配递增编号（最大编号 + 1）
        - 读取条目格式模板：`assets/output-format.md` 中的"单个条目格式"
        - 按模板填充所有必填字段：
            - `来源`：从 CR 文件头部元信息提取 story-id、round、date（提取规则见模板）
            - `优先级`：根据影响范围和紧迫程度建议，由用户确认
            - `类别`：从预定义枚举中选择（refactor / duplication / tech-debt / naming / test-gap / other）
            - `涉及文件`：从 CR 文件的位置信息中提取，使用项目相对路径
            - `建议时机`：根据涉及文件和问题性质建议，必须具体可操作
        - 生成数据：new-entries

    Step 4：写入文档
        - 将新条目插入 `## Open Items` 区域，按优先级排序（P1 在前）
        - 更新顶部统计摘要表的数字
        - 生成数据：updated-backlog

    Step 5：输出确认
        - 展示新增条目的摘要列表
        - 返回："✅ 已添加 N 条 TODO 到 cr-todo-backlog.md"

    ### 模式 B：检查相关条目 (check)

    Step 1：确定检查范围
        - 接收用户指定的 story-id 或文件路径列表
        - 如果指定 story-id：读取该 Story 文件获取涉及文件列表（从 File List 章节）
        - 如果指定文件路径：直接使用
        - 生成数据：check-paths

    Step 2：匹配 open 条目
        - 读取 `cr-todo-backlog.md`
        - 对每个 open/in-progress 条目的 `涉及文件` 字段做路径匹配
        - 同时检查 `建议时机` 字段是否匹配当前上下文
        - 生成数据：matched-entries

    Step 3：输出报告
        - 列出所有匹配的条目（编号、标题、优先级、建议时机）
        - P1 条目用 ⚠️ 标记，明确提醒"本 story 建议处理"
        - 如无匹配：返回 "✅ 无相关待办事项"
        - 如有匹配：返回 "📋 发现 N 条相关待办事项" + 详细列表

    ### 模式 C：标记解决 (resolve)

    Step 1：接收信息
        - 用户提供 TODO 编号（如 TODO-001）
        - 用户提供解决信息（在哪个 story 中解决、commit/PR 引用）

    Step 2：更新条目
        - 在 `cr-todo-backlog.md` 中找到对应条目
        - 将 `状态` 从 open/in-progress 改为 resolved
        - 填写 `解决记录` 字段

    Step 3：归档
        - 将条目从 `## Open Items` 移至 `## Resolved Items`
        - 更新顶部统计摘要表的数字

    Step 4：输出确认
        - 返回："✅ TODO-{NNN} 已标记为 resolved"

    ### 模式 D：查看摘要 (list)

    Step 1：读取文档
        - 读取 `cr-todo-backlog.md`

    Step 2：输出摘要
        - 按优先级分组输出所有 open + in-progress 条目
        - 每条显示：编号、标题、优先级、来源 story、涉及文件
        - 显示统计数字（open / in-progress / resolved）

    ### 模式 E：批量提取 (extract)

    Step 1：收集 CR 文件
        - 接收用户指定的 story-id
        - 按配置中的代码审查目录格式定位 CR 文件目录，Glob 搜索目录下所有 CR 文件

    Step 2：逐文件识别候选
        - 对每个 CR evaluation/summary 文件执行模式 A 的 Step 2
        - 跨文件去重（同一问题在多轮中出现只记一条）

    Step 3：合并确认
        - 向用户展示去重后的候选列表
        - 确认后批量执行模式 A 的 Step 3-5

[注意事项]
    - **只追踪非阻塞项**：阻塞性问题必须在当前 story 的 CR 流程中解决，不进入此 backlog
    - **编号不复用**：resolved 的编号永远保留，新条目继续递增，确保可追溯性
    - **路径使用项目相对路径**：`涉及文件` 字段使用相对于项目根目录的路径（如 `src/commands/init.ts`）
    - **中文输出**：所有条目内容和交互输出均使用中文
    - **不自动修改代码**：本技能仅管理追踪文档，不直接修改源代码
    - **确认机制**：添加条目前必须与用户确认候选项，不擅自写入
    - **优先级定义**：P1 = 下次触及必处理；P2 = Epic 内处理；P3 = 择机处理
    - **类别枚举**：refactor / duplication / tech-debt / naming / test-gap / other
    - `cr-todo-backlog.md` 的默认位置以 `references/cr-config.md` 中的 CR 规则目录配置为准
    - 如果 backlog 文件不存在，按 `assets/output-format.md` 中的"文件初始化模板"自动创建
