---
name: gitlab-fork-workflow
description: "Guide GitLab fork repository workflows with upstream setup, fork sync via rebase, conventional commits, and merge request submission. Use when user mentions sync fork, rebase upstream, merge request, MR, upstream, fork workflow, 派生仓库, 合并回原仓库, 同步上游, or needs to contribute from a fork back to the original repository. Do NOT use for general Git branching, regular merge operations, or non-fork repository workflows. Capable of safety checks, feature branch creation, conflict-resolution guidance, force-push handling after rebase, and GitLab MR preparation."
allowed-tools: Read, Write, Bash, Grep, Glob
---

[技能说明]
    管理 GitLab Fork（派生）仓库的完整工作流。确保团队成员在 Fork 仓库上开发时，能够保持与上游仓库同步、遵循约定式提交规范、保持干净的提交历史（rebase 而非 merge），并通过 Merge Request 将变更合并回原仓库。每次操作前自动检查本地仓库状态和环境配置，防止未提交的修改、缺失 upstream 配置或误在默认分支上开发导致的问题。

[核心能力]
    - **环境状态检查**：每次操作前自动检测 upstream 配置、当前分支、工作区状态，根据实际情况分流处理
    - **首次环境设置**：指导添加 upstream 远程仓库，完成一次性初始化配置
    - **功能分支管理**：基于最新上游代码创建规范命名的功能分支（类型前缀式）
    - **上游代码同步**：使用 rebase 而非 merge 同步上游仓库，保持线性提交历史
    - **冲突解决指引**：在 rebase 过程中遇到冲突时，提供逐步解决方案
    - **约定式提交规范**：按照 Conventional Commits 1.0.0 规范格式化提交信息
    - **Merge Request 提交**：指导在 GitLab 页面发起 MR 并填写规范的描述信息
    - **异常恢复**：处理误操作后的回退、强制推送、误在默认分支上提交等场景

[执行流程]

    说明：以下示例使用 `main` 作为原仓库默认分支。如项目默认分支是 `master`、`develop` 或其他名称，请将命令中的 `main` 替换为对应分支名。

    根据用户当前所处的阶段，选择对应的操作指引：

    === 阶段判断 ===

    询问用户当前状态：
    - 如果是第一次使用 Fork 仓库 → 从 Step 0 开始
    - 如果已完成初始化，要开始新功能开发 → 从 Step 1 开始（会自动先执行安全检查）
    - 如果已有本地提交，要同步上游并提交 MR → 从 Step 3 开始（会自动先执行安全检查）
    - 如果只需要同步上游代码 → 只执行 Step 3（会自动先执行安全检查）
    - 如果代码已推送到 Fork 且确认已同步上游 → 只执行 Step 5

    无论从哪个阶段开始，Step 1 ~ Step 4 的操作前必须先完成安全检查。

    === Step 0：首次环境设置（每人只需一次） ===

    确认当前远程仓库配置：
    ```bash
    git remote -v
    ```

    如果只有 origin（指向自己的 Fork 仓库），添加 upstream：
    ```bash
    git remote add upstream <原仓库 HTTPS 地址>
    ```

    验证添加成功：
    ```bash
    git remote -v
    ```
    预期输出应包含 origin（自己的仓库）和 upstream（原仓库）两个远程地址。

    完成后拉取上游数据：
    ```bash
    git fetch upstream
    ```

    === 安全检查：操作前状态检查（Step 1 ~ Step 4 前必须执行） ===

    1. 检查 upstream 是否已配置：
       ```bash
       git remote -v
       ```
       如果输出中没有 `upstream`，先执行 Step 0 添加 upstream，再继续后续步骤。

    2. 检查当前分支：
       ```bash
       git branch --show-current
       ```

    3. 检查工作区状态：
       ```bash
       git status
       ```

    4. 根据检查结果分流处理：

       情况 A — 工作区干净，当前在 main 分支：
       正常流程，直接进入目标步骤。

       情况 B — 工作区干净，当前在功能分支：
       已在功能分支开发中，根据需要进入 Step 2（提交）或 Step 3（同步上游）。

       情况 C — 有未提交的修改（工作区或暂存区不干净）：
       必须先处理未提交的修改，再继续操作。两种方案：

       方案 C1 — 修改已完成，直接提交：
       按照 Step 2 的规范提交代码，然后继续后续操作。

       方案 C2 — 修改未完成，暂时保存：
       ```bash
       git stash push -m "WIP: 临时保存未完成的修改"
       ```
       完成分支切换或 rebase 后，恢复修改：
       ```bash
       git stash pop
       ```
       如果 stash pop 遇到冲突，手动解决冲突文件后执行 `git add <文件>`。
       查看当前暂存列表：`git stash list`

       情况 D — 已在 main 上直接 commit 了代码（不在功能分支上）：
       将 main 上的提交转移到新功能分支，然后让 main 回到与上游一致的状态：
       ```bash
       git checkout -b <类型>/<分支名>
       git checkout main
       git fetch upstream
       git reset --hard upstream/main
       git checkout <类型>/<分支名>
       ```
       说明：`git checkout -b` 创建新分支时会自动带上当前分支的所有提交，
       然后用 `reset --hard` 让 main 恢复干净。

    === Step 1：创建功能分支 ===

    先同步上游最新代码，确保功能分支基于最新代码创建：
    ```bash
    git checkout main
    git fetch upstream
    git rebase upstream/main
    ```
    仅当本地 main 无私有提交时使用 rebase。如需严格镜像上游，可使用 `git reset --hard upstream/main`。

    创建并切换到功能分支，命名规范为 `<类型>/<简短描述>`：
    ```bash
    git checkout -b <类型>/<简短描述>
    ```

    分支命名规则（类型与提交类型一致）：
    - feat/xxx — 新功能
    - fix/xxx — 修复 Bug
    - docs/xxx — 文档修改
    - refactor/xxx — 代码重构
    - chore/xxx — 构建/工具变更
    - test/xxx — 测试相关
    - perf/xxx — 性能优化

    示例：
    ```bash
    git checkout -b feat/add-user-auth
    git checkout -b fix/login-redirect-error
    git checkout -b docs/update-api-guide
    ```

    === Step 2：本地开发与提交 ===

    开发完成后，按照约定式提交规范（Conventional Commits）提交代码。

    提交信息格式（详细规范参见 `references/commit-convention.md`）：
    ```
    <类型>(<范围>): <简短描述>

    [可选正文]

    [可选脚注]
    ```

    提交前先检查变更范围，确认只包含本次改动的相关文件：
    ```bash
    git status
    ```

    确认无误后执行提交：
    ```bash
    git add .
    git commit -m "<类型>(<范围>): <简短描述>"
    ```

    如果 `git status` 显示有不相关的文件变更，改用精确添加：
    ```bash
    git add <相关文件1> <相关文件2>
    git commit -m "<类型>(<范围>): <简短描述>"
    ```

    示例：
    ```bash
    git commit -m "feat(auth): add JWT token refresh mechanism"
    git commit -m "fix(api): correct pagination offset calculation"
    ```

    如需多行提交信息：
    ```bash
    git commit -m "feat(instructions): add common/frontend/backend instruction directories

    新增 instructions 三级规范目录结构：
    - common/: 通用原则文档
    - frontend/: TypeScript 和 JavaScript 特定规范
    - backend/: Java 和 Python 特定规范"
    ```

    === Step 3：同步上游代码（rebase） ===

    在 push 之前，必须先同步上游仓库的最新代码，使用 rebase 保持线性历史：

    ```bash
    git fetch upstream
    git rebase upstream/main
    ```

    该步骤适用于以原仓库默认分支为基础创建的功能分支。如果功能分支基于其他分支创建，请将 `upstream/main` 替换为对应的上游分支。

    三种结果及对应处理：

    结果 A — 无冲突，自动完成：
    提示 `Successfully rebased and updated`，直接进入 Step 4。

    结果 B — 有冲突，需手动解决：
    1. 命令行提示 `CONFLICT`，查看冲突文件列表
    2. 在冲突文件中找到 `<<<<<<<`、`=======`、`>>>>>>>` 标记
    3. 保留正确的代码，删除冲突标记
    4. 标记冲突已解决（不要执行 git commit）：
       ```bash
       git add <冲突文件>
       ```
    5. 继续 rebase：
       ```bash
       git rebase --continue
       ```
    6. 重复直到所有冲突解决完毕

    结果 C — 情况复杂想放弃：
    ```bash
    git rebase --abort
    ```
    这会回到 rebase 之前的状态，不会丢失任何代码。

    === Step 4：推送到自己的 Fork 仓库 ===

    如果是功能分支的首次推送，使用 `-u` 设置上游跟踪：
    ```bash
    git push -u origin <分支名>
    ```
    设置跟踪后，后续推送可直接使用 `git push`。

    如果该分支之前已经 push 过，rebase 后需要强制推送：
    ```bash
    git push origin <分支名> --force-with-lease
    ```

    ⚠️ `--force-with-lease` 比 `--force` 更安全：如果远端分支有预期之外的新提交，会拒绝覆盖而非无条件覆写。只用于自己的 Fork 仓库的功能分支，绝对不要对原仓库或共享分支使用。

    === Step 5：在 GitLab 页面发起 Merge Request ===

    1. 打开自己的 Fork 仓库页面
    2. 点击左侧导航栏 **Merge requests** → **New merge request**
       （如果刚 push，页面顶部通常会出现快捷创建按钮，可直接点击）
    3. 设置源和目标：
       - Source branch：自己的仓库 / 功能分支
       - Target branch：原仓库 / main（或项目的默认分支）
    4. 点击 **Compare branches and continue**
    5. 填写 MR 信息：
       - Title：与最主要的 commit message 保持一致，或概括性描述
       - Description：详细说明变更内容、原因、影响范围
       - Assignee/Reviewer：指派原仓库负责人（如知道）
    6. 点击 **Submit merge request**

    === Step 6：等待审查与迭代 ===

    提交 MR 后：
    - 如果审查通过：原仓库管理员点击 Merge，流程完成
    - 如果需要修改：在本地功能分支上继续修改，commit 后 push，MR 会自动更新，不需要重新创建

    功能合并完成后，清理本地环境：
    ```bash
    git checkout main
    git fetch upstream
    git rebase upstream/main
    git branch -d <分支名>
    ```

    如团队要求自己的 Fork main 也与上游保持同步，再执行：
    ```bash
    git push origin main
    ```

[注意事项]
    - 每次执行 Git 操作前，先通过安全检查确认 upstream 配置、工作区状态和当前分支
    - 永远不要直接在 main 分支上开发和 commit，main 应始终与 upstream/main 保持一致
    - 始终使用 `rebase` 而非 `merge` 同步上游代码，保持线性提交历史
    - rebase 后更新自己 Fork 中的功能分支，优先使用 `--force-with-lease`；只有在明确需要无条件覆盖时才使用 `--force`
    - 每次创建新功能分支前，先同步上游最新代码
    - 提交前先运行 `git status` 确认变更范围，避免误提交不相关文件
    - 提交信息必须遵循约定式提交规范，类型字段（feat/fix/docs 等）不可省略
    - 一个功能分支对应一个 MR，避免在同一分支上混合多个不相关的功能
    - 如果 rebase 过程中情况复杂无法处理，随时可以 `git rebase --abort` 安全回退
    - 首次设置 upstream（Step 0）每人只需执行一次，后续开发直接从 Step 1 开始
    - `git stash` 是临时方案，暂存的修改应尽快恢复并正式提交，避免遗忘
    - 以上示例中的 `main` 指原仓库默认分支，如项目使用 `master` 或其他分支名，请对应替换