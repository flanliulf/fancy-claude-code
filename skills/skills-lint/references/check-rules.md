# Skill 规范检查规则清单

## 概述

本文档定义了 Agent Skill 规范检查的 34 条规则，涵盖 YAML 头部、description 质量、文件结构、版本一致性、正文约束、命名规范、双语 mirror 和文件分类合理性八个维度。规则源自 Anthropic Skills 开放标准规范和 skills-creator 项目实践。

## 1. YAML Frontmatter 检查（5 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| YML-01 | name 格式 | Error | kebab-case，不超过 64 字符，与目录名一致 |
| YML-02 | description 长度 | Error | 不超过 1024 字符 |
| YML-03 | description 三段式 | Warning | 包含功能描述 + 触发条件 + 核心能力三部分 |
| YML-04 | 顶级属性与 metadata 合法性 | Error | 只允许 name、description、license、allowed-tools、metadata 五个顶级属性；metadata 仅支持 version、author、catalog |
| YML-05 | 安全检查 | Error | 无 XML 尖括号（`<` 或 `>`），无代码执行逻辑 |

### 详细说明

**YML-01 name 格式**：
- 必须为短横线命名法（kebab-case）
- 长度不超过 64 字符
- 必须与 Skill 目录名完全一致
- 不得以 `claude-`、`codex-` 或 `anthropic-` 开头（保留前缀）
- 检查方法：正则匹配 `^[a-z0-9]+(-[a-z0-9]+)*$`

**YML-04 顶级属性与 metadata 合法性**：
- YAML frontmatter 严格只允许五个顶级属性
- `metadata` 下仅支持 `version`、`author`、`catalog` 三个子属性
- `metadata.version` 与 `metadata.author` 的存在性分别由 VER-01、VER-04 报告
- `metadata.catalog` 可选；存在时必须为非空 kebab-case，并与 SKILL.en.md mirror 对齐
- 任何其他顶级属性（如 `version`、`author`）均为非法
- 任何未登记的 `metadata.*` 子属性均为非法

**YML-05 安全检查**：
- 扫描 YAML 区域（`---` 到 `---` 之间）是否包含 `<` 或 `>` 字符
- 检查是否包含 Shell 命令、代码片段等执行逻辑

## 2. description 质量检查（3 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| DESC-01 | 中英文双语触发词 | Warning | 至少包含 2 个中文触发关键词 + 2 个英文触发关键词 |
| DESC-02 | 触发词具体性 | Warning | 不使用过于模糊的通用词（如"处理项目"、"帮助用户"） |
| DESC-03 | 无尖括号 | Error | description 字段中不包含 `<` 或 `>` 字符 |

### 详细说明

**DESC-01 中英文双语触发词**：
- 检查 description 中单引号包裹的关键词
- 统计中文关键词数量（含中文字符的关键词）和英文关键词数量
- 至少各 2 个才算通过
- 中文关键词应覆盖正式用语和口语化表达

**DESC-02 触发词具体性**：
- 检测是否使用过于宽泛的触发词
- 模糊词黑名单："帮助处理项目"、"处理文件"、"完成任务" 等
- 应使用领域特定的具体描述

## 3. 文件结构检查（6 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| FILE-01 | SKILL.md 大写 | Error | 文件名严格为 `SKILL.md`，不接受其他大小写 |
| FILE-02 | 目录名 kebab-case | Error | 目录名无大写字母、无下划线、无空格 |
| FILE-03 | 无 README.md | Error | Skill 目录内不存在 `README.md` 文件 |
| FILE-04 | CHANGELOG.md 存在 | Warning | 每个 Skill 应包含 `CHANGELOG.md` |
| FILE-05 | 无保留前缀 | Error | 目录名不以 `claude-`、`codex-` 或 `anthropic-` 开头 |
| FILE-06 | SKILL.en.md 存在 | Warning | 每个 Skill 应包含英文 mirror 文件 `SKILL.en.md` |

## 4. 版本一致性与 metadata 字段检查（5 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| VER-01 | metadata.version 存在 | Warning | SKILL.md 的 YAML 中包含 `metadata.version` 字段 |
| VER-02 | 版本号一致 | Error | SKILL.md 中 `metadata.version` 与 CHANGELOG.md 最新版本号一致 |
| VER-03 | CHANGELOG 日期格式 | Warning | `## [x.y.z] - ` 后的日期匹配 `YYYY-MM-DD` 格式 |
| VER-04 | metadata.author 存在 | Warning | SKILL.md 的 YAML 中包含 `metadata.author` 字段且非空 |
| VER-05 | SKILL.en.md 版本一致 | Error | SKILL.en.md 的 `metadata.version` 与 SKILL.md 完全一致 |

### 详细说明

**VER-02 版本号一致**：
- 从 SKILL.md 的 YAML frontmatter 中提取 `metadata.version` 值
- 从 CHANGELOG.md 中提取第一个 `## [x.y.z]` 格式的版本号
- 两者必须完全一致
- 版本号格式必须符合语义化版本（MAJOR.MINOR.PATCH）

**VER-03 CHANGELOG 日期格式**：
- 检查 CHANGELOG.md 中所有 `## [x.y.z] - <date>` 行
- 日期部分必须匹配正则 `^\d{4}-\d{2}-\d{2}$`（即 YYYY-MM-DD）
- 不合法示例：`2026/04/07`、`April 7, 2026`、`20260407`

**VER-04 metadata.author 存在**：
- 检查 SKILL.md 的 YAML frontmatter 中是否包含 `metadata.author` 字段
- 字段值必须非空（不能为空字符串或仅空格）
- author 记录 Skill 的原始作者，创建时写入，后续版本迭代不变
- 缺失时建议：从 `git config user.name` 获取作者名并添加到 metadata 中

**metadata.catalog 字段契约**：
- `metadata.catalog` 是可选字段；不存在时不单独报错
- 存在时必须使用 kebab-case，且不得为空字符串或仅空格
- 当 Skill 位于 `forge/<catalog>/<skill-name>/`、`.claude/skills/<skill-name>/` 或 `.agents/skills/<skill-name>/` 的同步副本中时，catalog 值应表达源码 catalog 归属
- SKILL.en.md 中的 `metadata.catalog` 必须与 SKILL.md 一致，由 MIRROR-01 报告
- 缺失但目录明显属于某个 catalog 时，建议补充 `metadata.catalog` 并同步 mirror

**VER-05 SKILL.en.md 版本一致**：
- 如果 SKILL.en.md 存在，提取其 YAML frontmatter 中的 `metadata.version`
- 与 SKILL.md 中的 `metadata.version` 必须完全一致
- 如果 SKILL.en.md 缺失，本规则记为未检查，由 FILE-06 报告

## 5. 正文质量检查（8 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| BODY-01 | 字数限制 | Error | SKILL.md 正文（不含 YAML 头部）不超过 5000 字符 |
| BODY-02 | 必需章节 | Warning | 包含 [Overview（技能说明）]、[Core Capabilities（核心能力）]、[Workflow（执行流程）]、[Notes（注意事项）] 四个章节 |
| BODY-03 | 引用路径正确 | Warning | `references/` 引用路径对应的文件实际存在 |
| BODY-04 | 无模糊表述 | Warning | 不含"妥善验证"、"适当处理"、"酌情考虑"等模糊指令词 |
| BODY-05 | 核心能力条数 | Warning | [Core Capabilities（核心能力）] 章节内 `- **` 开头的行数应在 4-8 范围内 |
| BODY-06 | 中文 canonical 语言规则 | Warning | SKILL.md 章节标题使用 English（中文）形式，正文内容使用中文，技术标识使用英文 |
| BODY-07 | Workflow density | Warning | `workflow_chars > 1500` 且 `workflow_ratio > 0.5` |
| BODY-08 | Workflow extraction | Warning | 命中 BODY-07 时入口应引用 `references/*workflow*.md` 或等价流程 reference |

### 详细说明

**BODY-01 字数限制**：
- 字数计算从 YAML 结束标记 `---` 之后开始
- 统计字符数（中英文混合场景下以字符数为准）
- 超过 5000 字符需将低频内容拆分到 `references/`

**BODY-04 无模糊表述**：
- 模糊词检测列表："妥善验证"、"适当处理"、"酌情考虑"、"合理安排"、"必要时"
- 这些词在指令中不可执行，应替换为具体操作描述

**BODY-05 核心能力条数**：
- 统计 [Core Capabilities（核心能力）] 章节内以 `- **` 开头的行数
- 合理范围为 4-8 条，过少说明能力描述不完整，过多说明应精简或拆分
- [Core Capabilities（核心能力）] 章节的范围从标题到下一个 `[` 开头的章节标题

**BODY-06 中文 canonical 语言规则**：
- SKILL.md 必须使用中文正文，章节标题使用 English（中文）形式
- 命令、路径、字段名、fixture 名称、schema/issue id、API 名称、库名、协议名等技术标识和专有技术术语应保留英文
- 检查方式以结构扫描和人工报告建议为主：缺少 English（中文）章节标题时警告；正文大量英文叙述时警告

**BODY-07 Workflow density**：
- 必须使用 `scripts/check_skill_density.py <skill-dir>` 的 JSON 输出，不允许用 LLM 估算替代脚本结果
- 对 SKILL.md 和 SKILL.en.md 分别检查 `triggered_density_warning`
- 阈值固定为 `workflow_chars > 1500` 且 `workflow_ratio > 0.5`
- `near_body_limit` 为 true 时，在详情中提示正文接近 5000 字上限

**BODY-08 Workflow extraction**：
- 仅在同一入口文件命中 BODY-07 时检查
- 如果 `has_workflow_reference` 为 false，报告 Warning
- 修复建议：创建 `references/<skill-name>-workflow.md` 或等价 workflow reference，把详细步骤、规则矩阵、命令清单和长校验列表移入 reference，入口 Workflow 只保留阶段路由、读取条件和停止条件

## 6. 命名规范检查（3 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| NAME-01 | Reference 文件命名 | Warning | `references/` 下的文件使用小写短横线（如 `api-guide.md`） |
| NAME-02 | Script 文件命名 | Warning | Python 文件 snake_case（如 `convert_csv.py`），Shell 文件 kebab-case（如 `run-checks.sh`） |
| NAME-03 | Assets 文件命名 | Warning | `assets/` 下的文件使用小写短横线（如 `report-template.md`） |

## 7. 双语 mirror 检查（3 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| MIRROR-01 | YAML frontmatter 对齐 | Error | SKILL.en.md 的 name、description、allowed-tools、metadata.author、metadata.catalog 与 SKILL.md 保持一致 |
| MIRROR-02 | 英文章节齐备 | Warning | SKILL.en.md 包含 [Overview]、[Core Capabilities]、[Workflow]、[Notes] 四个章节 |
| MIRROR-03 | 引用路径同步 | Warning | SKILL.en.md 引用的 references/、scripts/、assets/ 路径均存在，并与 SKILL.md 的引用路径不冲突 |

### 详细说明

**MIRROR-01 YAML frontmatter 对齐**：
- SKILL.en.md 是 SKILL.md 的英文 mirror，不能使用独立 metadata
- 允许正文语言不同，但 YAML 触发和版本信息必须一致
- `metadata.version` 的一致性由 VER-05 单独报告

**MIRROR-02 英文章节齐备**：
- SKILL.en.md 至少包含 [Overview]、[Core Capabilities]、[Workflow]、[Notes]
- 各章节应与 SKILL.md 的四个 canonical 章节语义对应

**MIRROR-03 引用路径同步**：
- 扫描 SKILL.en.md 中的相对路径引用
- 所有引用的 `references/`、`scripts/`、`assets/` 路径必须存在
- 如 SKILL.md 与 SKILL.en.md 引用集合明显不同，报告 Warning，提示人工核对 mirror 漂移

## 8. 文件分类合理性检查（3 条）

| 规则 ID | 检查项 | 严重级别 | 判断标准 |
|:--------|:-------|:---------|:---------|
| CLASS-01 | 模板文件应放 assets/ | Warning | `references/` 下的 .md 文件如果包含 ` ```markdown` 代码块包裹的完整文档骨架，应放在 `assets/` |
| CLASS-02 | 脚本文件应放 scripts/ | Warning | `references/` 或 `assets/` 下存在 `.py` 或 `.sh` 文件 |
| CLASS-03 | 知识文档应放 references/ | Warning | `assets/` 下的 .md 文件如果不含模板骨架（无 ` ```markdown` 代码块），应放在 `references/` |

### 详细说明

**CLASS-01 模板文件应放 assets/**：
- 扫描 `references/` 下所有 .md 文件
- 如果文件内容包含 ` ```markdown` 代码块（即用代码块包裹的完整文档骨架/模板），则该文件属于"固定格式的模板资源"
- 根据渐进式披露架构，模板资源应放在 `assets/` 目录，而非 `references/`
- 额外信号：SKILL.md 中对该文件的引用描述包含"模板"、"按此格式生成"、"严格按照模板"等字样
- 检查方法：读取 `references/` 下每个 .md 文件，搜索 ` ```markdown` 出现次数，>=1 则触发警告

**CLASS-02 脚本文件应放 scripts/**：
- 扫描 `references/` 和 `assets/` 下的所有文件
- 如果存在 `.py` 或 `.sh` 后缀的文件，触发警告
- 根据渐进式披露架构，可执行脚本应放在 `scripts/` 目录

**CLASS-03 知识文档应放 references/**：
- 扫描 `assets/` 下所有 .md 文件
- 如果文件内容不包含任何 ` ```markdown` 代码块（即纯知识性说明文档，无模板骨架），则该文件属于"低频查阅的详细资料"
- 根据渐进式披露架构，知识性文档应放在 `references/` 目录，而非 `assets/`

## 严重级别说明

| 级别 | 含义 | 处理要求 |
|:-----|:-----|:---------|
| **Error** | 违反官方硬性要求 | 必须修复，否则 Skill 可能无法正常工作 |
| **Warning** | 影响质量但不阻塞使用 | 建议修复，提升 Skill 的触发准确率和可维护性 |

## 检查报告格式

检查完成后输出标准化报告：

```
📋 Skill 规范检查报告：<skill-name>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
| # | 规则 ID | 检查项 | 状态 | 详情 |
|---|---------|--------|------|------|
| 1 | YML-01  | name 格式 | ✅ | — |
| 2 | YML-02  | description 长度 | ✅ | 620/1024 字符 |
| ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
总结：X/34 项通过，Y 项警告，Z 项错误
状态：🟢 全部通过 / 🟡 有警告 / 🔴 有错误
```

## 版本说明
- v1.3 (2026-05-26): 增加 Workflow density 和 Workflow extraction 检查，总计 34 条规则
- v1.2 (2026-05-25): 增加 SKILL.en.md mirror、版本一致性和中文 canonical 语言规则检查，总计 32 条规则
- v1.0 (2026-03-25): 初始版本，22 条规则
