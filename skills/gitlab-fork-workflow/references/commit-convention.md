# 约定式提交规范 (Conventional Commits 1.0.0)

## 概述
基于官方约定式提交 1.0.0 规范整理的速查表和模板，用于规范化 Git 提交信息。在 Fork 工作流中，规范的提交信息能让原仓库管理员快速理解你的变更内容，提高 Merge Request 的审查效率。

## 提交信息结构

```
<类型>(<范围>): <简短描述>

[可选的正文，详细描述变更内容，可以分多行]

[可选的脚注，例如 BREAKING CHANGE 或关联的 issue]
```

## 类型 (Type) — 必需

用于说明提交的类别，必须是以下之一：

| 类型 | 说明 | SemVer 对应 |
|:-----|:-----|:-----------|
| **feat** | 新增功能 | MINOR |
| **fix** | 修复 Bug | PATCH |
| **build** | 修改构建系统或外部依赖（gulp, npm 等） | - |
| **chore** | 不修改 src 或 test 的其他更改 | - |
| **ci** | 修改 CI 配置文件和脚本 | - |
| **docs** | 仅修改文档 | - |
| **style** | 不影响代码含义的格式更改（空格、分号等） | - |
| **refactor** | 代码重构，既不修复错误也不添加功能 | - |
| **perf** | 提升性能的代码更改 | - |
| **test** | 添加或修改测试用例 | - |
| **revert** | 撤销之前的提交 | - |

## 范围 (Scope) — 可选

描述代码库中受影响部分的名词，用圆括号包围。

示例：`feat(parser):`、`fix(api):`、`docs(readme):`

## 简短描述 (Description) — 必需

- 紧跟在 `类型(范围):` 后的空格之后
- 使用祈使句（如 "add" 而不是 "added"）
- 首字母小写（英文）
- 结尾不加句号

## 正文 (Body) — 可选

在简短描述之后空一行开始，提供更详细的上下文信息，如变更动机和前后行为对比。

## 脚注 (Footer) — 可选

在正文之后空一行开始，用于：
1. **破坏性变更**：`BREAKING CHANGE: <说明>` 或在类型后加 `!`
2. **关联 Issue**：`Refs: #123` 或 `Closes: #456`

## 破坏性变更 (BREAKING CHANGE)

对应 SemVer 的 MAJOR 版本，两种标记方式：

方式一 — 类型后加 `!`：
```
feat(api)!: send an email to the customer when a product is shipped
```

方式二 — 脚注中声明：
```
chore: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
```

## 实用示例

### 简单修复
```
fix(lang): correct polish language spelling
```

### 新增功能
```
feat: allow provided config object to extend other configs
```

### 带正文的多行提交
```
feat(instructions): add common/frontend/backend instruction directories

新增 instructions 三级规范目录结构：
- common/: 8 个与编程语言无关的通用原则文档
- frontend/: TypeScript 和 JavaScript 特定规范目录
- backend/: Java 和 Python 特定规范目录
- 更新 instructions/README.md 和根 README.md 的目录结构
```

### 包含破坏性变更
```
refactor(auth)!: drop support for JWT, switch to session-based auth
```

### 完整提交（正文 + 脚注）
```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

## 版本说明
- v1.0 (2025-01-01): 基于 Conventional Commits 1.0.0 官方规范整理