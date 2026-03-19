1. 总结最近的项目修改内容
2. 按照以下“约定式提交规范”，简单扼要的组织 Git Commit Message；
3. 提交到本地 Git 仓库，并推送要远程仓库


## 1 约定式提交规范 (Conventional Commits Specifications)

这是根据官方的约定式提交 1.0.0 规范整理的速查表和模板，用于规范化 Git 提交信息。

### 1.1 提交信息结构模板

```shell
<类型>(<范围>): <简短描述>

[可选的正文，详细描述变更内容，可以分多行]

[可选的脚注，例如 BREAKING CHANGE 或关联的 issue]
```

---

### 1.2 `<类型>` (Type) - 必需

用于说明提交的类别，必须是以下之一：

*   **feat**: 新增功能 (对应 SemVer 的 `MINOR` 版本)
*   **fix**: 修复 Bug (对应 SemVer 的 `PATCH` 版本)

**其他推荐类型:**

*   **build**: 修改项目构建系统或外部依赖（例如：gulp, broccoli, npm）
*   **chore**: 其他不修改 `src` 或 `test` 文件的更改（例如：修改构建流程、辅助工具）
*   **ci**: 修改 CI 配置文件和脚本（例如：Travis, Circle, BrowserStack, SauceLabs）
*   **docs**: 仅修改文档
*   **style**: 不影响代码含义的更改（空格、格式、缺少分号等）
*   **refactor**: 代码重构，既不修复错误也不添加功能
*   **perf**: 提升性能的代码更改
*   **test**: 添加或修改测试用例
*   **revert**: 撤销之前的提交

---

### 1.3 `<范围>` (Scope) - 可选

一个描述代码库中某个部分的名词，用圆括号包围，用于提供额外的上下文信息。

*   **示例**: `feat(parser):`, `fix(api):`

---

### 1.4 `<简短描述>` (Description) - 必需

对代码变更的简短、精炼的描述。

* 紧跟在 `类型(范围):` 后的空格之后。
* 建议使用祈使句，例如 "add" 而不是 "added"。
* 结尾不加句号。

---

### 1.5 `[正文]` (Body) - 可选

在简短描述之后，空一行开始。用于提供更详细的上下文信息，如变更的动机和前后的行为对比。

---

### 1.6 `[脚注]` (Footer) - 可选

在正文之后，空一行开始。用于两种情况：

1.  **破坏性变更 (Breaking Change)**
2.  **关联 Issue 或 PR**

---

### 1.7 破坏性变更 (BREAKING CHANGE)

表示引入了破坏性 API 变更，对应 SemVer 的 `MAJOR` 版本。可以通过两种方式标记：

1.  在**类型/范围**后使用 `!` 符号。
    *   **示例**: `feat(api)!: send an email to the customer when a product is shipped`
2.  在**脚注**中添加 `BREAKING CHANGE:`。
    *   **示例**:

	```shell




chore: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
	```

---

### 1.8 实用示例

#### 1.8.1 **示例 1: 修复一个带范围的 bug**

```shell
fix(lang): correct polish language spelling
```

#### 1.8.2 **示例 2: 增加一个新功能**

```shell
feat: allow provided config object to extend other configs
```

#### 1.8.3 **示例 3: 包含 `!` 的破坏性变更**

```shell
refactor(auth)!: drop support for JWT, switch to session-based auth
```

#### 1.8.4 **示例 4: 包含正文和脚注的完整提交**

```shell
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```
