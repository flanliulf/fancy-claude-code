# 三层并行审查引擎

本文件定义 bmenhance-cr-01-reviewer Step 4 的审查执行逻辑。通过并行启动三个独立审查层（Blind Hunter、Edge Case Hunter、Acceptance Auditor），对代码变更进行多维度对抗式审查，然后将发现规范化、去重、分类，最终输出符合 `assets/output-format.md` 模板的结构化数据。

**运行时变量约定**：使用 `$snake_case` 格式标识运行时变量，与 cr-config.md 中的文件名模板占位符 `{花括号}` 区分。

**临时文件目录**：`$cr_dir/.tmp/`（由 SKILL.md Step 1 创建）。大体积中间数据写入临时文件，后续步骤通过 Read 工具读取，避免上下文窗口溢出。

**隔离机制**：每个 Story 拥有独立的 `$cr_dir`（如 `code-reviews/1-1-code-review/`、`code-reviews/2-3-code-review/`），因此不同 Story 的临时文件天然隔离、互不干扰。但同一 Story 不得同时发起多次审查，否则共享同一 `.tmp/` 目录会导致临时文件互相覆盖。

---

## Phase A：构建审查输入

### A1. 提取关联代码文件列表

从 Story 文档中提取本次审查涉及的代码文件路径。查找顺序：
1. Story 文件中的 `## File List` 章节（如存在）
2. Story 文件中的 `## Implementation Files` 章节（如存在）
3. Story 文件中 `## Tasks` 或 `## Subtasks` 章节中引用的文件路径

若以上均未找到，停止并询问用户提供涉及的代码文件列表。

### A2. 构建 diff → 写入 `$cr_dir/.tmp/review-input.diff`

根据当前 git 状态和用户意图，按以下优先级尝试获取 diff，将结果保存为 `$review_input`：

1. **用户提供 diff**：若用户直接粘贴了 diff 内容或指定了 diff 文件路径
   - 验证：内容非空且可解析为统一 diff 格式
   - 若不可解析，停止并要求用户提供有效 diff
2. **提交范围**：`git log --oneline <range> -- <file1> <file2> ...` 确认范围有效后，`git diff <range> -- <file1> <file2> ...`
   - 条件：用户指定了提交范围（如 `HEAD~3..HEAD`、`<sha1>..<sha2>`）
   - 验证：范围可解析且 diff 非空
3. **分支对比**（默认优先）：`git diff main...HEAD -- <file1> <file2> ...`
   - 条件：当前分支不是 main/master
   - 验证：基准分支存在且 diff 非空
4. **未提交变更**（降级）：`git diff HEAD -- <file1> <file2> ...`
   - 条件：存在暂存或未暂存的变更
   - 对于未追踪的新文件：`git diff --no-index /dev/null <file>`
5. **全文件内容**（再降级）：直接读取完整文件内容
   - 条件：以上四种 diff 均为空（代码已提交且无差异）
   - 此模式下审查范围为完整文件而非差异

选择逻辑：
- 若用户在触发审查时明确指定了 diff 来源（如"审查最近 3 次提交"、"审查这个 diff"），直接使用对应模式
- 若用户未指定，按 3→4→5 的优先级自动检测
- 无论何种来源，验证 `$review_input` 非空；若为空则停止并告知用户无内容可审查

**写入临时文件**：将 `$review_input` 写入 `$cr_dir/.tmp/review-input.diff`（全文件模式时使用 `review-input.md` 后缀），并记录输入模式（`diff` 或 `full-file`）。后续 Phase B 的子审查层通过读取此文件获取审查输入。

### A3. 确定审查模式 → 写入 `$cr_dir/.tmp/spec-content.md`

- Story 文件本身作为规格文件 → `$review_mode` = `"full"`（始终为 full，因为 CR 工作流必然有 Story 上下文）
- 提取 Story 文档中的验收标准（AC）章节内容 → `$spec_content`
- **写入临时文件**：将 `$spec_content` 写入 `$cr_dir/.tmp/spec-content.md`。后续 Phase B3 Acceptance Auditor 通过读取此文件获取验收标准。

---

## Phase B：并行三层审查

通过 Agent 工具同时启动三个独立子代理，实现真正的并行执行和上下文隔离。三个子代理各自拥有独立的上下文窗口，天然实现信息隔离——B1 无法看到 B2/B3 的输出，反之亦然。

**并发读安全**：三个子代理均以只读方式（Read 工具）读取 `$cr_dir/.tmp/review-input.diff`，文件系统层面多进程并发读同一文件不会产生冲突。该文件在 Phase A2 写入完成后才启动子代理，时序上保证先写后读。

**输出格式说明**：三个子代理的输出格式基于各自审查方法的特性选择——Blind Hunter 和 Acceptance Auditor 的发现以自然语言描述为主，使用 Markdown 格式；Edge Case Hunter 的发现具有固定 4 字段结构，使用 JSON 格式以实现零歧义的字段映射。Phase C1 会将三种格式统一规范化为中间 JSON 格式。

### B0. 执行模式选择

优先使用 Agent 工具并行启动三个子代理（**在同一条消息中发起全部三个 Agent 调用**）。

若 Agent 工具不可用或调用失败：
- 降级为串行模式：在当前上下文中依次执行 B1 → B2 → B3
- 串行模式下，每完成一层就将结果写入对应临时文件，然后继续下一层
- 向用户提示：「Agent 工具不可用，已降级为串行审查模式。」

### B1. Blind Hunter（Agent 子代理 #1）

- **调用方式**：Agent 工具，启动独立子代理
- **Agent prompt**：

> 使用 review-adversarial-general skill 对代码变更进行对抗式审查。
>
> 待审查内容位于文件：`$cr_dir/.tmp/review-input.diff`
> 请用 Read 工具读取该文件，然后按 review-adversarial-general skill 的指令执行审查。
>
> 重要约束：不要读取项目中的任何其他文件，不要寻找项目上下文、Story 文档或规格说明。仅基于上述文件的内容进行审查。
>
> 完成后将审查结果（Markdown 无序列表）写入文件：`$cr_dir/.tmp/b1-blind-hunter.md`

- **信息隔离**：prompt 中不包含任何 Story、项目上下文或其他审查层的信息，确保零上下文审查

### B2. Edge Case Hunter（Agent 子代理 #2）

- **调用方式**：Agent 工具，启动独立子代理
- **Agent prompt**：

> 使用 review-edge-case-hunter skill 对代码变更进行边界条件分析。
>
> 待审查内容位于文件：`$cr_dir/.tmp/review-input.diff`
> 请用 Read 工具读取该文件，然后按 review-edge-case-hunter skill 的指令执行审查。
>
> 你可以使用 Read、Grep、Glob 工具访问项目代码库，查看引用关系和上下文。
>
> 完成后将审查结果（JSON 数组）写入文件：`$cr_dir/.tmp/b2-edge-case-hunter.json`

### B3. Acceptance Auditor（Agent 子代理 #3）

- **调用条件**：`$review_mode` = `"full"`（CR 工作流中始终满足）
- **调用方式**：Agent 工具，启动独立子代理
- **Agent prompt**：

> 使用 review-acceptance-auditor skill 对代码变更进行验收标准审查。
>
> 待审查内容位于文件：`$cr_dir/.tmp/review-input.diff`
> 验收标准（AC）位于文件：`$cr_dir/.tmp/spec-content.md`
> 请用 Read 工具读取这两个文件，然后按 review-acceptance-auditor skill 的指令执行审查。
>
> 完成后将审查结果（Markdown 列表）写入文件：`$cr_dir/.tmp/b3-acceptance-auditor.md`

### B4. 收集结果与失败处理

三个 Agent 子代理全部返回后：

1. **收集结果**：依次用 Read 工具读取三个输出文件：
   - `$cr_dir/.tmp/b1-blind-hunter.md`
   - `$cr_dir/.tmp/b2-edge-case-hunter.json`
   - `$cr_dir/.tmp/b3-acceptance-auditor.md`

2. **失败检测**：若某个文件不存在、为空或子代理返回错误，将该层名称记录到 `$failed_layers` 列表，使用剩余层的发现继续

3. **全部失败降级**：若三个文件均不存在或为空，回退到单一 LLM 自行审查模式——按以下 6 个维度直接审查 `$cr_dir/.tmp/review-input.diff`：
  1. AC 验收标准覆盖情况
  2. 代码逻辑正确性
  3. 错误处理和边界条件
  4. 测试充分性
  5. 代码质量和可维护性
  6. 安全性和性能隐患
- 降级时向用户明确告知：「三层子审查均不可用，已降级为单一审查模式。」

---

## Phase C：规范化与去重

### C1. 格式规范化

从临时文件读取三层输出，将不同格式统一转换为中间格式。每条发现包含：

| 字段 | 说明 |
|------|------|
| `id` | 顺序整数（1, 2, 3...） |
| `source` | 来源层标识：`blind` / `edge` / `auditor`，合并后为 `blind+edge` 等 |
| `title` | 一行摘要 |
| `detail` | 完整描述（含推理和上下文） |
| `location` | 文件和行引用（如 `src/auth.ts:42-58`），若无则为空 |

转换规则：
- **Blind Hunter**（读取 `$cr_dir/.tmp/b1-blind-hunter.md`）：每条列表项的首句作为 `title`，完整内容作为 `detail`，`location` 从内容中提取（如有文件:行号引用）
- **Edge Case Hunter**（读取 `$cr_dir/.tmp/b2-edge-case-hunter.json`）：`trigger_condition` 作为 `title`，`potential_consequence` + `guard_snippet` 组合为 `detail`，`location` 直接映射
- **Acceptance Auditor**（读取 `$cr_dir/.tmp/b3-acceptance-auditor.md`）：标题作为 `title`，AC 引用 + 证据组合为 `detail`，从证据中提取 `location`

### C2. 语义去重

若两条或多条发现描述同一问题，合并为一条：
1. 以最具体的发现为基础（优先有 `location` 的 Edge Case Hunter JSON）
2. 将其他发现的唯一细节追加到 `detail` 字段
3. 将 `source` 设为合并来源（如 `blind+edge`）

判断"同一问题"的标准：
- 引用相同文件和相同/重叠行号范围
- 描述的问题本质相同（即使措辞不同）

**写入临时文件**：将规范化 + 去重后的发现列表写入 `$cr_dir/.tmp/normalized-findings.json`（JSON 数组格式）。

---

## Phase D：四桶分类 + 严重性标签映射

读取 `$cr_dir/.tmp/normalized-findings.json` 进行分类。

### D1. 四桶分类

对每条去重后的发现，分入恰好一个桶：

| 桶 | 条件 | 说明 |
|----|------|------|
| `decision_needed` | 存在需人工裁决的模糊选择；不知道用户意图则无法判断正确修复方式 | 仅当 `$review_mode` = `"full"` 时可能出现 |
| `patch` | 代码问题，修复方案明确，无需人工输入 | 最常见的桶 |
| `defer` | 既有问题，非本次改动引起；真实存在但现在无法处理 | 已有代码的历史债务 |
| `dismiss` | 噪音、误报、或已在其他地方处理 | 丢弃不输出 |

分类不确定时，优先选择更保守的分类（向严重方向倾斜）。

### D2. 严重性标签映射

四桶分类与严重性标签 [高/中/低] **并存**——两套标签同时写入输出。映射规则：

| 四桶分类 | 严重性标签 | 映射条件 |
|---------|----------|---------|
| `decision_needed` | `[高]` | 始终 |
| `patch` | `[高]` | 多来源命中（如 `blind+edge`）且涉及安全/数据完整性 |
| `patch` | `[中]` | 多来源命中但非安全相关，或单来源但涉及安全/数据 |
| `patch` | `[低]` | 单来源，非安全相关 |
| `defer` | — | 不标严重性，记入"通过项"区域，标注为「已知既有问题」 |
| `dismiss` | — | 丢弃不输出 |

安全/数据关键词判断：发现的 `title` 或 `detail` 中包含以下关键词时视为涉及安全/数据——`安全`、`漏洞`、`注入`、`XSS`、`CSRF`、`认证`、`授权`、`数据丢失`、`数据泄露`、`越权`、`security`、`vulnerability`、`injection`、`data loss`、`data leak`、`auth`。

### D3. 复审场景补充处理

若当前为复审轮次（`$round_number` > 1）：
1. 读取 `$cr_dir/.tmp/review-context.md` 获取「已修复问题清单」
2. 将 Phase C 去重后的发现与已修复清单交叉比对
3. 已修复的问题从发现列表中移除，记入「上轮问题回顾 → 已修复」区域
4. 仍未修复的历史问题保留在发现列表中，额外标注为「上轮遗留」

**写入临时文件**：将分类后的发现列表写入 `$cr_dir/.tmp/classified-findings.json`（JSON 数组格式，每条包含 id/source/title/detail/location/bucket/severity 字段）。

### D4. classified-findings.json Schema

每条发现的完整字段定义（Phase C 规范化 + Phase D 分类的最终产物）：

| 字段 | 类型 | 来源阶段 | 值域 | 说明 |
|------|------|---------|------|------|
| `id` | integer | Phase C1 | 1, 2, 3... | 顺序整数 |
| `source` | string | Phase C1/C2 | `blind` / `edge` / `auditor` / `blind+edge` 等 | 来源层标识，去重合并后为组合值 |
| `title` | string | Phase C1 | — | 一行摘要 |
| `detail` | string | Phase C1 | — | 完整描述（含推理和上下文） |
| `location` | string | Phase C1 | 文件:行号 或空字符串 | 代码位置引用，如 `src/auth.ts:42-58` |
| `bucket` | string | Phase D1 | `decision_needed` / `patch` / `defer` / `dismiss` | 四桶分类 |
| `severity` | string | Phase D2 | `[高]` / `[中]` / `[低]` / `""` | 严重性标签，defer 和 dismiss 为空字符串 |

---

## Phase E：构建输出数据

读取 `$cr_dir/.tmp/classified-findings.json`，将分类后的发现整理为 `assets/output-format.md` 模板所需的结构。

### E1. 新发现区域

每条发现按以下结构输出：

```markdown
### <序号>. [<严重性>] <问题标题>

- **来源**：<blind / edge / auditor / blind+edge 等>
- **分类**：<decision_needed / patch / defer>

- **证据**
  - <代码位置和行为描述，引用具体文件:行号>

- **影响**
  - <对功能/安全/质量的影响说明>

- **建议**
  - <具体修复建议>
```

- `来源` 和 `分类` 为本次新增的可选增强字段
- 严重性标签 `[高/中/低]` 作为主标签，保持与 output-format.md 模板一致

### E2. 通过项区域

- `defer` 桶的发现记入通过项区域，标注为「已知既有问题，非本次改动引起」
- 三层审查中未发现问题的功能模块/文件记入通过项

### E3. 审查层状态标注

若 `$failed_layers` 非空，在审查结论中标注：
- 「注意：<层名称> 审查层不可用，本轮审查结果基于 <可用层数>/3 层。」

### E4. 输出交接

1. `$cr_dir/.tmp/classified-findings.json` 已在 Phase D 写入，SKILL.md Step 5 通过 Read 工具读取
2. `$failed_layers` 保留在上下文中传回 SKILL.md（体积小，无需写文件）
3. Phase E 的格式化输出作为 SKILL.md Step 5 的参考，由 Step 5 按 output-format.md 模板写入最终的审查总结文件
