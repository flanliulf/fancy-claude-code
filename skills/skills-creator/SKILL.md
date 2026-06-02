---
name: skills-creator
description: "Interactive Skill development assistant that creates complete Agent Skills packages through structured dialogue. Use when user mentions 'create skill', 'new skill', 'build skill', 'generate skill', 'skill creator', 'skill development', 'skill pack', '创建 skill', '新建技能', '生成技能', '开发技能', '技能创建', '创建技能包', '帮我做个 Skill', or wants to create SKILL.md files, agent skills, or automate workflow packaging. Capable of progressive disclosure architecture design, five workflow pattern matching, YAML frontmatter generation, reference document structuring, Python/Shell script scaffolding, and trigger testing guidance."
allowed-tools: Read, Write, Bash, Grep, Glob
metadata:
  version: "1.5.0"
  author: "fancyliu"
  catalog: "skill-tooling"
---

[Overview（技能说明）]
    通过结构化交互对话创建符合 Anthropic Skills 开放标准的完整 Agent Skills 包。它把用户需求转化为标准化的 SKILL.md、SKILL.en.md、CHANGELOG.md、references/、scripts/ 和 assets/，并用脚本化 Workflow density gate 保证入口文件符合渐进式披露思想。

[Core Capabilities（核心能力）]
    - **需求挖掘**：一次最多提问 3 个，收集名称、目标、触发词、输入输出、catalog 和执行步骤。
    - **工作流匹配**：根据业务特征推荐顺序、多 MCP、迭代、上下文感知或领域专有模式，详见 `references/workflow-patterns.md`。
    - **规范转译**：生成三段式 description、kebab-case name、allowed-tools，并按 metadata 字段契约写入 `metadata.version`、`metadata.author` 和可选 `metadata.catalog`。
    - **双语入口生成**：生成中文 canonical `SKILL.md` 与英文 mirror `SKILL.en.md`，保持 YAML、版本、目录和执行语义一致。
    - **Workflow density gate**：使用 deterministic 脚本统计正文长度、Workflow 长度和占比，命中阈值时抽取 workflow reference。
    - **渐进式文件组织**：按 SKILL.md、SKILL.en.md、CHANGELOG.md、references/、scripts/、assets/ 分配核心指令、详细资料、脚本和模板。
    - **质量与测试指导**：控制正文长度、语言规则、命名规范、生成标注和触发测试建议。

[Workflow（执行流程）]
    本 Skill 采用需求收集→结构规划→文件生成→density gate→总结交付的顺序工作流。完整步骤见 `references/skill-creation-workflow.md`。

    Step 1：收集并确认需求
        读取 `references/skill-creation-workflow.md` 的 Requirement Collection 部分，按最多 3 个问题一组收集信息，并在生成前展示确认清单。

    Step 2：规划文件结构并生成入口
        先写入 `forge/<catalog>/<skill-name>/` 或 `forge/<skill-name>/`。生成 SKILL.md、SKILL.en.md、CHANGELOG.md，并按需生成 references/、scripts/、assets/。

    Step 3：运行 Workflow density gate
        生成草稿后，优先调用已安装 `skills-lint` 的 `scripts/check_skill_density.py`；在本仓库源码中使用 `python3 forge/skill-tooling/skills-lint/scripts/check_skill_density.py <skill-dir>`。脚本结果是唯一判断来源。

    Step 4：按 gate 结果拆分 Workflow
        若任一入口文件满足 `workflow_chars > 1500` 且 `workflow_ratio > 0.5`，必须创建 `references/<skill-name>-workflow.md` 或等价 workflow reference。入口 Workflow 只保留阶段摘要、何时读取 reference 和关键停止条件。

    Step 5：完成总结
        展示文件树、渐进式披露分层、触发测试建议、版本信息和后续通过 `skills-lint` / `skills-upgrade` 收敛的入口。

[Notes（注意事项）]
    - SKILL.md 是中文 canonical 文档，正文使用中文；章节标题使用 English（中文）形式；命令、路径、字段名、fixture 名称、schema/issue id 等技术标识使用英文。
    - SKILL.en.md 是英文 mirror，不得新增中文入口没有的能力、步骤、限制或触发条件。
    - 每个 Skill 必须包含 SKILL.md、SKILL.en.md 和 CHANGELOG.md，版本号保持同步。
    - 中文与英文入口正文分别控制在 5000 字以内；Workflow density gate 是 Warning 级质量规则，但创建时命中必须拆分。
    - YAML frontmatter 只允许 name、description、license、allowed-tools、metadata，且不得包含 XML 尖括号或代码执行逻辑。
    - metadata 仅支持 `version`、`author`、`catalog`：`version` 和 `author` 必填，`catalog` 在 Skill 归入 catalog 时填写并与路径及 mirror 对齐。
    - 目录和 name 字段必须使用 kebab-case，禁止保留前缀 claude-*、codex-*、anthropic-*。
    - 运行产物写入 output/，过程分析文档写入 docs/analysis/，不得散落在项目根目录。
    - 如需安装测试，只同步到实际存在的安装根；不得凭空创建 `.codex/skills`。

[Generation Metadata（生成信息）]
    本 Skill 由 skills-creator 自动生成。如需修改，必须同步更新 SKILL.md 与 SKILL.en.md，并同步 forge/ 与实际安装副本，或通过 skills-upgrade 管理版本。
