---
name: review-adversarial-general
description: Perform an adversarial review of code diffs, specs, stories, or any artifact, finding at least ten issues and outputting a Markdown findings list. Use when user mentions 'adversarial review', 'cynical review', 'critical review', 'blind review', 'blind hunter', 'review content', '对抗式审查', '批判性审查', '盲审', '找问题', '挑毛病', '审查内容', or asks for a harsh/skeptical review of any content. Capable of reviewing diffs, specs, story files, documents, and arbitrary artifacts with extreme skepticism, outputting structured findings.
allowed-tools: Read, Grep, Glob
metadata:
  version: "1.0.0"
---

[技能说明]
    以极度怀疑的态度对代码 diff、规格说明、故事文件、文档等任意制品进行对抗式审查，假设问题存在，找出至少十个需要修复或改进的问题，以 Markdown 列表格式输出发现报告。

[核心能力]
    - **对抗式分析**：以零容忍态度审查内容，假设提交者疏于验证，主动寻找遗漏、错误和不一致之处
    - **多类型内容支持**：支持审查代码 diff、规格说明、用户故事、设计文档、任意文本制品
    - **最小十条发现**：强制要求至少输出十条发现，防止审查流于表面
    - **可选领域聚焦**：支持通过 `also_consider` 参数指定额外关注领域，纳入审查维度
    - **结构化输出**：以 Markdown 列表格式输出，每条发现仅含描述，不含个人攻击或情绪化语言
    - **中止保护**：发现数为零时视为可疑，强制中止并要求重新分析

[执行流程]
    采用顺序工作流，共 3 步。

    Step 1：接收内容
        1. 从用户输入或当前上下文中加载待审查内容
        2. 若内容为空或不可读，立即中止并告知用户：「无法读取审查内容，请提供有效的 diff、文档或文件路径后重试。」
        3. 识别内容类型（代码 diff / 规格说明 / 用户故事 / 普通文档 / 其他制品），作为后续分析的参考维度

    Step 2：对抗式分析
        1. 以极度怀疑的审查者身份切入：假设内容存在问题，主动寻找而非被动发现
        2. 重点审查维度（根据内容类型适配）：
           - 遗漏：缺少的错误处理、边界条件、测试、文档
           - 错误：逻辑错误、类型错误、不安全假设
           - 不一致：命名不统一、风格不一致、与规格的偏差
           - 风险：潜在的安全隐患、性能问题、可维护性缺陷
           - 模糊：定义不清、行为未明确、缺少上下文
        3. 若用户提供了 `also_consider` 参数，将其中的领域纳入上述分析维度
        4. 收集发现，确保总数不少于十条

    Step 3：输出发现
        1. 以 Markdown 无序列表格式输出所有发现，每条仅含一行描述
        2. 若发现总数为零：立即中止，提示：「零发现结果可疑，正在重新分析……」并返回 Step 2 重新执行
        3. 输出格式示例：
           - 缺少对空指针的防御性检查，可能导致运行时崩溃
           - 函数命名与实际行为不符，误导阅读者
           - 未处理网络请求超时的情况

[注意事项]
    - 发现报告只包含描述，不含个人攻击、情绪化语言或主观评分
    - 零发现是可疑信号，必须强制重新分析，不得直接报告"未发现问题"
    - 内容为空或不可读时立即中止，不猜测内容
    - `also_consider` 为可选输入，缺省时按标准对抗式维度审查
    - 本 Skill 为并行代码审查流程中的"盲猎手"角色，不接收项目上下文，只接收待审查内容本身
