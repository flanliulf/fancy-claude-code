---
name: skills-upgrade
description: "Manage Skill version iteration by analyzing changes, determining semantic version bumps, updating metadata.version in SKILL.md and SKILL.en.md, and maintaining CHANGELOG.md records. Use when user mentions 'skills-upgrade', 'upgrade skill', 'bump version', 'update version', 'skill upgrade', 'version bump', 'new version', 'release version', '升级版本', '更新版本号', '版本升级', 'Skill 升级', '发布新版本', '更新 CHANGELOG', '升级 Skill 版本', or wants to record changes after modifying a Skill. Capable of semantic versioning analysis (MAJOR/MINOR/PATCH), CHANGELOG entry generation with categorized changes, multi-copy synchronization between forge/ and installed skill roots, and post-upgrade lint recommendation."
allowed-tools: Read, Write, Grep, Glob
metadata:
  version: "2.1.0"
  author: "fancyliu"
  catalog: "skill-tooling"
---

[Overview（技能说明）]
    管理 Skill 的版本迭代：分析变更内容，自动判断语义化版本号升级类型（MAJOR/MINOR/PATCH），同步更新 SKILL.md 与 SKILL.en.md 中的 metadata.version，在 CHANGELOG.md 中插入结构化变更记录，并同步 forge/ 与实际存在的安装副本。详细版本规则参见 `references/semver-guide.md`。

[Core Capabilities（核心能力）]
    - **变更分析**：读取用户描述或 git diff，识别变更涉及的文件和内容，将变更分类为 Added/Changed/Fixed/Removed
    - **版本号自动判断**：根据 `references/semver-guide.md` 中的语义化版本规则，推荐 MAJOR/MINOR/PATCH 升级类型，展示推荐理由供用户确认
    - **双语入口版本更新**：同步修改 SKILL.md 与 SKILL.en.md YAML frontmatter 中的 metadata.version 为新版本号
    - **CHANGELOG 生成**：在 CHANGELOG.md 中以时间倒序插入新版本记录，按 Added/Changed/Fixed/Removed 分类组织变更条目
    - **多副本同步**：检测 Skill 在 forge/、.claude/skills/、.agents/skills/、.codex/skills/ 中的所有副本，逐文件同步确保一致
    - **Mirror 完整性维护**：确保 SKILL.en.md 是中文 SKILL.md 的英文 mirror，不遗漏新能力、步骤、限制或引用路径
    - **质量闭环**：升级完成后建议运行 skills-lint 验证合规性

[Workflow（执行流程）]
    本 Skill 采用顺序工作流模式。

    Step 1：定位目标 Skill
        - 接收 Skill 名称或目录路径
        - 在 `forge/` 中查找源码副本
        - 在 `.claude/skills/`、`.agents/skills/`、`.codex/skills/` 中查找实际存在的部署副本
        - 读取当前 SKILL.md，提取 metadata.version（如 "1.0.0"）
        - 读取当前 SKILL.en.md（如存在），提取 metadata.version
        - 读取当前 CHANGELOG.md（如存在），提取最新版本号
        - 如果 SKILL.md、SKILL.en.md、CHANGELOG.md 版本不一致，先警告用户

    Step 2：分析变更内容
        通过以下方式之一收集变更信息：
        - **方式 A**：用户直接描述变更内容（最常见）
        - **方式 B**：用户提供 git diff 输出或 commit message
        - **方式 C**：用户指定"对比 CHANGELOG 最后记录以来的所有改动"

        将变更分类为：
        - **Added**：新增的功能、检查项、文件、触发词
        - **Changed**：已有功能的修改、规则的调整、流程的优化
        - **Fixed**：缺陷修复、拼写更正、路径修正
        - **Removed**：移除的功能、废弃的文件

    Step 3：确定版本号
        根据 `references/semver-guide.md` 中的决策树判断：

        ```
        变更是否移除已有功能或改变触发时机？
        ├── 是 → MAJOR（X.0.0）
        └── 否 → 变更是否新增功能或显著改进？
            ├── 是 → MINOR（x.Y.0）
            └── 否 → PATCH（x.y.Z）
        ```

        向用户展示：
        "📦 版本升级建议：
        当前版本：<current_version>
        推荐新版本：<new_version>（<MAJOR/MINOR/PATCH>）
        理由：<具体理由>

        确认升级？"

        等待用户确认后继续。用户可以指定不同的版本号。

    Step 4：更新 SKILL.md
        - 定位 YAML frontmatter 中的 `metadata.version` 字段
        - 将版本号更新为新版本
        - 如果 `metadata.version` 不存在，在 `metadata:` 下添加
        - 保留 metadata.author 与 metadata.catalog，不因版本升级改写作者或 catalog

    Step 5：更新 SKILL.en.md
        - 如果 SKILL.en.md 存在，同步更新 YAML frontmatter 中的 `metadata.version`
        - 对比本次变更涉及的 SKILL.md 内容，更新 SKILL.en.md 对应英文章节，保持章节、能力清单、执行步骤、注意事项和引用路径一一对应
        - 如果 SKILL.en.md 缺失，按 `skills-creator` 的 SKILL.en.md mirror 规则补建，并与 SKILL.md 的 YAML frontmatter 对齐
        - 不允许只更新 SKILL.en.md 而不更新 SKILL.md；中文 SKILL.md 是 canonical 来源

    Step 6：更新 CHANGELOG.md
        - 如果 CHANGELOG.md 不存在，按模板创建（参见 `references/semver-guide.md` 中的格式规范）
        - 在最新版本记录之前插入新版本块：
          ```
          ## [X.Y.Z] - YYYY-MM-DD

          ### Added
          - <新增项>

          ### Changed
          - <变更项>
          ```
        - 只列出有内容的分类
        - 如果旧版本有已知问题被本次修复，添加删除线标注

    Step 7：同步副本
        - 检测是否存在 forge/ 中的源码副本，以及 `.claude/skills/`、`.agents/skills/`、`.codex/skills/` 中的安装副本
        - 以用户明确修改的副本为来源；如果用户只给 Skill 名称，默认以 forge/ 源码副本为来源
        - 同步文件至少包括 SKILL.md、SKILL.en.md、CHANGELOG.md，以及本次变更涉及的 references/、scripts/、assets/ 文件
        - 对不存在的安装根只记录为"未发现"，不得凭空创建新的安装副本
        - 逐个副本同步，每个副本同步后确认

    Step 8：完成确认
        展示版本变更摘要：
        "✅ 版本升级完成！

        📦 <skill-name>：<old_version> → <new_version>

        📝 更新的文件：
        - forge/.../<name>/SKILL.md（metadata.version）
        - forge/.../<name>/SKILL.en.md（mirror 同步）
        - forge/.../<name>/CHANGELOG.md（新增 [<new_version>]）
        - <installed-root>/<name>/...（已同步，按实际存在副本列出）

        🔍 建议运行 skills-lint 验证合规性。"

    错误处理：
        - CHANGELOG.md 不存在：自动创建并告知用户
        - metadata.version 字段不存在：添加 metadata 块并告知用户
        - SKILL.en.md 缺失：补建英文 mirror，并在 CHANGELOG.md 中记录 Added
        - 版本号格式不合法（如 "v1.0" 或 "1.0"）：提示正确格式 "X.Y.Z"
        - forge/ 副本不存在：标记为信息提示，不阻塞升级流程
        - 用户未描述变更内容：引导用户至少提供一句变更说明

[Notes（注意事项）]
    - 版本号变更必须经用户确认，不能自动执行（即使用户说"直接升级"，仍需展示变更摘要）
    - CHANGELOG 条目必须按 Added/Changed/Fixed/Removed 分类，不使用其他分类
    - 日期格式统一为 YYYY-MM-DD
    - 与 skills-lint 配合：升级后建议运行 lint 验证
    - 与 skills-creator 配合：新建 Skill 始终从 1.0.0 开始，后续修改通过本 Skill 管理版本
    - SKILL.md 是中文 canonical 入口，章节标题使用 English（中文）形式；SKILL.en.md 是英文 mirror，不能成为功能事实来源
    - 同步操作按副本逐个执行，每个副本单独确认
    - 不存在的安装根（如没有 `.codex/skills/`）只报告未发现，不创建空副本
    - 如果用户只想更新 CHANGELOG 不改版本号，应拒绝并解释"版本号和 CHANGELOG 必须同步"
