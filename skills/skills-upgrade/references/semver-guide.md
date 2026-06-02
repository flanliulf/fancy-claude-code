# 语义化版本规则与 CHANGELOG 格式规范

## 概述

本文档定义 Skill 版本管理的语义化版本判断规则和 CHANGELOG 格式规范。用于指导 `skills-upgrade` 在分析变更时正确判断版本号升级类型，并生成规范的 CHANGELOG 记录。

## 版本号格式

遵循 [Semantic Versioning 2.0.0](https://semver.org/)，格式为 `MAJOR.MINOR.PATCH`。

示例：`1.2.3` 表示主版本 1、次版本 2、修订版 3。

## MAJOR 升级（X.0.0）

**条件**：不兼容的破坏性变更，会影响 Skill 的触发时机或行为方式。

### 触发场景

- 触发条件（description）大幅重写，导致触发时机根本性改变
- 核心执行流程重写，输入/输出不兼容旧版本
- 移除已发布的核心功能
- 更改 `allowed-tools`，移除之前依赖的工具

### 示例

- `skills-creator` 从交互式创建改为批量自动化创建（执行流程完全不同）
- `skills-lint` 的检查规则 ID 全部重新编号（影响已有的引用）
- 移除对某种文件格式的支持（如不再支持 .csv 输入）

## MINOR 升级（x.Y.0）

**条件**：向后兼容的新功能或重大改进。

### 触发场景

- 新增核心能力或工作流步骤
- 新增 reference 文档或脚本
- 新增触发关键词（不移除已有的）
- 显著改进现有功能的质量或覆盖范围
- 新增对额外文件格式或场景的支持
- description 增加新的触发词类别（如新增中文触发词覆盖）

### 示例

- `skills-creator` 新增中英文双语触发词规则（不改变已有创建流程）→ 1.0.0 → 1.1.0
- `skills-creator` 新增 SKILL.en.md mirror 生成规则（不移除旧文件）→ 1.3.0 → 1.4.0
- `skills-lint` 新增 5 条检查规则（不改变已有规则）→ 1.0.0 → 1.1.0
- 新增 `references/examples.md` 补充使用示例

## PATCH 升级（x.y.Z）

**条件**：向后兼容的缺陷修复或微小调整。

### 触发场景

- 修复拼写错误、格式错误
- 修复引用路径错误
- 调整措辞使指令更清晰（不改变行为）
- 修复 YAML 格式问题
- 补充遗漏的小细节

### 示例

- 修复 `references/spec-guide.md` 中的断链 → 1.1.0 → 1.1.1
- 修正 description 中的拼写错误 → 1.0.0 → 1.0.1

## 判断决策树

```
变更是否移除已有功能或改变触发时机？
├── 是 → MAJOR（X.0.0）
└── 否 → 变更是否新增功能或显著改进？
    ├── 是 → MINOR（x.Y.0）
    └── 否 → PATCH（x.y.Z）
```

**关键判断点**：
- 用户升级后，旧的使用方式是否仍然有效？有效 → 不是 MAJOR
- 变更是否增加了新的可观察能力？是 → MINOR
- 变更是否仅修正错误或措辞？是 → PATCH

## CHANGELOG 格式规范

### 基本结构

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- 新增的功能或能力

### Changed
- 已有功能的变更

### Fixed
- 修复的缺陷

### Removed
- 移除的功能
```

### 规则

1. **时间倒序**：新版本插入在上一版本之前
2. **版本号一致**：与 SKILL.md 和 SKILL.en.md 中 `metadata.version` 保持同步
3. **分类必选**：只列出有内容的分类（如无 Removed 则不写该标题）
4. **条目格式**：每条以 `-` 开头，简明描述变更内容
5. **日期格式**：`YYYY-MM-DD`

### 完整示例

```markdown
## [1.1.0] - 2026-03-25

### Added
- description 中英文双语触发词覆盖规则
- CLAUDE.md 中新增"Skill 版本管理规范"章节

### Changed
- Q3 提问模板增加中英文双语要求
- Step 6 生成规则增加双语触发词检查

### Fixed
- skills-creator 自身 description 缺少中文触发关键词

## [1.0.0] - 2026-03-25

### 初始版本
- 功能 A
- 功能 B
```

### 已知问题处理

- 在对应版本下单独列出已知问题
- 修复后用删除线标注并指向修复版本：
  ```
  - ~~**问题描述**~~ → 已在 v1.1.0 修复
  ```

## 多副本同步规范

如果 Skill 同时存在于多个位置（如 `forge/`、`.claude/skills/`、`.agents/skills/`、`.codex/skills/`），版本升级时必须同步所有实际存在的副本：

1. 先更新源码位置（`forge/`）
2. 同步更新 SKILL.md、SKILL.en.md、CHANGELOG.md，以及本次变更涉及的 references/、scripts/、assets/
3. 再同步到实际存在的部署位置（`.claude/skills/`、`.agents/skills/`、`.codex/skills/`）
4. 对不存在的安装根只记录为"未发现"，不得凭空创建
5. 验证所有副本完全一致

## 双语入口版本规范

- SKILL.md 是中文 canonical 入口，SKILL.en.md 是英文 mirror。
- 版本升级时必须同时更新两个入口的 `metadata.version`。
- 如果 SKILL.en.md 缺失，应在同次升级中补建，并在 CHANGELOG.md 的 Added 中记录。
- 如果 SKILL.md 与 SKILL.en.md 内容冲突，以 SKILL.md 为事实来源，先修正 SKILL.md，再同步翻译 SKILL.en.md。

## 版本说明
- v1.1 (2026-05-25): 增加 SKILL.en.md mirror 与多安装根同步规则
- v1.0 (2026-03-25): 初始版本
