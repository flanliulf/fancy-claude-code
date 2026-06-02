---
name: review-edge-case-hunter
description: Exhaustively enumerate every branching path and boundary condition in code diffs, files, or functions, reporting only unhandled edge cases as a JSON array. Use when user mentions 'edge case', 'edge case hunter', 'boundary conditions', 'path analysis', 'unhandled cases', 'exhaustive review', '边界条件', '边缘情况', '路径分析', '未处理情况', '边界审查', '穷举分析', or needs orthogonal mechanical path-tracing review. Capable of scanning diffs, full files, and functions; outputs structured JSON with location, trigger condition, guard snippet, and potential consequence for each finding.
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
---

[技能说明]
    以纯路径追踪方式对代码 diff、完整文件或函数进行穷举式边界条件分析，机械地遍历每条分支路径，仅报告缺少处理的边缘情况，以结构化 JSON 数组格式输出。与对抗式审查正交——方法驱动，不是态度驱动。

[核心能力]
    - **穷举路径枚举**：机械遍历所有分支路径和边界条件，不依赖直觉猜测
    - **差异范围限制**：提供 diff 时仅扫描 diff 块，只报告直接可达且缺少显式防守的边界
    - **全文件/函数模式**：未提供 diff 时将整个内容作为分析范围
    - **仅报告未处理路径**：已处理的路径静默丢弃，输出无噪音
    - **JSON 结构化输出**：每条发现包含 location、trigger_condition、guard_snippet、potential_consequence 四个字段
    - **可选领域聚焦**：支持 `also_consider` 参数，将指定领域纳入分析维度
    - **完整性二次验证**：Step 3 对 Step 2 的边缘类别进行复查，确保无遗漏

[执行流程]
    采用顺序工作流，共 4 步。执行顺序不可更改。

    Step 1：接收内容
        1. 严格从用户提供的输入中加载待审查内容
        2. 若内容为空或无法解码为文本，立即返回以下 JSON 并停止：
           [{"location":"N/A","trigger_condition":"输入为空或无法解码","guard_snippet":"请提供有效内容后重试","potential_consequence":"审查已跳过，未执行任何分析"}]
        3. 识别内容类型（代码 diff / 完整文件 / 函数），确定后续分析的范围规则：
           - diff → 仅分析 diff 块中直接可达的边界
           - 完整文件/函数 → 将整个内容作为分析范围

    Step 2：穷举路径分析
        对范围内的每条分支路径和边界条件进行完整遍历，仅报告未处理的路径。

        1. 若用户提供了 `also_consider` 参数，将其指定领域纳入分析维度
        2. 遍历所有分支路径：
           - 控制流：条件分支（if/else/switch）、循环、错误处理器、提前返回
           - 领域边界：值/状态/条件发生转变的地方
        3. 从内容本身推导相关边缘类别，不依赖固定清单。典型示例：
           - 缺少 else/default 分支
           - 未防守的输入（null、空、超出范围）
           - 循环的差一错误（off-by-one）
           - 算术溢出
           - 隐式类型转换
           - 竞态条件
           - 超时间隙
        4. 对每条路径判断内容是否已处理
        5. 仅收集未处理的路径作为发现——已处理的路径静默丢弃

    Step 3：完整性验证
        1. 重新审视 Step 2 中识别的每个边缘类别
        2. 将新发现的未处理路径加入发现列表；将确认已处理的路径丢弃
        3. 确保输出完整，不存在遗漏的类别

    Step 4：输出发现
        1. 严格按以下格式输出 JSON 数组，每个对象包含且仅包含四个字段：
           - location：文件:起始行-结束行（单行用 文件:行号，无法确定精确行时用 文件:块编号）
           - trigger_condition：一行描述（最多 15 个词）
           - guard_snippet：修复该缺口的最小代码草图（单行转义字符串，无原始换行或未转义引号）
           - potential_consequence：实际可能出错的内容（最多 15 个词）
        2. 无额外文字、无解释、无 Markdown 包装
        3. 无未处理路径时输出空数组 [] 是合法结果

[注意事项]
    - 执行步骤顺序不可更改，不可跳过任何步骤
    - 仅追踪路径和边界条件，不评价代码质量好坏
    - 已处理的路径必须静默丢弃，不出现在输出中
    - 输出仅为纯 JSON 数组，无任何额外包装或说明文字
    - 空数组 [] 是合法输出，表示范围内所有路径均已处理
    - 本 Skill 与对抗式审查（review-adversarial-general）正交，两者配合使用覆盖不同审查维度
