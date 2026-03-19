# Fancy Claude Code

个人定制的 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 配置集合，包含自定义斜杠命令、技能、代理、状态栏脚本和核心行为规则。

## 状态栏

自定义状态栏脚本，实时展示模型、目录和上下文用量：

```
🤖 claude-sonnet-4.6 | 📁 .claude | ⚡ 13.2% · 26.4k tokens
```

- 从 `current_usage` 自行计算上下文百分比，修复了 1M 模型下 `used_percentage` 卡在 80% 不更新的问题
- 百分比保留一位小数，同时显示已用令牌数（k/M 格式）
- 颜色编码：绿色 (<50%)、黄色 (50-80%)、红色 (>80%)
- 在 Git 仓库内自动显示分支名

## 斜杠命令

| 命令 | 说明 |
|---|---|
| `/git commit` | 约定式提交（Conventional Commit）|
| `/git gc` | 总结改动并按约定式提交规范提交到本地 |
| `/git gcp` | 同上，提交后推送到远程 |
| `/git new-feature` | 创建并切换到 `feature/` 分支 |
| `/bugfix debug` | 根据问题描述分析可能的原因和解决方案 |
| `/bugfix troubleshooting` | 根据报错信息分析根因 |
| `/bugfix summary` | 总结排查过程为参考资料 |
| `/codebase analyze-codebase-java-ddd` | 全面分析 Java DDD 微服务代码库 |
| `/codebase analyze-codebase-java-mvc` | 全面分析 Java MVC 微服务代码库 |
| `/codebase project-analyst` | 生成项目知识库 |
| `/codebase security-audit` | 安全审计 |
| `/dev persona` | 启用资深技术合伙人角色 |
| `/dev tech-decision` | 记录技术决策 |
| `/api apidoc-fetch` | 抓取 API 文档 |
| `/review implement-review` | 审查代码实现 |
| `/prompt-optimize` | 优化提示词（先展示再执行）|
| `/guideline summary` | 将问题总结为 AI 编程规约 |
| `/gen translate-skill-zh` | 将 Skill 翻译为中文版本 |
| `/go` | 按推荐方案执行 |

## 技能

| 技能 | 说明 |
|---|---|
| `java-spring-boot-zh` | Spring Boot 应用开发（REST API、Security、Data、Actuator）|
| `java-jpa-hibernate-zh` | JPA/Hibernate 实体设计、查询、事务、性能优化 |
| `java-testing-zh` | JUnit 5、Mockito、集成测试、TDD 模式 |
| `spring-boot-patterns-zh` | Spring Boot 架构模式、分层服务、缓存、异步处理 |
| `architecture-decision-records-zh` | 架构决策记录（ADR）最佳实践 |
| `architecture-patterns-zh` | Clean Architecture、Hexagonal、DDD 实现 |
| `iosdev-cn` | iOS 开发、构建、签名、App Store 上架（中国区）|
| `gitlab-fork-workflow` | GitLab Fork 工作流与提交规范 |
| `claudeforge-skill` | CLAUDE.md 文件分析、生成与增强 |

## 代理

内置 20+ 专用代理配置，覆盖：

- **分析**：API 文档、代码库分析、数据分析、模式检测
- **规划**：依赖映射、Epic 优化、需求分析、技术决策、趋势洞察、用户旅程、用户研究
- **审查**：文档审查、技术评估、测试覆盖率分析
- **其他**：棕地项目分析、CLAUDE.md 维护、Gemini 分析、提示词优化

## 安装

```bash
# 克隆到 ~/.claude
git clone git@github.com:flanliulf/fancy-claude-code.git ~/.claude

# 复制配置模板并填入你的 API 信息
cp ~/.claude/settings.json.example ~/.claude/settings.json
# 编辑 settings.json，填入 ANTHROPIC_AUTH_TOKEN 和 ANTHROPIC_BASE_URL

# 确保状态栏脚本可执行
chmod +x ~/.claude/scripts/statusline-command.sh
```

依赖：需要安装 [`jq`](https://jqlang.github.io/jq/) 用于状态栏脚本的 JSON 解析。

```bash
brew install jq  # macOS
```

## 目录结构

```
~/.claude/
├── CLAUDE.md              # 核心行为规则
├── settings.json.example  # 配置模板（不含密钥）
├── commands/              # 自定义斜杠命令
│   ├── git/               #   Git 工作流
│   ├── bugfix/            #   问题排查
│   ├── codebase/          #   代码库分析
│   ├── dev/               #   开发辅助
│   ├── api/               #   API 文档
│   ├── review/            #   代码审查
│   ├── gen/               #   生成工具
│   └── guideline/         #   编程规约
├── scripts/               # 状态栏等脚本
├── skills/                # 自定义技能
│   ├── java-*-zh/         #   Java 技术栈（中文）
│   ├── architecture-*-zh/ #   架构模式（中文）
│   ├── iosdev-cn/         #   iOS 开发（中国区）
│   └── ...
└── agents/                # 自定义代理配置
```

## 许可

MIT
