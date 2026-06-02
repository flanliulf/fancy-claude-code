# SR 三层并行审查引擎

本文件定义 SR-01 的三层并行审查引擎执行逻辑。由 SKILL.md Step 4 调用。

对标 CR-01 的 `review-engine.md`，审查对象从代码 diff 改为 Story 设计文档。

---

## 输入变量

由 SKILL.md 传入：

| 变量 | 说明 |
|------|------|
| `$review_scope` | 审查粒度：`"epic"` 或 `"story"` |
| `$epic_id` | Epic 编号 |
| `$story_id` | Story ID（仅 Story 模式） |
| `$sr_dir` | Story 审查目录路径 |
| `$round_number` | 当前审查轮次 |
| `$review_type` | `"first"` 或 `"followup"` |
| `$story_files` | 待审查的 Story 文件路径列表 |
| `$epic_file` | Epic 定义文件路径 |
| `$baseline_files` | 对照基准文件路径列表（project-context.md、架构文档等） |

复审时额外传入：
| 变量 | 说明 |
|------|------|
| `$sr_dir/.tmp/review-context.md` | 已修复问题清单（由 SKILL.md Step 3 写入） |

---

## Phase A：构建审查输入

### A1：组织待审查内容

- 读取 `$epic_file` 获取 Epic 定义（目标、范围、FR/NFR）
- 读取 `$story_files` 中每个 Story 文件的完整内容
- 记录每个 Story 的文件名和标题

### A2：收集对照基准

- 读取 `$baseline_files` 中的所有基准文件
- 提取关键信息摘要（避免全文传入子代理导致上下文溢出）：
  - `project-context.md`：全局规则、技术约束、非功能性要求
  - 架构文档（如 `03-core-decisions.md`、`04-implementation-patterns.md`）：接口签名、模块边界、类型定义
  - 前序 Epic Story（如有引用）：共享契约定义（公共接口、类型、错误处理约定）

### A3：写入审查输入文件

将组织后的内容写入 `$sr_dir/.tmp/review-input.md`，结构如下：

```markdown
# 审查输入

## 审查粒度
{$review_scope}

## Epic 定义
{Epic 文件内容摘要}

## 待审查 Story
### Story {story-id-1}: {title}
{完整内容}

### Story {story-id-2}: {title}
{完整内容}
...

## 对照基准摘要
### project-context.md
{关键规则摘要}

### 架构文档
{接口/类型/模块边界摘要}

### 前序 Epic 共享契约
{公共接口定义摘要，如有}
```

### A4：分批判断

- **Epic 模式**：若 Story 数量 > 5，按编号顺序分批，每批 ≤ 5 个
  - 每批独立执行 Phase B ~ Phase E
  - 第一批完成后写入审查总结文件
  - 后续批次开始前回顾前批意见确保口径一致，结果追加写入同一份文件
- **Story 模式**：不分批，直接进入 Phase B

---

## Phase B：并行三层审查

### B0：执行模式选择

优先尝试并行模式（同一消息中发起全部三个 Agent 调用）。

降级策略：
1. **并行模式**（首选）：同时启动 B1 + B2 + B3
2. **串行模式**（Agent 并行不可用时）：按 B1 → B2 → B3 顺序执行
3. **单一 LLM 回退**（全部子代理失败时）：
   - Epic 模式：按八大维度自行审查（结构完整性、AC 可测性、Epic 一致性、架构一致性、Story 间冲突、任务拆分、交互/安全/性能、共享契约）
   - Story 模式：按六大维度自行审查（跳过 Story 间冲突与依赖、跳过跨 Story 共享契约中的 Story 间部分）
   - 向用户明确告知降级

### B1：Structure & Completeness Hunter

通过 Agent 工具启动 `review-adversarial-general` 子代理。

**Prompt 构造**：
```
你是一个 Story 设计文档的结构和完整性审查专家。

审查目标：对以下 Story 设计文档进行对抗式审查，专注于三个维度：
1. **结构完整性**：Story 是否包含所有必要章节（Story 描述、AC、Tasks、Dev Notes、References）。章节不能只有标题，必须有实质内容。
2. **AC 可测性**：逐条检查每个 Acceptance Criteria 是否清晰、可测试、只有一种解释。识别模糊词汇如"妥善处理"、"适当验证"、"合理配置"。
3. **任务拆分合理性**：Tasks 是否足够支撑 AC 的全部交付。是否有遗漏的实现步骤。粒度是否合适。检查"AC 范围超出 Story 自身边界"的问题。

找出至少 10 个问题。每个问题必须包含：具体的文件名、章节名、问题内容和改进建议。

{review-input.md 的内容}
```

输出文件：`$sr_dir/.tmp/b1-structure-hunter.md`（Markdown 列表格式）

### B2：Consistency Checker

通过 Agent 工具启动 `review-edge-case-hunter` 子代理。

**Prompt 构造（Epic 模式）**：
```
你是一个 Story 设计文档的跨文档一致性审查专家。

审查目标：对以下 Story 设计文档进行一致性穷举审查，专注于三个维度：
1. **与 Epic 一致性**：Story 的交付内容是否与 Epic 目标对应。FR/NFR 引用是否匹配。是否有范围超出。
2. **与架构文档一致性**：Story 中的接口签名、类型定义、模块边界是否与架构文档一致。使用具体的接口名和类型名进行交叉核对。
3. **Story 间冲突与依赖**：同一 Epic 内 Story 之间的依赖顺序是否合理。是否有职责重叠或矛盾定义。是否存在前向依赖（当前 Story 依赖尚未定义的能力）。

输出 JSON 数组格式，每个条目包含：title、detail、location（文件名:章节）、story_id。

{review-input.md 的内容}
```

**Prompt 构造（Story 模式）**：
```
你是一个 Story 设计文档的跨文档一致性审查专家。

审查目标：对以下单个 Story 设计文档进行一致性穷举审查，专注于两个维度：
1. **与 Epic 一致性**：Story 的交付内容是否与 Epic 目标对应。FR/NFR 引用是否匹配。是否有范围超出。
2. **与架构文档一致性**：Story 中的接口签名、类型定义、模块边界是否与架构文档一致。使用具体的接口名和类型名进行交叉核对。

注意：本次为单 Story 审查模式，不检查 Story 间冲突与依赖。

输出 JSON 数组格式，每个条目包含：title、detail、location（文件名:章节）、story_id。

{review-input.md 的内容}
```

输出文件：`$sr_dir/.tmp/b2-consistency-checker.json`（JSON 数组格式）

### B3：Contract & Boundary Auditor

通过 Agent 工具启动 `review-acceptance-auditor` 子代理。

**Prompt 构造**：
```
你是一个 Story 设计文档的契约和边界审查专家。

审查目标：对以下 Story 设计文档进行契约和边界审查，专注于两个维度：
1. **跨 Epic 共享契约**：当 Story 引用前序 Epic 定义的公共接口（如 Reporter、PathResolver、GlobalError、类型定义等）时，核对契约是否一致。识别"Story 隐式改写公共契约"和"文档内部可读但跨文档冲突"的隐蔽模式。
2. **交互/认证/安全/性能口径**：涉及用户交互（TTY/非 TTY 行为）、认证、安全处理规则、性能可衡量标准的 Story 是否定义了清晰规则。是否与 project-context.md 的全局规则一致。

每个问题必须包含：具体的文件名、章节名、与哪个基准文档存在什么样的不一致。

{review-input.md 的内容}
```

输出文件：`$sr_dir/.tmp/b3-contract-auditor.md`（Markdown 列表格式）

### B4：收集结果与失败处理

- 收集三层输出文件
- 若某层子代理失败（文件为空或不存在）：
  - 记录失败层名称到 `$failed_layers`（如 `["consistency"]`）
  - 使用剩余层继续
- 若全部失败：执行 B0 中的单一 LLM 回退策略

---

## Phase C：规范化与去重

### C1：格式规范化

将三层的不同输出格式统一转换为中间格式：

```json
{
  "id": 1,
  "source": "structure",
  "title": "一行摘要",
  "detail": "完整描述",
  "location": "2-1-user-auth.md:Acceptance Criteria",
  "story_id": "2-1"
}
```

**转换规则**：

| 层 | 输入格式 | source 值 | 转换要点 |
|----|---------|----------|---------|
| B1 | Markdown 列表 | `structure` | 从列表项提取 title（首句）和 detail（剩余）；从引用的文件名提取 location 和 story_id |
| B2 | JSON 数组 | `consistency` | 直接映射字段；已包含 location 和 story_id |
| B3 | Markdown 列表 | `contract` | 从列表项提取 title 和 detail；从引用的文件名提取 location 和 story_id |

### C2：语义去重

- 按 title + location 进行相似度匹配
- 同一问题被多层发现时合并为一条，`source` 变为组合值（如 `structure+consistency`）
- 合并规则：
  - 优先保留 B2（JSON 格式）的 detail 和 location（更结构化）
  - 将其他层的补充细节追加到 detail
  - story_id 取一致的值；不一致时列出所有涉及的 story_id

写入 `$sr_dir/.tmp/normalized-findings.json`

---

## Phase D：四桶分类 + 严重性标签映射

### D1：四桶分类

对每条 normalized finding 分入恰好一个桶：

| 桶 | 条件 | SR 场景典型示例 |
|----|------|---------------|
| `decision_needed` | 需人工裁决的模糊设计选择 | 架构方案二选一、AC 的多种合理解读 |
| `patch` | 修复方案明确的文档问题 | AC 措辞模糊、缺失章节、接口签名不一致 |
| `defer` | 既有问题，非本次 Story 引入 | 前序 Epic 遗留的契约不一致 |
| `dismiss` | 噪音、误报或已处理 | 审查理解偏差、已在其他章节覆盖 |

### D2：严重性标签映射

四桶分类与严重性标签并存：

| 四桶分类 | 严重性标签 | 映射条件 |
|---------|----------|---------|
| `decision_needed` | `[高]` | 始终 |
| `patch` | `[高]` | 多来源命中 + 涉及安全/数据/核心接口 |
| `patch` | `[中]` | 多来源非安全 OR 单来源 + 安全/数据 |
| `patch` | `[低]` | 单来源，非安全 |
| `defer` | — | 不标严重性，记入通过项 |
| `dismiss` | — | 丢弃，不出现在最终输出 |

### D3：复审场景补充

IF `$round_number` > 1：
- 读取 `$sr_dir/.tmp/review-context.md` 获取已修复问题清单
- 将当前 findings 与已修复清单交叉比对：
  - 已修复的问题从 findings 中移除，标注为"上轮问题回顾 → 已修复"
  - 未修复的问题保留，额外标注"上轮遗留"
  - 新发现的问题标注 `[新]`

### D4：写入分类结果

将分类后的 findings 写入 `$sr_dir/.tmp/classified-findings.json`：

```json
{
  "id": 1,
  "source": "structure+consistency",
  "title": "一行摘要",
  "detail": "完整描述",
  "location": "2-1-user-auth.md:Acceptance Criteria",
  "story_id": "2-1",
  "bucket": "patch",
  "severity": "[中]"
}
```

---

## Phase E：构建输出数据

### E1：新发现区域

按序号、严重性、标题组织（`dismiss` 桶的发现不输出）：

```markdown
### <序号>. [<严重性>] <问题标题>
- **来源**：<structure / consistency / contract / 组合>
- **分类**：<decision_needed / patch>
- **涉及 Story**：<story-id>
- **证据** - <文件名、章节、具体内容>
- **影响** - <对设计完整性/一致性/可开发性的影响>
- **建议** - <具体修改建议，指明修改哪个文件的哪个部分>
```

### E2：通过项区域

- `defer` 桶的发现列入通过项（标注为"已知既有问题"）
- 未发现问题的审查维度列入通过项

### E3：审查层状态标注

若 `$failed_layers` 非空，在审查结论中标注：

```
审查层状态：{可用层数}/3 层完成（{失败层名称} 层执行失败，已使用剩余层完成审查）
```

### E4：输出交接

- `classified-findings.json` 已在 Phase D 写入 `$sr_dir/.tmp/`
- `$failed_layers` 在上下文中传回 SKILL.md Step 5
- Phase E 的格式化输出供 SKILL.md Step 5 组装最终审查总结时参考
