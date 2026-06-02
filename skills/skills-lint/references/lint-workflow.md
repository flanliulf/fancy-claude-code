# Skills Lint Workflow

## Overview（概述）

本文档承载 `skills-lint` 的详细扫描流程。入口 SKILL.md 只保留阶段路由；执行 34 条规则时按本文档逐组检查。若入口与本文档冲突，以本文档的执行细则为准。

## Target Discovery（目标定位）

支持三类输入：
- 完整目录路径，例如 `.claude/skills/skills-creator/`。
- Skill 名称，例如 `skills-creator`，按 `forge/`、`.claude/skills/`、`.agents/skills/`、`.codex/skills/` 的实际存在目录搜索。
- "所有 Skill"，批量扫描上述实际存在目录。

目标目录必须包含 SKILL.md。缺少 SKILL.md 时报告关键文件缺失并终止该目标。

## Read Phase（读取阶段）

对每个目标读取：
- SKILL.md，并拆分 YAML frontmatter 和正文。
- SKILL.en.md，如存在则同样拆分。
- CHANGELOG.md，如存在则提取最新版本。
- references/、scripts/、assets/ 的文件树。
- SKILL.md 与 SKILL.en.md 中引用的相对路径。

然后运行：

```bash
python3 scripts/check_skill_density.py <skill-dir>
```

脚本输出 JSON 字段用于 BODY-07 与 BODY-08，不允许用 LLM 估算替代脚本结果。

## Rule Groups（规则分组）

1. YAML Frontmatter（YML-01 ~ YML-05）
   - 验证 name、description、顶级属性白名单、metadata 字段契约和 YAML 安全边界。

2. Description Quality（DESC-01 ~ DESC-03）
   - 验证三段式结构、中英文触发词覆盖、触发词具体性和尖括号安全。

3. File Structure（FILE-01 ~ FILE-06）
   - 验证 SKILL.md、SKILL.en.md、CHANGELOG.md、目录名、README.md 禁止项和保留前缀。

4. Version Consistency（VER-01 ~ VER-05）
   - 验证 metadata.version、CHANGELOG 最新版本、日期格式、metadata.author、metadata.catalog 字段契约和 SKILL.en.md 版本一致性。

5. Body Quality（BODY-01 ~ BODY-08）
   - 验证正文长度、必需章节、引用路径、模糊表述、核心能力条数、中文 canonical 语言规则、Workflow density 和 Workflow extraction。

6. Naming（NAME-01 ~ NAME-03）
   - 验证 references/、scripts/、assets/ 文件命名。

7. Mirror（MIRROR-01 ~ MIRROR-03）
   - 验证 SKILL.en.md YAML 对齐、英文章节齐备和引用路径同步。

8. Classification（CLASS-01 ~ CLASS-03）
   - 验证模板、脚本和知识文档是否放在正确目录。

## Metadata Contract（metadata 字段契约）

检查 YAML frontmatter 时只认可以下 `metadata` 子字段：
- `metadata.version`：必填，SemVer 格式，并与 CHANGELOG.md 最新版本和 SKILL.en.md 一致。
- `metadata.author`：必填，非空，记录原始作者。
- `metadata.catalog`：可选；存在时必须非空、kebab-case，并与源码 catalog 归属及 SKILL.en.md mirror 一致。

发现未登记的 `metadata.*` 字段时，在 YML-04 中报告非法字段；不要把未知字段解释为开放扩展。

## Workflow Density（Workflow 密度）

BODY-07 与 BODY-08 必须使用 `scripts/check_skill_density.py` 的输出：
- `body_chars`：入口正文字符数。
- `workflow_chars`：Workflow 章节字符数。
- `workflow_ratio`：Workflow 占正文比例。
- `near_body_limit`：`body_chars >= 4500`。
- `has_workflow_reference`：入口是否引用 workflow reference。
- `triggered_density_warning`：`workflow_chars > 1500` 且 `workflow_ratio > 0.5`。

报告建议：
- BODY-07：当 `triggered_density_warning` 为 true 时，提示 Workflow 过重。
- BODY-08：当 BODY-07 命中且 `has_workflow_reference` 为 false 时，建议抽取 `references/<skill-name>-workflow.md` 或等价 workflow reference。
- 如果 `near_body_limit` 为 true，在 BODY-07 详情中提示正文接近 5000 字上限。

## Report Phase（报告阶段）

输出标准表格：
- `#`
- `规则 ID`
- `检查项`
- `状态`
- `详情`

总结行使用 `X/34 项通过，Y 项警告，Z 项错误`。错误和警告必须附带具体修复建议。

## Rescan Phase（复查阶段）

用户说"重新检查"、"re-lint"或"再查一次"时，重新执行读取、脚本统计和 34 条规则扫描。报告中标注已修复项和新增项。
