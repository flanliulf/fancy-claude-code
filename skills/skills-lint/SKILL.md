---
name: skills-lint
description: "Validate Agent Skills against Anthropic open standard specifications, checking YAML frontmatter, file naming, description quality, version consistency, and content constraints. Use when user mentions 'skills-lint', 'lint skill', 'validate skill', 'check skill', 'skill lint', 'skill check', 'skill validation', '检查 Skill', '检查 Skill 规范', '验证技能', 'Skill 规范检查', 'Skill 合规检查', '技能验证', '检查技能格式', or wants to audit an existing Skill for compliance. Capable of YAML violation detection, naming convention verification, bilingual trigger keyword coverage analysis, version mismatch identification, forbidden file scanning, and structured report generation."
allowed-tools: Read, Bash, Grep, Glob
metadata:
  version: "2.3.0"
  author: "fancyliu"
  catalog: "skill-tooling"
---

[Overview（技能说明）]
    纯只读的 Skill 规范检查器，对指定 Skill 目录执行 34 条合规规则扫描，生成结构化检查报告。不修改任何文件，仅报告问题并提供修复建议。完整规则见 `references/check-rules.md`，详细扫描流程见 `references/lint-workflow.md`。

[Core Capabilities（核心能力）]
    - **YAML 头部验证**：检查 name、description、allowed-tools、metadata 字段契约和安全边界是否符合开放标准。
    - **description 质量分析**：验证三段式结构、中英文双语触发词覆盖、触发词具体性和尖括号安全。
    - **文件结构合规**：检查 SKILL.md、SKILL.en.md、CHANGELOG.md、目录命名、README.md 禁止项和保留前缀。
    - **版本与 mirror 一致性**：验证 SKILL.md、SKILL.en.md、CHANGELOG.md 的版本、YAML 和引用路径同步。
    - **正文与 Workflow density 检查**：统计正文长度、Workflow 长度和占比，识别需要抽到 references/ 的过重流程。
    - **命名与文件分类检查**：检查 references/、scripts/、assets/ 的命名和职责边界。
    - **结构化报告输出**：按 Error 与 Warning 输出规则表、摘要和具体修复建议。

[Workflow（执行流程）]
    本 Skill 采用扫描→报告→修复建议→重新扫描的迭代模式。完整步骤见 `references/lint-workflow.md`；入口仅保留阶段路由，执行细则以 reference 为准。

    Step 1：定位目标 Skill
        接收完整目录、Skill 名称或"所有 Skill"。按 `forge/`、`.claude/skills/`、`.agents/skills/`、`.codex/skills/` 的实际存在目录搜索，目标必须包含 SKILL.md。

    Step 2：读取规则与统计密度
        读取 `references/check-rules.md` 和 `references/lint-workflow.md`。对目标目录运行只读脚本：
        `python3 scripts/check_skill_density.py <skill-dir>`
        使用脚本 JSON 结果作为 BODY-07 与 BODY-08 的唯一判断来源。

    Step 3：执行 34 条规则扫描
        按 `references/lint-workflow.md` 的分组流程检查 YAML、description、文件结构、版本、正文、命名、mirror、分类和 Workflow density。不得修改目标文件。

    Step 4：输出报告并支持复查
        输出标准表格：规则 ID、检查项、状态、详情、修复建议。用户修复后说"重新检查"、"re-lint"或"再查一次"时，重新执行 Step 2-4 并标注已修复和新增问题。

[Notes（注意事项）]
    - 本 Skill 只读，绝不修改文件；Bash 仅可用于运行 `scripts/check_skill_density.py` 这类只读统计脚本。
    - Error 表示硬性合规问题；Warning 表示质量、可维护性或渐进式披露风险。
    - BODY-07 阈值固定为 `workflow_chars > 1500` 且 `workflow_ratio > 0.5`；BODY-08 在命中 BODY-07 且无 workflow reference 时提示抽取。
    - 新建或更新后的 Skill 必须包含中文 canonical `SKILL.md` 与英文 mirror `SKILL.en.md`。
    - 中文 SKILL.md 的章节标题必须使用 English（中文）形式，正文内容使用中文，命令、路径、字段名、fixture 名称、schema/issue id 等技术标识和专有技术术语使用英文。
    - 检查完成后如有修改，建议运行 `skills-upgrade` 同步版本号和 CHANGELOG。
