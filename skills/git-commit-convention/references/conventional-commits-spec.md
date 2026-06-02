# 约定式提交规范速查表 (Conventional Commits 1.0.0)

## 概述
本文档基于官方约定式提交 1.0.0 规范整理，供 Skill 执行时快速参照，确保生成的 Commit Message 符合标准。

## 提交信息结构模板

```
<类型>(<范围>): <简短描述>

[可选的正文，详细描述变更内容，可以分多行]

[可选的脚注，例如 BREAKING CHANGE 或关联的 issue]
```

## 提交类型 (Type) - 必需

用于说明提交的类别，必须是以下之一：

| 类型 | 说明 | SemVer 对应 |
|:-----|:-----|:-----------|
| **feat** | 新增功能 | MINOR |
| **fix** | 修复 Bug | PATCH |
| **build** | 修改项目构建系统或外部依赖（gulp, npm 等） | - |
| **chore** | 其他不修改 src 或 test 的更改 | - |
| **ci** | 修改 CI 配置文件和脚本（Travis, Circle 等） | - |
| **docs** | 仅修改文档 | - |
| **style** | 不影响代码含义的更改（空格、格式、分号等） | - |
| **refactor** | 代码重构，既不修复错误也不添加功能 | - |
| **perf** | 提升性能的代码更改 | - |
| **test** | 添加或修改测试用例 | - |
| **revert** | 撤销之前的提交 | - |

## 范围 (Scope) - 可选

一个描述代码库中某个部分的名词，用圆括号包围。

- 示例：`feat(parser):`、`fix(api):`
- 推断方法：从变更文件路径中提取模块名（如 `src/api/` → `api`）

## 简短描述 (Description) - 必需

- 紧跟在 `类型(范围):` 后的空格之后
- 使用祈使句（"add" 而非 "added"）
- 结尾不加句号
- 精炼概括变更意图

## 正文 (Body) - 可选

- 在简短描述之后空一行开始
- 详细的上下文信息：变更动机、前后行为对比
- 可以分多行书写

## 脚注 (Footer) - 可选

在正文之后空一行开始，用于两种情况：

1. **破坏性变更 (BREAKING CHANGE)**
2. **关联 Issue 或 PR**

## 破坏性变更 (BREAKING CHANGE)

表示引入了破坏性 API 变更（对应 SemVer MAJOR）。两种标记方式：

1. 在类型/范围后使用 `!` 符号：
   ```
   feat(api)!: send an email to the customer when a product is shipped
   ```

2. 在脚注中添加 `BREAKING CHANGE:`：
   ```
   chore: drop support for Node 6
   BREAKING CHANGE: use JavaScript features not available in Node 6.
   ```

## 实用示例

### 修复一个带范围的 bug
```
fix(lang): correct polish language spelling
```

### 增加一个新功能
```
feat: allow provided config object to extend other configs
```

### 包含 "!" 的破坏性变更
```
refactor(auth)!: drop support for JWT, switch to session-based auth
```

### 包含正文和脚注的完整提交
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
- v1.0 (2026-03-28): 基于 Conventional Commits 1.0.0 官方规范整理
