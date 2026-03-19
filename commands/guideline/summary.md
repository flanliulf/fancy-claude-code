深入分析该问题出现的本质原因, 然后深度思考该问题的出现是否既有代表性（容易重复出现），如果是，请总结为 200 字以内的 AI 编程规约/避坑指令, 保存到 CLAUDE.md 的 "## AI 编程规约" 章节.

示例如下：

---

## AI 编程规约

> 从代码审查中提炼的避坑指令，持续迭代更新。

### 1. 嵌套结构校验原则

**来源**: Story 4-4 Code Review (AC-4.4.1)

**问题**: 对外部输入的数组/对象，只检查容器类型而遗漏内部结构校验。

**规约**:
- 数组 → 验证非空 + 遍历每个元素
- 对象 → 验证必需字段的类型和值约束
- 与规格文档逐字段对照，防止遗漏

**反模式**:
```typescript
// ❌ 只检查是数组，不检查元素结构
if (!Array.isArray(parts)) return error
// 直接使用 parts...
```

**正模式**:
```typescript
// ✅ 递归验证到叶子节点
if (!Array.isArray(parts)) return error
if (parts.length === 0) return error
for (const part of parts) {
  if (part.type !== 'text') return error
  if (typeof part.text !== 'string') return error
}
```

注意：
- 编号结构 (### 1., ### 2....) 便于后续迭代追加
- 每条规约包含：来源、问题、规约、反模式、正模式
- 代码示例使用 TypeScript 格式

后续代码审查发现的新规约可按相同格式追加 ### 2. xxx 等。