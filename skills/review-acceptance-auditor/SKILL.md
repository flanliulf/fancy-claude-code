---
name: review-acceptance-auditor
description: "Audit code changes against acceptance criteria (AC) from Story specifications, reporting violations, deviations, and unimplemented behaviors as a structured Markdown list. Use when user mentions 'acceptance audit', 'AC audit', 'AC review', 'acceptance criteria check', 'spec compliance', 'acceptance auditor', '验收审计', 'AC 审查', '验收标准检查', '验收对照', '规格合规审查', or needs to verify code against Story acceptance criteria. Capable of cross-referencing AC items with code changes, identifying spec violations and gaps, outputting structured findings with AC references and code evidence."
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
---

[技能说明]
    对照 Story 验收标准（AC）审查代码变更，检查实现是否违反验收条件、偏离规格意图、遗漏规格行为或存在矛盾，以结构化 Markdown 列表格式输出发现报告。与对抗式审查（review-adversarial-general）和边界条件分析（review-edge-case-hunter）正交——本 Skill 聚焦「规格合规性」维度。

[核心能力]
    - **AC 逐条对照**：将代码变更与 Story 验收标准逐条对照，确保每条 AC 均有对应实现
    - **违规检测**：识别违反验收条件的代码实现
    - **偏差检测**：识别偏离规格意图的行为
    - **缺失检测**：识别规格中指定但未实现的行为
    - **矛盾检测**：识别规格约束与实际代码之间的矛盾
    - **结构化输出**：每条发现包含一行标题、违反的 AC/约束引用、以及来自代码的证据（文件:行号）
    - **可选领域聚焦**：支持通过 `also_consider` 参数指定额外关注领域

[执行流程]
    采用顺序工作流，共 3 步。

    Step 1：接收内容
        1. 从用户输入或指定文件路径加载待审查内容（代码 diff 或完整文件内容）
        2. 从用户输入或指定文件路径加载验收标准（Story AC 章节内容）
        3. 若待审查内容为空或不可读，立即中止并告知用户：「无法读取审查内容，请提供有效的 diff 或文件路径后重试。」
        4. 若验收标准为空或不可读，立即中止并告知用户：「无法读取验收标准，请提供有效的 AC 内容后重试。」

    Step 2：AC 对照审查
        1. 逐条解析验收标准，建立 AC 检查清单
        2. 对每条 AC，在代码变更中查找对应实现
        3. 检查以下内容：
           - 违反验收条件的实现（代码行为与 AC 要求相反或不一致）
           - 偏离规格意图的行为（实现方式虽不违反字面 AC 但偏离了设计目的）
           - 未实现规格中指定的行为（AC 中要求但代码中找不到实现）
           - 规格约束与实际代码之间的矛盾（AC 间接暗示的约束被违反）
        4. 若用户提供了 `also_consider` 参数，将其中的领域纳入审查维度
        5. 收集所有发现

    Step 3：输出发现
        1. 以 Markdown 列表格式输出所有发现
        2. 每条发现包含三部分：
           - **一行标题**：简要描述问题
           - **AC 引用**：违反的具体验收标准条目或约束
           - **代码证据**：具体文件:行号，以及实际代码行为描述
        3. 输出格式示例：
           - **AC-3 的用户权限检查未实现** — 违反 AC: "管理员操作需要 admin 角色验证" — 证据: `src/api/admin.ts:28-35` 中 deleteUser 函数缺少角色检查
           - **搜索结果排序与规格不符** — 违反 AC: "默认按相关性降序排列" — 证据: `src/search/index.ts:142` 使用了创建时间排序
        4. 若无发现：返回空列表并说明所有 AC 均已覆盖

[注意事项]
    - 发现报告只包含客观事实描述，不含主观评分或情绪化语言
    - 每条发现必须引用具体的 AC 条目和代码位置，禁止模糊描述
    - 本 Skill 为并行代码审查流程中的"验收审计员"角色
    - 审查范围限于待审查内容和验收标准，不主动扩展到其他文件（除非通过 Grep/Glob 验证引用关系）
    - `also_consider` 为可选输入，缺省时仅按 AC 维度审查
