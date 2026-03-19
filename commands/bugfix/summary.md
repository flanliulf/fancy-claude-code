根据问题的排查分析过程、解决方案思路以及修复解决过程，总结问题原因和解决方案，作为后续开发和排查错误的参考资料。

你需要：

1. 保存详细内容到 $1 目录下（默认 docs 目录下）的**问题跟踪文档**中， 文档的命名格式为 {storyId}-bugfix-{bugEnglishTitle}.md （如果没有则创建）；
2. 将"问题描述"、"核心原因"、"解决方案"、"经验总结"（如果有），追加到 $2 目录下（默认 docs 目录下）的**问题汇总文档** bugfix-index.md 文件中（如果没有则创建）；
3. **注意：文档的内容必须遵循以下格式**：

---

**问题跟踪文档**格式如下：

# Story-{storyId} Bugfix: {bug中文标题}

## 问题描述

{根据用户的问题描述，结合问题分析，重新整理成有序的、清晰的问题现象描述}

## 根因分析

### 布局结构
{描述问题原因涉及的代码组件、类、方法等层级结构}

### 核心原因

{详细阐述导致问题产生的根本原因，以及分析结果}

### {提出产生问题现象的相关问题}

## 解决方案

{按照优先级，给出解决问题的方案，以及解决方案的执行步骤}

### 1. {步骤一}

{关键代码}

**作用**: {该步骤的作用描述}

### 2. {步骤二}

{关键代码}

**作用**: {该步骤的作用描述}

### 3. {其余步骤（如果有）}

## 修改文件清单

{以 markdown 表格形式，列出修复该问题涉及到的所有需要更新的文件清单}

示例如下：

| 文件 | 行号 | 修改内容 |
|------|------|---------|
| `app/page.tsx` | 160 | `flex-1` → `flex-1 min-h-0` |
| `components/layout/split-view.tsx` | 47 | `h-full` → `h-full overflow-hidden` |
| `components/layout/header.tsx` | 5 | `h-14` → `h-14 shrink-0` |

## 经验总结（如果有）

{总结该问题的通用原因或者问题类型、避免方式或者最佳实践、， 供后续编码或者排查参考}

示例如下：
### Flex 纵向布局滚动的最佳实践

在 Tailwind + Flex 纵向布局中，要实现"固定头部 + 剩余区域内部滚动"：

```tsx
<div className="flex flex-col h-screen">
  <header className="h-14 shrink-0">固定头部</header>
  <div className="flex-1 min-h-0 overflow-hidden">
    <div className="h-full overflow-y-auto">
      可滚动内容区
    </div>
  </div>
</div>
```

关键点：
1. **外层容器**: `h-screen` 锁定视口高度
2. **固定元素**: `shrink-0` 防止被压缩
3. **弹性区域**: `flex-1 min-h-0` 占据剩余空间且允许收缩
4. **滚动容器**: `overflow-y-auto` 或 `overflow-hidden` 控制溢出

### {提出总结的核心问题}

示例如下：

Flexbox 规范中，flex 子元素的 `min-height` 默认值是 `auto`（内容高度），而不是 `0`。这意味着：
- 子元素不会收缩到小于其内容高度
- 即使设置了 `flex-1`，内容溢出时仍会撑开父容器
- 必须显式设置 `min-h-0` 来覆盖这个默认行为

## 参考资料

{解决问题所依赖的参考资料，包括但不限于官方文档，API 文档等}

示例如下：
- [CSS Flexbox - min-height: auto](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_flexible_box_layout/Basic_concepts_of_flexbox#the_min-height_property)
- [Tailwind CSS - Min-Height](https://tailwindcss.com/docs/min-height)

---

**问题汇总文档** bugfix-index.md 格式如下：

# Bugfix 汇总索引

本文档记录项目开发过程中遇到的所有问题及其解决方案，按 Epic 和 Story 组织。

## Epic 1

### Story 1

- {story-id}-bugfix-{bugEnglishTitle}：
    - **问题描述**：{问题描述一到两句话简要描述}
    - **核心原因**：{核心原因一到两句话简要描述}
    - **解决方案**：{解决方案一到两句话简要描述}
    - **经验总结**：{经验总结一到两句话简要描述}
    - **详细文档**：{story-id}-bugfix-{bugEnglishTitle}.md 文档所在路径
...

## Story 2
...

