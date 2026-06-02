---
name: skills-creator
description: "Interactive Skill development assistant that creates complete Agent Skills packages through structured dialogue. Use when user mentions 'create skill', 'new skill', 'build skill', 'generate skill', 'skill creator', 'skill development', 'skill pack', '创建 skill', '新建技能', '生成技能', '开发技能', '技能创建', '创建技能包', '帮我做个 Skill', or wants to create SKILL.md files, agent skills, or automate workflow packaging. Capable of progressive disclosure architecture design, five workflow pattern matching, YAML frontmatter generation, reference document structuring, Python/Shell script scaffolding, and trigger testing guidance."
allowed-tools: Read, Write, Bash, Grep, Glob
metadata:
  version: "1.5.0"
  author: "fancyliu"
  catalog: "skill-tooling"
---

[Overview]
    Creates complete Agent Skills packages through structured interaction. It converts requirements into standardized SKILL.md, SKILL.en.md, CHANGELOG.md, references/, scripts/, and assets/, using a scripted Workflow density gate to keep entry files concise.

[Core Capabilities]
    - **Requirement discovery**: Ask at most 3 questions at a time to collect name, goal, trigger terms, inputs, outputs, catalog, and workflow steps.
    - **Workflow matching**: Recommend sequential, multi-MCP, iterative, context-aware, or domain-specific patterns. See `references/workflow-patterns.md`.
    - **Specification translation**: Generate three-part description, kebab-case name, allowed-tools, and metadata fields: `metadata.version`, `metadata.author`, and optional `metadata.catalog`.
    - **Bilingual entry generation**: Generate canonical Chinese SKILL.md and English mirror SKILL.en.md with aligned YAML, versions, directories, and execution semantics.
    - **Workflow density gate**: Use a deterministic script to count body length, Workflow length, and ratio, then extract workflow references when thresholds are triggered.
    - **Progressive file organization**: Allocate core instructions, detailed knowledge, scripts, and templates across SKILL.md, SKILL.en.md, CHANGELOG.md, references/, scripts/, and assets/.
    - **Quality and testing guidance**: Enforce body length, language rules, naming rules, generation metadata, and trigger test suggestions.

[Workflow]
    This Skill follows a sequential flow: collect requirements, plan structure, generate files, run density gate, and summarize delivery. Full steps are in `references/skill-creation-workflow.md`.

    Step 1: Collect and confirm requirements
        Read the Requirement Collection section in `references/skill-creation-workflow.md`. Ask at most 3 questions at a time and show a confirmation checklist before generation.

    Step 2: Plan file structure and generate entries
        Write first to `forge/<catalog>/<skill-name>/` or `forge/<skill-name>/`. Generate SKILL.md, SKILL.en.md, CHANGELOG.md, and optional references/, scripts/, and assets/.

    Step 3: Run Workflow density gate
        After drafting files, prefer the installed `skills-lint` `scripts/check_skill_density.py`; in this repository use `python3 forge/skill-tooling/skills-lint/scripts/check_skill_density.py <skill-dir>`. The script result is the only decision source.

    Step 4: Extract Workflow when needed
        If any entry file satisfies `workflow_chars > 1500` and `workflow_ratio > 0.5`, create `references/<skill-name>-workflow.md` or an equivalent workflow reference. Keep only phase summary, reference loading conditions, and stop conditions in the entry Workflow.

    Step 5: Summarize completion
        Show the file tree, progressive disclosure layers, trigger test suggestions, version information, and follow-up entry points through `skills-lint` and `skills-upgrade`.

[Notes]
    - SKILL.md is the canonical Chinese document with English-Chinese section headings, Chinese body content, and English technical identifiers.
    - SKILL.en.md is an English mirror and must not add capabilities, steps, limits, or trigger conditions absent from SKILL.md.
    - Every Skill must include SKILL.md, SKILL.en.md, and CHANGELOG.md with synchronized versions.
    - Chinese and English entry bodies must each stay under 5000 characters; Workflow density gate is a Warning-level quality rule, but creation must extract Workflow when triggered.
    - YAML frontmatter allows only name, description, license, allowed-tools, and metadata, and must not contain XML angle brackets or executable logic.
    - metadata supports only `version`, `author`, and `catalog`: `version` and `author` are required, while `catalog` is set when the Skill belongs to a catalog and must align with the path and mirror.
    - Directory and name fields must be kebab-case and must not use reserved prefixes claude-*, codex-*, or anthropic-*.
    - Runtime outputs go under output/, process analysis documents go under docs/analysis/, and neither should be scattered in the repository root.
    - Install test copies only into existing install roots; do not create `.codex/skills` when it does not exist.

[Generation Metadata]
    This Skill was generated by skills-creator. Update SKILL.md and SKILL.en.md together, and sync forge/ with installed copies or manage versions through skills-upgrade.
