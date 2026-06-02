# SR 审查总结 — 输出格式模板

本文档定义 SR-01 审查总结的输出格式。根据 `$review_scope`（epic/story）和 `$round_number`（首轮/复审）选择对应模板变体。

---

## Epic 模式 — 首轮审查（Round 1）

文件命名：`epic-{epic-id}-story-review-summary-{YYYYMMDD}-round-{n}.md`

```markdown
---
Epic: {epic-id}
Scope: epic
Round: 1
Date: {YYYY-MM-DD}
Model Used: {模型全名} ({模型标识符})
Type: Story Review Summary
Stories Reviewed: {story-count}
---

## 审查结论

首轮审查。共审查 Epic {epic-id} 下 {story-count} 个 Story。{审查层状态标注，如有失败层}

- 通过：{n} 个
- 有条件通过：{n} 个
- 硬阻塞：{n} 个

总体判断：{方向评估 + 建议}

## 审查范围

- Story 文件：
  - `{story-file-1}.md`
  - `{story-file-2}.md`
  {按实际数量列出}
- 对照基准：
  - `project-context.md`
  - `planning-artifacts/epics/epic-{epic-id}.md`
  {按实际需要列出架构文档、前序 Story 等}
- 审查维度：
  - 结构完整性
  - AC 可测性
  - 与 Epic 一致性
  - 与架构文档一致性
  - Story 间冲突与依赖
  - 任务拆分合理性
  - 交互/认证/安全/性能口径
  - 跨 Epic 共享契约
  {根据 Epic 特性补充特定维度}

## 新发现

### 1. [{严重性}] {问题标题}
- **来源**：{structure / consistency / contract / 组合}
- **分类**：{decision_needed / patch}
- **涉及 Story**：{story-id}
- **证据** - {文件名、章节、具体内容}
- **影响** - {对设计完整性/一致性/可开发性的影响}
- **建议** - {具体修改建议，指明修改哪个文件的哪个部分}

{按严重性降序排列所有 decision_needed 和 patch 桶的发现}

## 逐篇审查结论

### Story {epic-id}.{x}: {story_title}

**结论：{通过 / 有条件通过 / 硬阻塞}**

**优点**
- {优点 1}
- {优点 2}

**关键问题**
1. **{问题标题}** — {描述，引用具体文件、章节、内容作为证据}

**建议动作**
- {具体建议，指明修改哪个文件的哪个部分}

{如果结论是"通过"，可省略"关键问题"和"建议动作"，改为"关注点"列出非阻塞的观察}
{按 Story 编号顺序逐篇列出}

## 通过项
- {已通过检查的维度/模块概述}
- {defer 桶的已知既有问题，标注为"已知既有问题，非本次引入"}
```

---

## Epic 模式 — 复审（Round N > 1）

在首轮模板基础上，在"审查范围"之后、"新发现"之前增加以下章节：

```markdown
## 上轮问题回顾

### 已修复
1. Round {x} / Finding #{y} — {问题标题}
   - {修复位置和方式简述}
   - {验证结果}

### 仍为非阻塞待办
1. Round {x} / Finding #{y} — {问题标题}
   - 维持既有评估结论。

## 新发现

{如果无新发现}：本轮未发现新的阻塞项或中高优先级问题。

{如果有新发现}：复审中新发现的问题需加 `[新]` 标记（如 `[中][新]`）。
```

并在末尾增加结论章节：

```markdown
## 结论
- **结论**：{通过 / 不通过}
- **阻塞项**：{无 / 列出}
- **建议**：{后续行动建议}
```

---

## Story 模式 — 首轮审查（Round 1）

文件命名：`{story-id}-story-review-summary-{YYYYMMDD}-round-{n}.md`

```markdown
---
Story: {story-id}
Epic: {epic-id}
Scope: story
Round: 1
Date: {YYYY-MM-DD}
Model Used: {模型全名} ({模型标识符})
Type: Story Review Summary
---

## 审查结论

首轮审查。审查 Story {story-id}。{审查层状态标注，如有失败层}

结论：{通过 / 有条件通过 / 硬阻塞}

{总体判断文字}

## 审查范围

- Story 文件：`{story-file-path}`
- 对照基准：
  - `project-context.md`
  - `planning-artifacts/epics/epic-{epic-id}.md`
  {按实际需要列出}
- 审查维度：
  - 结构完整性
  - AC 可测性
  - 与 Epic 一致性
  - 与架构文档一致性
  - 任务拆分合理性
  - 交互/认证/安全/性能口径
  - 跨 Epic 共享契约
  - ~~Story 间冲突与依赖~~（单 Story 模式未启用）

## 新发现

### 1. [{严重性}] {问题标题}
- **来源**：{structure / consistency / contract / 组合}
- **分类**：{decision_needed / patch}
- **证据** - {文件名、章节、具体内容}
- **影响** - {对设计完整性/一致性/可开发性的影响}
- **建议** - {具体修改建议，指明修改哪个文件的哪个部分}

{按严重性降序排列}

## 优点
- {优点 1}
- {优点 2}

## 通过项
- {已通过检查的维度概述}
- {defer 桶的已知既有问题}
```

---

## Story 模式 — 复审（Round N > 1）

在首轮模板基础上，在"审查范围"之后、"新发现"之前增加"上轮问题回顾"章节（结构与 Epic 模式复审相同），并在末尾增加"结论"章节。

---

## 格式规范

- **严重性标签**：`[高]` / `[中]` / `[低]`
- **新发现标注**：复审中的新发现需加 `[新]` 标记（如 `[中][新]`）
- **来源字段**：`structure` / `consistency` / `contract` / 组合值（如 `structure+consistency`）
- **分类字段**：`decision_needed` / `patch`（`defer` 和 `dismiss` 不出现在新发现中）
- **逐篇结论三级判定**：
  - **通过**：结构完整、AC 可测、与 Epic/架构一致、无明显冲突
  - **有条件通过**：整体可用但存在需修正的问题，不影响核心架构
  - **硬阻塞**：存在必须先解决才能进入开发的关键问题
