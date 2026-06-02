# 测试与迭代指南

## 概述
Skill 创建完成后，需要进行系统性的触发测试和迭代优化，确保 Skill 在正确的场景下被触发，且不会误触发。

## 触发测试

### 测试方法
准备三类测试输入各 3-5 个：

| 测试类别 | 说明 | 合格标准 |
|:--------|:-----|:---------|
| ✅ 明确相关 | 包含触发关键词的标准输入 | 触发率 100% |
| ✅ 同义替换 | 换种说法表达相同意图 | 触发率不低于 80% |
| ❌ 无关查询 | 验证不会误触发 | 误触发率约 0% |

**整体合格标准**：相关查询触发率不低于 90%，无关查询误触发率约 0%

### 测试输出模板
生成 Skill 后，向用户提供如下测试建议：

```
🧪 触发测试建议：
请依次测试以下三类输入：
1. ✅ 明确相关："<包含触发词的标准输入>"
2. ✅ 换种说法："<同义词/口语化的输入>"
3. ❌ 不相关："<无关问题，验证不会误触发>"
```

## 调试技巧

如果触发不理想，让用户直接问智能体：
> "你会在什么情况下使用 [Skill 名称] 这个技能？"

智能体会暴露它对触发条件的理解，便于定位 description 问题。

## 常见问题与对策

### 触发不足（该加载时没加载）
- **诊断**：description 太笼统或缺少用户常用口语
- **对策**：
  - 补充领域术语
  - 添加用户原话关键词
  - 补充文件类型后缀

### 过度触发（不相关时也加载）
- **诊断**：description 适用范围界定不清
- **对策 1**：添加负面触发词
  - 示例：`"Do NOT use for simple data exploration"`
- **对策 2**：提高具体化程度
  - 改前："处理文档"
  - 改后："处理 PDF 法律文档以进行合同审查"
- **对策 3**：澄清适用范围
  - 示例：`"专门用于在线支付工作流，不适用于一般财务查询"`

## 迭代优化流程

```
1. 用户反馈触发问题
       ↓
2. 分析属于"触发不足"还是"过度触发"
       ↓
3. 针对性修改 YAML description
       ↓
4. 重新测试验证
       ↓
5. 必要时调整 SKILL.md 正文中的执行流程
       ↓
6. 同步更新 SKILL.en.md mirror
       ↓
7. 更新 CHANGELOG.md 记录变更
```

### 优化 description 的检查清单
- [ ] 包含功能描述（What it does）
- [ ] 包含触发条件（When to use it）+ 关键词 + 文件类型
- [ ] 包含核心能力（Core capabilities）
- [ ] **触发关键词覆盖中英文双语**（中文正式用语 + 口语化表达 + 英文关键词）
- [ ] 不超过 1024 字符
- [ ] 无 XML 尖括号
- [ ] 关键词覆盖用户常用口语和同义词
- [ ] 有明确的适用边界（避免过度触发）

### 双语入口检查清单
- [ ] SKILL.md 与 SKILL.en.md 同时存在
- [ ] 两个文件的 YAML frontmatter 保持一致
- [ ] `metadata.version` 必填且与 CHANGELOG.md 最新版本一致
- [ ] `metadata.author` 必填且非空
- [ ] `metadata.catalog` 如存在，使用 kebab-case，并与路径及 mirror 一致
- [ ] 不包含未登记的 `metadata.*` 字段
- [ ] SKILL.md 章节标题使用 English（中文）形式，正文内容使用中文
- [ ] SKILL.en.md 是 SKILL.md 的英文 mirror，能力、步骤、限制、引用路径未漂移
- [ ] CHANGELOG.md 版本号与两个入口的 metadata.version 一致

### Workflow density 检查清单
- [ ] 已运行 `python3 forge/skill-tooling/skills-lint/scripts/check_skill_density.py <skill-dir>`
- [ ] 已记录 SKILL.md 与 SKILL.en.md 的 `body_chars`、`workflow_chars`、`workflow_ratio`
- [ ] 任一入口命中 `triggered_density_warning` 时，已抽取 `references/<skill-name>-workflow.md` 或等价 workflow reference
- [ ] 入口 Workflow 只保留阶段摘要、何时读取 reference、关键停止条件
- [ ] 两个入口引用同一个 workflow reference 路径

## 版本说明
- v1.3 (2026-05-26): 增加 metadata 字段契约检查
- v1.2 (2026-05-26): 增加 Workflow density gate 测试检查
- v1.1 (2026-05-25): 增加 SKILL.en.md mirror 迭代检查
- v1.0 (2026-03-25): 初始版本
