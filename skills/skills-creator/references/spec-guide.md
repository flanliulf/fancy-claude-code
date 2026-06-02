# Skill 规范指南

## 概述
本文档详细说明 Anthropic Skills 开放标准的规范要点，包括渐进式披露架构、文件命名规范、YAML 头部要求和常见 Skill 类型配置。生成 Skill 时必须参照本文档确保合规。

## 渐进式披露架构

Skills 基于三层加载系统工作，这是核心设计原则：

### 第一层：YAML Frontmatter（触发判断层）
- 只有 `name` 和 `description` 始终加载到系统提示词中
- 作用：帮助智能体判断何时激活该 Skill
- 要求：极度精简，只包含触发所需的最少信息

### 第二层：SKILL.md 正文（核心指令层）
- 仅当智能体判断需要该 Skill 时才加载
- 包含完整的操作步骤、业务逻辑、故障处理
- 要求：不超过 5000 字，指令具体可执行

### 第三层：链接文件（按需探索层）
- `references/`、`scripts/`、`assets/` 中的文件
- 智能体在执行过程中按需主动读取
- 作用：避免一次性加载全部内容，节省 Token

### 内容分配原则
| 内容类型 | 存放位置 | 加载时机 |
|:---------|:---------|:---------|
| 高频使用的核心逻辑 | SKILL.md 正文 | 触发时加载 |
| 低频查阅的详细资料 | references/ 目录 | 按需读取 |
| 复杂 Workflow 细则 | references/ 目录 | Workflow 命中 density gate 时读取 |
| 确定性操作的代码 | scripts/ 目录 | 按需调用 |
| 固定格式的模板资源 | assets/ 目录 | 按需调用 |

## 文件结构规范

```
.claude/skills/<skill-name>/
    ├── SKILL.md                    # 必需：主技能文件（唯一入口）
    ├── SKILL.en.md                 # 必需：英文 mirror 入口
    ├── CHANGELOG.md                # 必需：版本变更记录
    ├── references/                 # 可选：按需加载的补充文档
    │   ├── <ref-name>.md           #   如 api-guide.md、design-spec.md
    │   └── examples.md             #   详细使用示例（如有需要）
    ├── scripts/                    # 可选：可执行脚本
    │   └── <script_name>.py        #   如 validate.py、convert_csv.py
    └── assets/                     # 可选：模板、字体、图标等资源
        └── <asset-name>.md         #   如 report-template.md
```

## 文件命名规范

### Skill 目录命名
- 格式：短横线命名法 kebab-case
- 示例：`csv-converter`、`api-doc-generator`、`code-reviewer`
- 避免：`CSV_Converter`、`ApiDocGenerator`、`csv_converter`
- 禁止：`claude-*`、`codex-*`、`anthropic-*`（保留前缀）

### SKILL.md
- 必须大写：`SKILL.md`（不能是 `skill.md` 或 `Skill.md`）
- 作为中文 canonical 入口，章节标题使用 English（中文）形式，正文内容使用中文
- 命令、路径、字段名、fixture 名称、schema/issue id、API 名称、库名、协议名等技术标识和专有技术术语使用英文
- 官方硬性要求，智能体通过此文件名识别技能

### SKILL.en.md
- 必须与 `SKILL.md` 同步生成，作为英文 mirror 入口
- YAML frontmatter 与 `SKILL.md` 保持一致，包括 `name`、`description`、`allowed-tools`、`metadata.version`、`metadata.author`、`metadata.catalog`
- 英文正文必须镜像 `SKILL.md` 的能力、步骤、限制和引用路径，不新增或删除功能事实
- 当两者冲突时，以 `SKILL.md` 为 canonical 来源并同步修正 `SKILL.en.md`

### CHANGELOG.md
- 必须大写：`CHANGELOG.md`
- 格式基于 Keep a Changelog，版本号遵循 Semantic Versioning
- 版本号必须与 SKILL.md 中 `metadata.version` 保持一致

### YAML name 字段
- 格式：短横线命名法 kebab-case
- 不超过 64 字符
- 与目录名保持一致

### Reference 文件
- 位置：`references/` 子目录内
- 格式：小写短横线（`api-guide.md`、`design-spec.md`）
- 示例文件固定为：`references/examples.md`

### Script 文件
- 位置：`scripts/` 子目录内
- Python：snake_case + `.py`（`convert_csv.py`、`validate_form.py`）
- Shell：kebab-case + `.sh`（`run-checks.sh`）

### Assets 文件
- 位置：`assets/` 子目录内
- 格式：小写短横线（`report-template.md`、`brand-colors.json`）

### 禁止文件
- 严禁在 Skill 目录内创建 `README.md`

## YAML 头部规范

### 必需字段
- `name`：不超过 64 字符，kebab-case
- `description`：不超过 1024 字符，三段式结构
- `metadata`：元数据容器，必须包含 `metadata.version` 和 `metadata.author`

### 可选字段
- `allowed-tools`：限定可用工具列表
- `license`：许可证信息

### YAML 顶级属性限制
只允许以下五个顶级属性：`name`、`description`、`license`、`allowed-tools`、`metadata`

### metadata 字段契约

`metadata` 下仅支持以下字段：
- `metadata.version`：必填，SemVer 格式，必须与 SKILL.en.md 和 CHANGELOG.md 最新版本一致。
- `metadata.author`：必填，记录 Skill 原始作者，创建后版本迭代中保持稳定。
- `metadata.catalog`：可选；当 Skill 归入 catalog 目录时填写，值使用 kebab-case，并与 `forge/<catalog>/<skill-name>/` 路径及 SKILL.en.md mirror 保持一致。未归入 catalog 时省略。

不得擅自新增未登记的 `metadata.*` 字段；确需扩展时，必须同步更新 skills-creator、skills-lint 和 skills-upgrade 的字段契约。

使用 `metadata` 嵌套：
```yaml
metadata:
  version: "1.0.0"
  author: "<author-name>"
  catalog: "<catalog-name>"
```

### 安全红线
- 绝对禁止包含 XML 尖括号（`<` 或 `>`）！系统会拦截并视为指令注入风险
- 严禁包含代码执行逻辑

## description 三段式结构

必须包含三部分：
1. **功能描述（What it does）**：这个 Skill 做什么
2. **触发条件（When to use it）**：什么情况下使用，包含用户常用关键词和文件类型
3. **核心能力（Core capabilities）**：它擅长处理什么

⚠️ **触发关键词必须覆盖中英文双语**：
- 用户可能用中文或英文触发，description 中的关键词必须同时包含中英文常用表述
- 中文关键词应覆盖：正式用语 + 用户口语化表达（如"帮我做个"、"生成一个"）

### 优秀示例（中英文双语触发词）
```
"Analyze Figma design files and generate developer handoff documentation.
Use when user uploads .fig files, requests 'design specs', 'component documentation',
'design-to-code handoff', '设计稿解析', '组件文档', '设计交付', or '设计转开发'.
Capable of extracting design tokens, component hierarchy, and responsive breakpoints."
```

### 错误示例
- 过于模糊："帮助处理项目。"
- 缺少触发条件："创建复杂的多页文档系统。"
- 过于技术化："实现具有层次关系的项目实体模型。"
- 只有英文触发词："Use when user mentions 'create skill', 'new skill'."（缺少中文：'创建技能'、'新建技能'）

## allowed-tools 自动判断规则

| Skill 操作类型 | 推荐 allowed-tools |
|:-------------|:------------------|
| 只读分析类（代码审查、格式验证、内容分析） | Read, Grep, Glob |
| 文档生成类（PRD、设计规范、报告） | Read, Write, Grep, Glob |
| 数据处理类（转换、计算、批量操作） | Read, Write, Bash, Grep, Glob |
| 系统集成类（API 调用、外部命令、自动化脚本） | Read, Write, Bash, Grep, Glob |

### 特殊情况
- 用户明确说"不要修改文件"、"只读就行"：移除 Write
- 需要执行 Python/Shell 脚本：必须包含 Bash
- Grep 和 Glob 通常都保留（除非明确只处理单个固定文件）

## 常见 Skill 类型及配置

| Skill 类型 | 工作流模式 | allowed-tools | 脚本 | Reference | 典型示例 |
|:----------|:----------|:-------------|:-----|:---------|:---------|
| 数据转换 | 顺序工作流 | Read, Write, Bash | 推荐 | 通常不需要 | CSV→Markdown、JSON 格式化 |
| 文档生成 | 迭代优化 | Read, Write | 可选 | 看情况 | API 文档、PRD 生成 |
| 代码分析 | 领域专有智能 | Read, Grep, Glob | 可选 | 推荐 | 代码审查、依赖检查 |
| API 集成 | 多 MCP 协调 | Read, Write, Bash | 必需 | 必需 | 第三方 API 集成 |
| 设计规范 | 领域专有智能 | Read, Write | 不需要 | 必需 | UI 组件库、品牌规范 |
| 文件操作 | 上下文感知 | Read, Write, Bash, Glob | 推荐 | 通常不需要 | 批量重命名、文件合并 |
| 质量检查 | 迭代优化 | Read, Grep, Glob | 推荐 | 推荐 | 格式验证、一致性检查 |
| 跨平台流程 | 多 MCP 协调 | Read, Write, Bash | 可选 | 推荐 | 设计→开发交接 |
| 合规审查 | 领域专有智能 | Read, Write, Grep | 可选 | 必需 | 支付合规、合同审批 |

## SKILL.md 正文规范

- 控制在 5000 字以内
- 章节标题使用 English（中文）形式，例如 `[Overview（技能说明）]`、`[Core Capabilities（核心能力）]`、`[Workflow（执行流程）]`、`[Notes（注意事项）]`
- 正文内容始终使用中文；技术标识和专有技术术语使用英文
- 指令必须具体可执行，禁止模糊表述（"妥善验证"、"适当处理"、"酌情考虑"）
- 使用占位符而非固定内容保持灵活性
- 引用补充文件时使用相对路径：`references/api-guide.md`
- 核心原则：可组合性、可移植性、渐进式披露

## SKILL.en.md mirror 规范

- 控制在 5000 字以内
- 使用英文正文，章节标题为 `[Overview]`、`[Core Capabilities]`、`[Workflow]`、`[Notes]`
- 与 SKILL.md 的章节顺序、能力数量、步骤编号、引用路径、限制条件保持一致
- 不作为功能事实来源；新增能力、流程或限制必须先写入 SKILL.md，再同步翻译到 SKILL.en.md

## Workflow density gate 规范

- 生成或更新入口文件后，使用 deterministic checker 统计，不用 LLM 估算：
  `python3 forge/skill-tooling/skills-lint/scripts/check_skill_density.py <skill-dir>`
- BODY-07 阈值固定为 `workflow_chars > 1500` 且 `workflow_ratio > 0.5`。
- `body_chars >= 4500` 时标记 `near_body_limit`，即使未触发 BODY-07，也应优先精简入口。
- 命中 BODY-07 时，入口 Workflow 只保留阶段路由、何时读取 reference、关键停止条件。
- 详细步骤、规则矩阵、命令清单、长检查列表和示例应抽到 `references/<skill-name>-workflow.md` 或等价 workflow reference。

## 版本说明
- v1.2 (2026-05-26): 增加 Workflow density gate 规范
- v1.1 (2026-05-25): 增加 SKILL.en.md mirror 与中文 canonical 语言规则
- v1.0 (2026-03-25): 初始版本
