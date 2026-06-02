# SR 工作流配置

本文件定义 bmenhance SR 系列 Skill（01-03）共用的路径约定、文件名格式和通用规则。所有 SR Skill 应以本文件为准，避免硬编码。

---

## 双粒度审查模式

SR 系列支持两种审查粒度，根据用户输入自动判定：

| 模式 | 触发条件 | 审查范围 | 跨 Story 维度 |
|------|---------|---------|-------------|
| **Epic 模式** | 输入匹配 `epic {N}` / `epic-{N}` | 该 Epic 下全部 Story | 完整启用 |
| **Story 模式** | 输入匹配 `story {N-M}` / `{N-M}` / Story 文件路径 | 仅指定 Story | 部分启用（跳过 Story 间冲突与依赖） |

判定规则：
- `$review_scope = "epic"` 时：`$epic_id` 从输入提取，`$story_id` 为空
- `$review_scope = "story"` 时：`$story_id` 从输入提取，`$epic_id` 从 story-id 前缀提取

---

## 目录与路径

| 配置项 | 路径格式 | 说明 |
|--------|---------|------|
| 实现产物目录 | `_bmad-output/implementation-artifacts/` | 项目级实现产物根目录 |
| Story 文件目录 | `{impl-artifacts}/stories/` | Story spec 文件所在目录 |
| Epic 文件目录 | `_bmad-output/planning-artifacts/epics/` | Epic 定义文件所在目录 |
| Story 审查父目录 | `{impl-artifacts}/story-reviews/` | 所有 SR 目录的父目录 |
| Story 审查目录（Epic 模式） | `{impl-artifacts}/story-reviews/epic-{epic-id}-story-review/` | Epic 粒度的 SR 产物存放目录 |
| Story 审查目录（Story 模式） | `{impl-artifacts}/story-reviews/{story-id}-story-review/` | Story 粒度的 SR 产物存放目录 |
| 临时文件目录 | `$sr_dir/.tmp/` | 审查过程中的中间数据，完成时自动清理 |
| 规划产物目录 | `_bmad-output/planning-artifacts/` | 项目级规划产物 |

说明：
- `{impl-artifacts}`：实现产物目录的简写，即 `_bmad-output/implementation-artifacts/`
- `{epic-id}`：Epic 编号（如 `2`）
- `{story-id}`：Story ID，仅包含序号（如 `2-3`）
- `$sr_dir`：Story 审查目录的运行时路径，根据 `$review_scope` 解析为 Epic 模式目录或 Story 模式目录
- 两种粒度的产物存放在不同目录中，互不干扰
- Story 审查目录如不存在，在首次写入时自动创建
- 临时文件目录 `.tmp/` 的内容在审查完成后自动删除，不纳入版本管理

---

## 文件名格式

| 文件类型 | Epic 模式 | Story 模式 | 使用者 |
|---------|-----------|-----------|--------|
| 审查总结 | `epic-{epic-id}-story-review-summary-{YYYYMMDD}-round-{n}.md` | `{story-id}-story-review-summary-{YYYYMMDD}-round-{n}.md` | 01-reviewer 生成，02-evaluator 消费 |
| 审查评估 | `epic-{epic-id}-story-review-evaluation-{YYYYMMDD}-round-{m}.md` | `{story-id}-story-review-evaluation-{YYYYMMDD}-round-{m}.md` | 02-evaluator 生成，03-fixer 消费 |

说明：
- `{YYYYMMDD}`：当前日期，如 20260413
- `{n}` / `{m}`：轮次编号，从 1 开始递增
- 审查和评估的轮次编号独立计数

---

## Story ID 规则

- **定义**：story-id 只包含 epic 和 story 的序号，不包括 story name
- **合法格式**：`1-1`、`1.1`、`1·1`、`2-3`
- **非法格式**：`1-1-user-auth`（包含了 story name）
- **提取方法**：从 Story 文件路径或用户输入中提取前缀序号部分
- **Epic ID 提取**：从 story-id 的第一段提取（如 `2-3` → epic-id = `2`）

---

## Story 匹配规则

- **Epic 模式**：在 Story 文件目录中匹配以 `{epic-id}-` 开头的所有文件（如 epic-2 → `2-1-*.md`、`2-2-*.md`）
- **Story 模式**：在 Story 文件目录中匹配以 `{story-id}-` 开头的文件（如 story 2-3 → `2-3-*.md`）

---

## 轮次检测规则

- **审查轮次**：扫描 `$sr_dir` 下匹配 `*-story-review-summary-*-round-*.md` 的文件，统计已有轮次数量，本轮 = 已有轮次 + 1
- **评估轮次**：扫描 `$sr_dir` 下匹配 `*-story-review-evaluation-*-round-*.md` 的文件，统计已有轮次数量，本轮 = 已有轮次 + 1
- **首轮 vs 复审**：轮次 == 1 为首轮审查，轮次 > 1 为复审

---

## 输出语言

- 始终使用中文输出审查结果、评估结果和修订记录
- 代码注释和技术术语保持原文（英文）

---

## 元信息字段

所有 SR 产物文件的 YAML 头部必须包含以下字段：
- `Scope`：审查粒度，值为 `epic` 或 `story`
- `Model Used`：如实填写当前执行该操作的模型名称，格式为 `<模型全名> (<模型标识符>)`，便于跨 LLM 追溯和质量归因
- Epic 模式额外字段：`Epic`（epic-id）、`Stories Reviewed`（审查的 Story 数量，仅审查总结）
- Story 模式额外字段：`Story`（story-id）、`Epic`（所属 epic-id）

---

## 变量标识约定

SR Skill 文档中使用两种占位符格式，含义不同：

| 格式 | 含义 | 示例 |
|------|------|------|
| `{花括号}` | 文件名模板占位符，定义命名规则 | `epic-{epic-id}-story-review-summary-{YYYYMMDD}-round-{n}.md` |
| `$snake_case` | 运行时变量，执行过程中动态产生和消费 | `$epic_id`、`$review_scope`、`$failed_layers` |

SKILL.md 和 review-engine.md 中的运行时变量统一使用 `$snake_case` 格式。从 sr-config.md 读取文件名模板后，将模板中的 `{epic-id}` 等占位符替换为对应运行时变量的实际值。

SR 专用变量：
- `$review_scope`：审查粒度，值为 `"epic"` 或 `"story"`
- `$epic_id`：Epic 编号（两种模式下都有值）
- `$story_id`：Story ID（仅 Story 模式下有值，Epic 模式为空）
- `$sr_dir`：Story 审查目录的运行时路径
