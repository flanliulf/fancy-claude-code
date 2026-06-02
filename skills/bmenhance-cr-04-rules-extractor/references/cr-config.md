# CR 工作流配置

本文件定义 bmenhance CR 系列 Skill（01-06）共用的路径约定、文件名格式和通用规则。所有 CR Skill 应以本文件为准，避免硬编码。

---

## 目录与路径

| 配置项 | 路径格式 | 说明 |
|--------|---------|------|
| 实现产物目录 | `_bmad-output/implementation-artifacts/` | 项目级实现产物根目录 |
| Story 文件目录 | `{impl-artifacts}/stories/` | Story spec 文件所在目录 |
| 代码审查父目录 | `{impl-artifacts}/code-reviews/` | 所有 Story 的 CR 目录的父目录 |
| 代码审查目录 | `{impl-artifacts}/code-reviews/{story-id}-code-review/` | 每个 Story 的 CR 产物存放目录 |
| 临时文件目录 | `$cr_dir/.tmp/` | 审查过程中的中间数据（diff、子审查输出、分类结果），Step 5 结束时自动清理 |
| CR 规则目录 | `{impl-artifacts}/cr-rules/` | CR 规则文件（todo-backlog、规则文档等） |
| 回顾总结目录 | `{impl-artifacts}/retrospectives/` | Epic/Sprint 回顾总结文件 |
| 规划产物目录 | `_bmad-output/planning-artifacts/` | 项目级规划产物（bmm-workflow-status.yaml 等） |

说明：
- `{impl-artifacts}`：实现产物目录的简写，即 `_bmad-output/implementation-artifacts/`
- `{story-id}`：从 Story 标识中提取的序号（见下方 Story ID 规则）
- `$cr_dir`：代码审查目录的运行时路径（= `{impl-artifacts}/code-reviews/{story-id}-code-review/`）
- Story 文件和 CR 目录分别位于 `stories/` 和 `code-reviews/` 子目录中，不在同一层级
- 代码审查目录如不存在，在首次写入时自动创建
- 临时文件目录 `.tmp/` 的内容在审查完成后自动删除，不纳入版本管理

---

## 文件名格式

| 文件类型 | 文件名格式 | 使用者 |
|---------|-----------|--------|
| 审查总结 | `{story-id}-code-review-summary-{YYYYMMDD}-round-{n}.md` | 01-reviewer 生成，02-evaluator / 04-rules-extractor 消费 |
| 审查评估 | `{story-id}-code-review-evaluation-{YYYYMMDD}-round-{m}.md` | 02-evaluator 生成，03-fixer / 05-todo-tracker / 06-finalizer 消费 |
| CR 规则总结 | `cr-rules-summary.md` | 04-rules-extractor 管理，位于 CR 规则目录（`{impl-artifacts}/cr-rules/`） |
| TODO Backlog | `cr-todo-backlog.md` | 05-todo-tracker 管理，位于 CR 规则目录（`{impl-artifacts}/cr-rules/`） |
| Sprint 状态 | `sprint-status.yaml` | 06-finalizer 更新，位于实现产物目录根 |
| 工作流状态 | `bmm-workflow-status.yaml` | 06-finalizer 更新，位于规划产物目录 |

说明：
- `{YYYYMMDD}`：当前日期，如 20260403
- `{n}` / `{m}`：轮次编号，从 1 开始递增
- 审查和评估的轮次编号独立计数
- `cr-rules-summary.md` 用于沉淀已验证、已解决或已确认可复用的 CR 规则；未解决的非阻塞改进项应进入 `cr-todo-backlog.md`

---

## Story ID 规则

- **定义**：story-id 只包含 epic 和 story 的序号，不包括 story name
- **合法格式**：`1-1`、`1.1`、`1·1`、`2-3`
- **非法格式**：`1-1-user-auth`（包含了 story name）
- **提取方法**：从 Story 文件路径或用户输入中提取前缀序号部分

---

## 轮次检测规则

- **审查轮次**：扫描代码审查目录下匹配 `*-code-review-summary-*-round-*.md` 的文件，统计已有轮次数量，本轮 = 已有轮次 + 1
- **评估轮次**：扫描代码审查目录下匹配 `*-code-review-evaluation-*-round-*.md` 的文件，统计已有轮次数量，本轮 = 已有轮次 + 1
- **首轮 vs 复审**：轮次 == 1 为首轮审查，轮次 > 1 为复审

---

## 输出语言

- 始终使用中文输出审查结果、评估结果和修复记录
- 代码注释和技术术语保持原文（英文）

---

## 元信息字段

所有 CR 产物文件的 YAML 头部必须包含 `Model Used` 字段，如实填写当前执行该操作的模型名称，格式为 `<模型全名> (<模型标识符>)`，便于跨 LLM 追溯和质量归因。

---

## 变量标识约定

CR Skill 文档中使用两种占位符格式，含义不同：

| 格式 | 含义 | 示例 |
|------|------|------|
| `{花括号}` | 文件名模板占位符，定义命名规则 | `{story-id}-code-review-summary-{YYYYMMDD}-round-{n}.md` |
| `$snake_case` | 运行时变量，执行过程中动态产生和消费 | `$story_id`、`$review_input`、`$failed_layers` |

SKILL.md 和 review-engine.md 中的运行时变量统一使用 `$snake_case` 格式。从 cr-config.md 读取文件名模板后，将模板中的 `{story-id}` 等占位符替换为对应运行时变量 `$story_id` 的实际值。
