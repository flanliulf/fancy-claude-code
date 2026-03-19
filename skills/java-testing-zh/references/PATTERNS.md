# Java 测试模式

## 设计模式

### 模式 1：输入校验

处理前始终校验输入：

```python
def validate_input(data):
    if data is None:
        raise ValueError("Data cannot be None")
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")
    return True
```

### 模式 2：错误处理

使用一致的错误处理方式：

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    handle_error(e)
except Exception as e:
    logger.exception("Unexpected error")
    raise
```

### 模式 3：配置加载

加载并校验配置：

```python
import yaml

def load_config(config_path):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    validate_config(config)
    return config
```

## 应避免的反模式

### ❌ 不要：吞掉异常

```python
# 错误示范
try:
    do_something()
except:
    pass
```

### ✅ 应该：显式处理

```python
# 正确示范
try:
    do_something()
except SpecificError as e:
    logger.warning(f"Expected error: {e}")
    return default_value
```

## 分类特定模式：测试

### 推荐做法

1. 从最简单的实现开始
2. 仅在需要时增加复杂度
3. 测试每次新增的内容
4. 记录决策过程

### 常见集成点

- 配置：`assets/config.yaml`
- 校验：`scripts/validate.py`
- 文档：`references/GUIDE.md`

---

*java-testing 技能的模式库*
