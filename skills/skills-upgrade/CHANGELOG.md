# Changelog

本文件记录 `skills-upgrade` 技能的版本变更历史。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本号遵循 [Semantic Versioning](https://semver.org/)。

## [2.1.0] - 2026-05-25

### Added

- 新增 `SKILL.en.md` mirror 升级规则：版本号、英文章节、引用路径和缺失 mirror 补建需要与中文 SKILL.md 同步处理。
- 新增多安装根同步规则：检测并同步 `.claude/skills/`、`.agents/skills/`、`.codex/skills/` 中实际存在的副本。
- 新增 `skill-tooling` catalog，用于归类 Skill 创建、检查、升级工具链。

### Changed

- 版本升级范围从 SKILL.md / CHANGELOG.md 扩展为 SKILL.md / SKILL.en.md / CHANGELOG.md。
- 同步策略从固定 forge 与 `.claude/skills/` 双副本调整为 forge 与实际存在安装副本的多副本同步。

## [2.0.0] - 2026-04-08

### Changed

- Skill 更名：`skill-upgrade` → `skills-upgrade`，与项目命名规范（skills-creator 等）保持一致
- YAML `name` 字段由 `skill-upgrade` 改为 `skills-upgrade`
- description 中新增触发词 `'skills-upgrade'`，同时保留旧触发词（`'skill upgrade'`、`'upgrade skill'` 等）向后兼容
- 正文中对 `skill-lint` 的引用更新为 `skills-lint`

## [1.0.0] - 2026-03-25

### 初始版本

- 变更分析：读取用户描述或 git diff，识别变更类型并分类（Added/Changed/Fixed/Removed）
- 版本号自动判断：根据语义化版本决策树推荐 MAJOR/MINOR/PATCH
- SKILL.md 版本更新：修改 YAML frontmatter 中 metadata.version
- CHANGELOG 生成：以时间倒序插入新版本记录，按分类组织变更条目
- 双副本同步：检测 forge/ 和 .claude/skills/ 副本，逐文件同步确保一致
- 质量闭环：升级完成后建议运行 skill-lint 验证

### 已知问题

- 暂无

---

版本变更类型说明：
- **Added**：新增功能
- **Changed**：已有功能的变更
- **Fixed**：缺陷修复
- **Removed**：移除的功能

后续版本更新时，在最新版本记录之前插入新版本记录，并同步更新 SKILL.md 中的 metadata.version。
已知问题修复后，用删除线标注并注明修复版本，如：
- ~~**问题描述**~~ → 已在 vX.Y.Z 修复
