# CR TODO Backlog — 输出格式模板

本文档定义了 `cr-todo-backlog.md` 的文件结构和条目格式。首次创建文件或添加新条目时，严格按照此模板生成，无需检索已有文件。

---

## 文件初始化模板

首次创建 `cr-todo-backlog.md` 时使用以下骨架：

```markdown
# CR TODO Backlog — 跨 Story 延迟事项追踪

> 本文档由 `bmad-enhance-05-cr-todo-tracker` 技能维护。
> 记录 Code Review 中发现的非阻塞改进项，跨 Story 追踪直到解决。

## 统计摘要

| 状态 | 数量 |
|------|------|
| 🔴 open | 0 |
| 🟡 in-progress | 0 |
| ✅ resolved | 0 |

---

## Open Items

<!-- 按优先级排序：P1 > P2 > P3 -->

---

<!-- 已解决事项归档于此，保留用于回顾 -->

---

## 条目模板（不要删除）

<!--
### TODO-{NNN}: {简短标题}

- **来源**: {story-id} CR round {N} ({YYYY-MM-DD})
- **优先级**: P1 / P2 / P3
- **类别**: refactor / duplication / tech-debt / naming / test-gap / other
- **描述**: {具体问题描述}
- **涉及文件**: `{file-path}` (可多个)
- **建议时机**: {例如 "下次触及 init.ts 时" / "epic-3 开始前" / "专项重构"}
- **状态**: open / in-progress / resolved
- **解决记录**: {解决时填写：在哪个 story 中解决，PR/commit 引用}
-->
```

---

## 单个条目格式

每个 TODO 条目必须包含以下所有字段：

```markdown
### TODO-{NNN}: {简短标题}

- **来源**: {story-id} CR round {N} ({YYYY-MM-DD})
- **优先级**: P1 / P2 / P3
- **类别**: refactor / duplication / tech-debt / naming / test-gap / other
- **描述**: {具体问题描述，包含代码位置引用和影响说明}
- **涉及文件**: `{file-path}`{, `{file-path-2}`}
- **建议时机**: {具体建议，如 "下次触及 init.ts 时" / "Epic 3 中实现前序阶段的 Story" / "安全策略专项优化时"}
- **状态**: open
- **解决记录**:
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| 编号 | ✅ | `TODO-{NNN}`，三位数字零填充，递增不复用 |
| 标题 | ✅ | 简短描述问题本质，不超过 50 字 |
| 来源 | ✅ | story-id + CR round + 日期，从 CR 文件头部元信息提取 |
| 优先级 | ✅ | P1（下次触及必处理）/ P2（Epic 内处理）/ P3（择机处理） |
| 类别 | ✅ | 枚举值：refactor / duplication / tech-debt / naming / test-gap / other |
| 描述 | ✅ | 包含具体代码位置（文件:行号）、问题行为、改进方案 |
| 涉及文件 | ✅ | 项目相对路径，反引号包裹，多个文件逗号分隔 |
| 建议时机 | ✅ | 具体可操作的触发条件，避免模糊的"后续处理" |
| 状态 | ✅ | open / in-progress / resolved |
| 解决记录 | ✅ | 初始留空；resolved 时填写解决的 story、方式、引用 |

---

## 文档操作规范

### 添加条目
- 新条目插入 `## Open Items` 区域内，按优先级排序（P1 在前，P3 在后）
- 同优先级内按编号升序排列
- 插入后更新顶部统计摘要表中 `🔴 open` 的数量

### 标记解决
- 将条目状态从 `open` / `in-progress` 改为 `resolved`
- 填写 `解决记录` 字段
- 将整个条目从 `## Open Items` 移至 `<!-- 已解决事项归档于此 -->` 注释下方
- 更新顶部统计摘要表（减少 open/in-progress，增加 resolved）

### 来源信息提取规则
从 CR 文件头部 YAML 元信息中提取：
- `Story` 字段 → story-id
- `Round` 字段 → round 编号
- `Date` 字段 → 日期
- 组合为：`{story-id} CR round {round} ({date})`
- 如果条目跨越多轮 CR，记录所有轮次范围：`{story-id} CR round {N1}-{N2} ({date1} ~ {date2})`
