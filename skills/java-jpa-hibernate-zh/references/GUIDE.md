# Java JPA Hibernate 指南

## 概述

本指南为 custom-plugin-java 插件中的 **java-jpa-hibernate** 技能提供全面的文档。

## 分类：通用

## 快速开始

### 前置条件

- 熟悉通用概念
- 已搭建好开发环境
- 已安装并配置插件

### 基本用法

```bash
# 调用技能
claude "java-jpa-hibernate - [你的任务描述]"

# 示例
claude "java-jpa-hibernate - analyze the current implementation"
```

## 核心概念

### 关键原则

1. **一致性** - 遵循既定模式
2. **清晰性** - 编写可读、可维护的代码
3. **质量** - 部署前进行验证

### 最佳实践

- 始终校验输入数据
- 显式处理边界情况
- 记录你的决策
- 为关键路径编写测试

## 常见任务

### 任务 1：基本实现

```python
# 示例实现模式
def implement_java_jpa_hibernate(input_data):
    """
    实现 java-jpa-hibernate 功能。

    Args:
        input_data: 待处理的输入

    Returns:
        处理后的结果
    """
    # 校验输入
    if not input_data:
        raise ValueError("Input required")

    # 处理
    result = process(input_data)

    # 返回
    return result
```

### 任务 2：高级用法

对于高级场景，请考虑：

- 通过 `assets/config.yaml` 自定义配置
- 使用 `scripts/validate.py` 进行校验
- 与其他技能集成

## 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 技能未找到 | 未安装 | 运行插件同步 |
| 校验失败 | 无效配置 | 检查 config.yaml |
| 输出异常 | 缺少上下文 | 提供更多详细信息 |

## 相关资源

- SKILL.md - 技能规范
- config.yaml - 配置选项
- validate.py - 校验脚本

---

*最后更新：2025-12-30*
