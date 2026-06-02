---
name: git-commit-convention
description: "Summarize recent project changes, generate standardized Git commit messages following Conventional Commits specification, commit to local repository, and optionally push to remote. Use when user mentions 'git commit', 'commit', 'gc', 'gcp', 'commit and push', 'push', 'conventional commit', 'submit code', 'commit message', '提交代码', '提交到 Git', 'Git 提交', '生成提交信息', '规范提交', '约定式提交', '帮我提交', '代码提交', '提交并推送', '推送到远程', '同步远程', or wants to commit staged/unstaged changes with well-formatted messages. Capable of multi-file change summarization, Conventional Commits type classification, scope extraction, breaking change detection, automated git commit execution, and conditional remote push with safety checks."
allowed-tools: Read, Bash, Grep, Glob
metadata:
  version: "1.4.0"
---

[技能说明]
    自动分析项目最近的代码变更，按照约定式提交（Conventional Commits 1.0.0）规范生成结构化的 Git Commit Message（默认中文描述，支持切换英文），提交到本地 Git 仓库，并可根据用户意图选择性推送到远程仓库。完整的约定式提交规范速查表详见 `references/conventional-commits-spec.md`。

[核心能力]
    - **变更摘要分析**：通过 `git diff` 和 `git status` 全面分析暂存区和工作区的代码变更，提取核心修改内容
    - **提交类型判断**：根据变更内容自动匹配最合适的提交类型（feat/fix/refactor/docs/chore/build/ci/style/perf/test/revert）
    - **范围自动提取**：从变更文件路径和模块归属中推断合理的 scope（如 api、auth、parser）
    - **破坏性变更检测**：识别 API 签名变更、依赖移除、配置格式变化等潜在 BREAKING CHANGE
    - **Commit Message 规范生成**：严格按照 `<类型>(<范围>): <简短描述>` 格式生成，默认中文描述，支持用户选择中文或英文，可选附带正文和脚注
    - **多变更分组提交**：当一次变更涉及多个 Story 或混合业务开发与基础设施变更时，按"Story 优先 → 基础设施独立"的策略自动分组，生成多条 commit message 并分批提交，保证提交记录的颗粒度和可读性
    - **安全提交**：提交前检查是否存在敏感文件（.env、credentials 等），避免误提交
    - **智能推送**：提交完成后根据用户意图和仓库状态决定是否推送到远程，自动检测远程仓库配置、分支跟踪关系，拒绝向 main/master 直接 force push

[执行流程]
    本 Skill 采用顺序工作流模式：分析→语言选择→分组生成→确认→提交→推送（可选）。

    Step 1：分析项目变更
        - 执行 `git status` 查看工作区状态（已暂存、未暂存、未追踪文件）
        - 执行 `git diff --cached` 查看暂存区变更详情
        - 执行 `git diff` 查看未暂存变更详情
        - 如果暂存区为空且有未暂存变更，提示用户是否需要先执行 `git add`
        - 执行 `git log --oneline -10` 查看最近 10 条提交记录，了解项目提交风格
        - 生成数据：变更文件列表、变更内容摘要、最近提交记录

    Step 2：变更分组与 Commit Message 生成
        - 接收数据：Step 1 的变更摘要和最近提交记录
        - 安全检查：扫描变更文件列表，如发现 .env、credentials.json、*.key 等敏感文件，发出警告并建议从暂存区移除

        语言选择（在生成 commit message 之前必须确认）：
            - 默认语言为**中文**
            - 向用户展示语言选项并请求确认：
              "🌐 Commit Message 描述语言：
              - **中文**（默认）：`feat(auth): 添加 OAuth2 登录和令牌验证`
              - **英文**：`feat(auth): add OAuth2 login and token validation`

              请选择语言，或直接回车使用默认中文。"
            - 用户选择后，后续所有 commit message 的简短描述和正文均使用该语言
            - 注意：类型（feat/fix 等）、范围（scope）和 BREAKING CHANGE 标记始终使用英文（这是约定式提交规范的硬性要求）
            - 语言选择仅影响冒号后面的描述部分
            - 中文描述规则：使用简洁的陈述句，结尾不加句号（如"添加用户认证功能"而非"添加了用户认证功能。"）
            - 英文描述规则：使用祈使句（如 "add" 而非 "added"），结尾不加句号

        - 对所有变更文件执行分组判断（按以下优先级逐层归类）：

        分组判断规则（必须执行，不可跳过）：

            第一层：分离基础设施变更
                先将与具体业务无关的"项目基础设施"文件独立出来，单独成组：
                - .gitignore、.editorconfig、.eslintrc 等项目配置文件
                - CI/CD 配置（.github/workflows/、Jenkinsfile 等）
                - 构建工具配置（pom.xml 依赖升级、package.json 依赖升级等）
                - IDE 配置（.vscode/、.idea/ 等）
                这些文件无论与哪个 Story 同时出现，都必须拆出来作为独立的 chore/build/ci 提交

            第二层：按 Story/业务需求分组（最高优先级）
                对剩余的业务相关文件，判断是否涉及多个 Story：
                - 识别依据：文件路径中的模块归属、变更内容中的 Story ID 引用、代码注释中的需求关联、同一功能域的文件聚集
                - 同一 Story 产生的所有文件归为一组，包括：
                  · 功能代码（src/、lib/ 下的业务实现）
                  · 该 Story 的 CR 审查文档（如 docs/cr/、_bmad-output/ 等）
                  · 因该 Story 而连带修改的全局文档（如 CLAUDE.md、README.md、CHANGELOG.md 中与该 Story 相关的段落变更）
                  · 该 Story 的测试文件
                - 如果涉及多个 Story，每个 Story 必须独立成组，禁止跨 Story 合并

            第三层：组内提交类型判断
                对每个分组（每个 Story 组或基础设施组），确定 Conventional Commits 类型：
                - 新增功能为主 → feat(<scope>)
                - 修复 Bug 为主 → fix(<scope>)
                - 重构为主 → refactor(<scope>)
                - 纯文档 → docs(<scope>)
                - 基础设施/配置 → chore/build/ci
                - 如果同一 Story 组内既有 feat 又有 docs，合并为一次 feat 提交（因为文档是该功能的一部分）
                - 如果同一 Story 组内既有 feat 又有 fix（修的是本次新增功能的 bug），合并为一次 feat 提交

            第四层：单 Story 内的拆分（仅当单个 Story 变更量极大时）
                如果单个 Story 组内文件数超过 15 个或 diff 行数超过 500 行，考虑按子模块拆分为 2-3 次提交，但保持 scope 一致

        分组结果示例：

            示例 1：单 Story + 基础设施混合
            ─────────────────────────────
            变更文件：
              src/auth/oauth2.java          ← Story-1001 功能代码
              src/auth/token-validator.java  ← Story-1001 功能代码
              test/auth/oauth2-test.java    ← Story-1001 测试
              docs/cr/story-1001-cr-r1.md   ← Story-1001 CR 文档
              CLAUDE.md                      ← Story-1001 连带全局文档更新
              .gitignore                     ← 项目配置（与 Story 无关）

            分组结果：
              Commit 1: chore: 更新 .gitignore 规则
                └─ .gitignore
              Commit 2: feat(auth): 添加 OAuth2 登录和令牌验证 (Story-1001)
                └─ src/auth/oauth2.java, src/auth/token-validator.java,
                   test/auth/oauth2-test.java, docs/cr/story-1001-cr-r1.md, CLAUDE.md

            示例 2：多 Story 并存
            ─────────────────────
            变更文件：
              src/auth/sso.java             ← Story-1001
              src/auth/sso-config.java      ← Story-1001
              docs/cr/story-1001-cr-r1.md   ← Story-1001 CR
              src/payment/refund.java        ← Story-1002
              src/payment/refund-policy.java ← Story-1002
              test/payment/refund-test.java  ← Story-1002
              .editorconfig                  ← 项目配置

            分组结果：
              Commit 1: chore: 更新 .editorconfig 格式化规则
                └─ .editorconfig
              Commit 2: feat(auth): 实现 SSO 单点登录认证 (Story-1001)
                └─ src/auth/sso.java, src/auth/sso-config.java,
                   docs/cr/story-1001-cr-r1.md
              Commit 3: feat(payment): 添加退款处理功能 (Story-1002)
                └─ src/payment/refund.java, src/payment/refund-policy.java,
                   test/payment/refund-test.java

        单次提交的情况：如果所有变更文件属于同一 Story + 无基础设施变更，生成单条 commit message 即可，无需拆分

        - 为每个分组生成独立的 Commit Message（参照 `references/conventional-commits-spec.md` 中的类型定义）
        - 从变更文件路径推断每组的 scope（如文件在 src/api/ 下则 scope 为 api）
        - 撰写简短描述：根据用户选择的语言（默认中文）撰写，中文用简洁陈述句、英文用祈使句，结尾均不加句号，精炼概括变更意图
        - 如果某组存在破坏性变更，在类型后添加 `!` 标记或在脚注中添加 `BREAKING CHANGE:`
        - 生成数据：分组提交计划（每组包含：commit message + 文件清单）

    Step 3：展示提交计划并确认
        - 如果只有 1 个分组：直接展示单条 Commit Message 和文件清单
        - 如果有多个分组：以编号列表展示完整提交计划
          格式：
            "📋 检测到 N 组不同类型的变更，建议分 N 次提交：

            **Commit 1/N**：`<type>(<scope>): <description>`
              文件：<file1>, <file2>

            **Commit 2/N**：`<type>(<scope>): <description>`
              文件：<file3>

            ..."
        - 等待用户确认或修改（用户可调整分组、合并/拆分、修改 message）
        - 如果用户要求调整，根据反馈修改后重新展示

    Step 4：执行提交（按分组顺序逐个提交）
        - 接收确认：用户同意提交计划
        - 按分组顺序依次执行（每组一次独立提交）：
            a. 执行 `git add <该组的具体文件名>`（逐个文件添加，绝不使用 `git add -A`）
            b. 执行 `git commit -m` 提交（commit message 通过 HEREDOC 传递以确保格式正确）
            c. 如果当前提交失败（如 pre-commit hook 报错）：停止后续提交，显示错误信息，等待用户修复
        - 所有分组提交完成后：
            a. 执行 `git log --oneline -N` 展示本次所有新增的提交记录（N = 分组数量）
            b. 执行 `git status` 验证工作区状态
            c. 完成后返回："已完成 N 次提交到本地 Git 仓库"，展示每次提交的 hash 和摘要
            d. 进入 Step 5 判断是否需要推送

    Step 5：推送判断与执行（条件触发）
        判断是否需要推送——按以下优先级决策：

        意图识别：
            - 用户原始请求中包含 push 意图关键词 → 需要推送
              关键词：'gcp'、'push'、'推送'、'推到远程'、'同步远程'、'提交并推送'、'commit and push'
            - 用户原始请求中仅包含 commit 意图 → 不推送，直接结束
              关键词：'gc'、'commit'、'提交代码'（不含 push 相关词）
            - 无法判断 → 提交完成后询问用户："已提交到本地，是否需要推送到远程仓库？"

        如果需要推送，执行以下前置检查链（任一环节不通过则终止推送）：

        检查 1：远程仓库是否存在
            - 执行 `git remote -v`
            - 如果输出为空（纯本地仓库）→ 告知用户"当前仓库无远程配置，跳过推送"，正常结束
            - 如果有远程仓库 → 记录 remote 名称（通常为 origin），继续下一步

        检查 2：当前分支的远程跟踪状态
            - 执行 `git rev-parse --abbrev-ref --symbolic-full-name @{upstream} 2>/dev/null`
            - 如果有上游分支 → 直接 `git push`
            - 如果没有上游分支 → 使用 `git push -u origin <当前分支名>` 建立跟踪关系

        检查 3：目标分支保护
            - 获取当前分支名：`git branch --show-current`
            - 如果当前分支为 main 或 master → 发出警告："即将推送到受保护分支 <branch>，确认继续？"，等待用户确认
            - 其他分支 → 直接推送

        执行推送：
            - 所有检查通过后执行 `git push`（或 `git push -u origin <branch>`）
            - 推送成功 → 返回："已推送到远程仓库 <remote>/<branch>"
            - 推送失败（如远程有新提交导致冲突）→ 显示错误信息，建议用户先 `git pull --rebase` 后重试

[注意事项]
    - 绝不使用 `git add -A` 或 `git add .`，只添加用户明确相关的文件
    - 绝不使用 `--no-verify` 跳过 pre-commit hooks
    - 绝不使用 `--amend` 修改历史提交，除非用户明确要求
    - 绝不使用 `git push --force`，推送失败时建议用户手动处理冲突
    - **推送默认关闭**：仅当用户明确表达 push 意图（含 'gcp'、'push'、'推送' 等关键词）时才执行推送；用户只说"提交"则仅 commit
    - **推送前必须通过三项检查**：远程仓库存在 → 分支跟踪正常 → 目标分支非 main/master（或用户已确认）
    - 发现敏感文件（.env、credentials、*.key、*.pem）时必须警告用户
    - 提交类型必须严格匹配约定式提交规范的类型列表，不可自创类型
    - **描述语言默认中文**：commit message 的简短描述默认使用中文，用户可在 Step 2 语言选择环节切换为英文；类型（feat/fix 等）、范围（scope）和 BREAKING CHANGE 标记始终使用英文
    - 中文描述使用简洁陈述句（如"添加用户认证功能"），英文描述使用祈使句（如 "add user authentication"），结尾均不加句号
    - **多变更必须分组提交**：当变更涉及多个 Story 或混合业务与基础设施变更时，必须拆分为多次提交，禁止跨 Story 合并
    - **Story 优先原则**：同一 Story 产生的代码、测试、CR 文档、连带全局文档变更归为一次提交；不同 Story 之间必须拆分
    - 分批提交顺序：基础设施（chore/build/ci）→ 各 Story 业务提交（按 Story ID 升序）
    - 某次提交失败时立即停止后续提交，等待用户处理，不跳过继续
    - commit message 通过 HEREDOC 传递，确保多行格式正确
