---
name: java-jpa-hibernate
description: 精通 JPA/Hibernate - 实体设计、查询、事务、性能优化
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 06-java-persistence
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# 参数校验
parameters:
  database:
    type: string
    enum: [postgresql, mysql, oracle, h2]
    description: 目标数据库
  focus:
    type: string
    enum: [entities, queries, transactions, caching]
    description: 主题聚焦方向
---

# Java JPA Hibernate 技能

掌握 JPA 和 Hibernate 的数据持久化，构建生产级应用。

## 概述

本技能涵盖 JPA 实体设计、Hibernate 优化、Spring Data Repository、查询策略和缓存。重点关注防止 N+1 查询问题和构建高性能持久层。

## 何时使用此技能

当你需要：
- 设计带有关联关系的 JPA 实体
- 优化数据库查询
- 配置 Hibernate 以提升性能
- 实施缓存策略
- 调试持久化问题

## 涵盖的主题

### 实体设计
- 实体映射注解
- 关联类型（1:1、1:N、N:M）
- 继承策略
- 生命周期回调
- 审计

### 查询优化
- N+1 问题防范
- JOIN FETCH vs EntityGraph
- 批量抓取
- 投影与 DTO

### 事务
- @Transactional 配置
- 传播行为与隔离级别
- 乐观锁 vs 悲观锁
- 死锁预防

### 缓存
- 一级缓存与二级缓存
- 查询缓存
- 缓存失效
- Redis 集成

## 快速参考

```java
// 带关联关系的实体
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "customer_id", nullable = false)
    private Customer customer;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    @BatchSize(size = 20)
    private List<OrderItem> items = new ArrayList<>();

    @Version
    private Long version;

    // 双向关联辅助方法
    public void addItem(OrderItem item) {
        items.add(item);
        item.setOrder(this);
    }
}

// 审计基类
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class Auditable {
    @CreatedDate
    @Column(updatable = false)
    private Instant createdAt;

    @LastModifiedDate
    private Instant updatedAt;
}

// 带查询优化的 Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // 使用 JOIN FETCH 防止 N+1
    @Query("SELECT DISTINCT o FROM Order o JOIN FETCH o.items WHERE o.status = :status")
    List<Order> findByStatusWithItems(@Param("status") Status status);

    // EntityGraph 替代方案
    @EntityGraph(attributePaths = {"items", "customer"})
    Optional<Order> findById(Long id);

    // DTO 投影
    @Query("SELECT new com.example.OrderSummary(o.id, o.status, c.name) " +
           "FROM Order o JOIN o.customer c WHERE o.id = :id")
    Optional<OrderSummary> findSummaryById(@Param("id") Long id);
}
```

## N+1 防范策略

| 策略 | 使用场景 | 示例 |
|------|----------|------|
| JOIN FETCH | 总是需要关联数据时 | `JOIN FETCH o.items` |
| EntityGraph | 动态抓取时 | `@EntityGraph(attributePaths)` |
| @BatchSize | 集合访问时 | `@BatchSize(size = 20)` |
| DTO 投影 | 只读查询时 | `new OrderSummary(...)` |

## Hibernate 配置

```yaml
spring:
  jpa:
    open-in-view: false  # 关键配置！
    properties:
      hibernate:
        jdbc.batch_size: 50
        order_inserts: true
        order_updates: true
        default_batch_fetch_size: 20
        generate_statistics: ${HIBERNATE_STATS:false}

  datasource:
    hikari:
      maximum-pool-size: 20
      minimum-idle: 5
      leak-detection-threshold: 60000
```

## 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| N+1 查询 | 循环中延迟加载 | JOIN FETCH、EntityGraph |
| LazyInitException | Session 已关闭 | 使用 DTO 投影 |
| 查询缓慢 | 缺少索引 | EXPLAIN ANALYZE |
| 连接泄漏 | 缺少 @Transactional | 添加注解 |

### 调试属性
```properties
spring.jpa.show-sql=true
logging.level.org.hibernate.SQL=DEBUG
logging.level.org.hibernate.orm.jdbc.bind=TRACE
hibernate.generate_statistics=true
```

### 调试清单
```
□ 启用 SQL 日志
□ 检查每个请求的查询次数
□ 验证抓取策略
□ 审查 @Transactional
□ 检查连接池
```

## 用法

```
Skill("java-jpa-hibernate")
```

## 相关技能
- `java-performance` - 查询优化
- `java-spring-boot` - Spring Data
