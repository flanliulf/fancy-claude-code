---
name: architecture-decision-records
description: 编写和维护架构决策记录（ADR），遵循技术决策文档化的最佳实践。适用于记录重大技术决策、审查过往架构选择或建立决策流程。
---

# 架构决策记录

用于创建、维护和管理架构决策记录（ADR）的完整模式，捕获重大技术决策背后的上下文和理由。

## 何时使用此 Skill

- 做出重大架构决策
- 记录技术选型
- 记录设计中的权衡取舍
- 新成员入职了解历史决策
- 审查历史决策
- 建立决策流程

## 核心概念

### 1. 什么是 ADR？

一份架构决策记录包含：

- **上下文（Context）**：为什么需要做出决策
- **决策（Decision）**：我们决定了什么
- **后果（Consequences）**：决策带来的影响

### 2. 何时编写 ADR

| 需要编写 ADR               | 无需编写 ADR         |
| -------------------------- | ---------------------- |
| 引入新框架                  | 小版本升级             |
| 数据库技术选型              | Bug 修复              |
| API 设计模式               | 实现细节               |
| 安全架构                   | 日常维护               |
| 集成模式                   | 配置变更               |

### 3. ADR 生命周期

```
Proposed → Accepted → Deprecated → Superseded
              ↓
           Rejected
```

## 模板

### 模板 1：标准 ADR（MADR 格式）

```markdown
# ADR-0001: 使用 PostgreSQL 作为主数据库

## 状态

已采纳（Accepted）

## 上下文

我们需要为新的电商平台选择主数据库。系统需要处理：

- 约 10,000 个并发用户
- 包含层级分类的复杂产品目录
- 订单和支付的事务处理
- 产品全文搜索
- 门店定位的地理空间查询

团队有 MySQL、PostgreSQL 和 MongoDB 的使用经验。金融交易需要 ACID 合规。

## 决策驱动因素

- **必须具备 ACID 合规**以支持支付处理
- **必须支持复杂查询**以满足报表需求
- **应支持全文搜索**以降低基础设施复杂度
- **应具备良好的 JSON 支持**以适应灵活的产品属性
- **团队熟悉度**可缩短上手时间

## 备选方案

### 方案 1：PostgreSQL

- **优点**：ACID 合规、出色的 JSON 支持（JSONB）、内置全文搜索、
  PostGIS 支持地理空间查询、团队有使用经验
- **缺点**：复制配置比 MySQL 略复杂

### 方案 2：MySQL

- **优点**：团队非常熟悉、复制配置简单、社区庞大
- **缺点**：JSON 支持较弱、无内置全文搜索（需要额外部署
  Elasticsearch）、无地理空间扩展支持

### 方案 3：MongoDB

- **优点**：灵活的 Schema、原生 JSON、水平扩展
- **缺点**：多文档事务无 ACID 支持（做决策时），
  团队经验有限，需要严格的 Schema 设计规范

## 决策

我们将使用 **PostgreSQL 15** 作为主数据库。

## 理由

PostgreSQL 提供了最佳平衡：

1. **ACID 合规**是电商交易的必要条件
2. **内置能力**（全文搜索、JSONB、PostGIS）降低了基础设施复杂度
3. **团队熟悉** SQL 数据库，学习曲线较低
4. **成熟的生态系统**，拥有优秀的工具和社区支持

复制配置的额外复杂度，被减少额外服务（无需单独部署 Elasticsearch）
所带来的收益所抵消。

## 后果

### 正面

- 单一数据库处理事务、搜索和地理空间查询
- 降低运维复杂度（更少的服务需要管理）
- 为金融数据提供强一致性保证
- 团队可利用现有的 SQL 专业知识

### 负面

- 需要学习 PostgreSQL 特有功能（JSONB、全文搜索语法）
- 垂直扩展限制可能更早需要读副本
- 部分团队成员需要 PostgreSQL 专项培训

### 风险

- 全文搜索的扩展性可能不如专用搜索引擎
- 缓解措施：预留未来引入 Elasticsearch 的设计空间

## 实施说明

- 使用 JSONB 存储灵活的产品属性
- 使用 PgBouncer 实现连接池
- 配置流复制用于读副本
- 使用 pg_trgm 扩展实现模糊搜索

## 相关决策

- ADR-0002：缓存策略（Redis）- 与数据库选型互补
- ADR-0005：搜索架构 - 如需 Elasticsearch 可能取代本决策

## 参考资料

- [PostgreSQL JSON 文档](https://www.postgresql.org/docs/current/datatype-json.html)
- [PostgreSQL 全文搜索](https://www.postgresql.org/docs/current/textsearch.html)
- 内部文档：`/docs/benchmarks/database-comparison.md` 中的性能基准测试
```

### 模板 2：轻量级 ADR

```markdown
# ADR-0012: 前端开发采用 TypeScript

**状态**: 已采纳（Accepted）
**日期**: 2024-01-15
**决策者**: @alice, @bob, @charlie

## 上下文

我们的 React 代码库已增长到 50 多个组件，与 prop 类型不匹配和
undefined 错误相关的 Bug 报告日益增多。PropTypes 仅提供运行时检查。

## 决策

所有新的前端代码采用 TypeScript。现有代码逐步迁移。

## 后果

**正面**：在编译时捕获类型错误、更好的 IDE 支持、代码即文档。

**负面**：团队学习曲线、初期开发速度下降、构建复杂度增加。

**缓解措施**：开展 TypeScript 培训、通过 `allowJs: true` 支持渐进式采用。
```

### 模板 3：Y-Statement 格式

```markdown
# ADR-0015: API Gateway 选型

在**构建微服务架构**的背景下，
面对**集中式 API 管理、认证和限流的需求**，
我们决定采用 **Kong Gateway**，
而非 **AWS API Gateway 和自定义 Nginx 方案**，
以实现**厂商无关性、插件可扩展性以及团队对 Lua 的熟悉度**，
接受**需要自行管理 Kong 基础设施**这一代价。
```

### 模板 4：废弃决策 ADR

```markdown
# ADR-0020: 废弃 MongoDB，迁移至 PostgreSQL

## 状态

已采纳（取代 ADR-0003）

## 上下文

ADR-0003（2021 年）选择 MongoDB 存储用户资料，原因是需要 Schema 灵活性。
自那以后：

- MongoDB 的多文档事务在我们的场景下仍存在问题
- 我们的 Schema 已趋于稳定，很少变更
- 通过其他服务我们已积累了 PostgreSQL 经验
- 维护两种数据库增加了运维负担

## 决策

废弃 MongoDB，将用户资料迁移至 PostgreSQL。

## 迁移计划

1. **第一阶段**（第 1-2 周）：创建 PostgreSQL Schema，启用双写
2. **第二阶段**（第 3-4 周）：回填历史数据，验证一致性
3. **第三阶段**（第 5 周）：将读操作切换至 PostgreSQL，持续监控
4. **第四阶段**（第 6 周）：移除 MongoDB 写入，下线服务

## 后果

### 正面

- 单一数据库技术降低运维复杂度
- 用户数据具备 ACID 事务保证
- 团队可集中 PostgreSQL 专业能力

### 负面

- 迁移工作量（约 4 周）
- 迁移过程中的数据风险
- 失去部分 Schema 灵活性

## 经验教训

从 ADR-0003 的经验中总结：

- Schema 灵活性的收益被高估了
- 多数据库的运维成本被低估了
- 技术决策应考虑长期维护成本
```

### 模板 5：征求意见（RFC）风格

```markdown
# RFC-0025: 订单管理领域采用 Event Sourcing

## 摘要

提议在订单管理领域采用 Event Sourcing 模式，以提升审计能力、
支持时间维度查询并服务业务分析。

## 动机

当前面临的挑战：

1. 审计需求要求完整的订单历史
2. "某个时间点的订单状态是什么？"这类查询无法实现
3. 分析团队需要事件流用于实时仪表盘
4. 客服部门的订单状态重建依赖人工操作

## 详细设计

### Event Store
```

OrderCreated { orderId, customerId, items[], timestamp }
OrderItemAdded { orderId, item, timestamp }
OrderItemRemoved { orderId, itemId, timestamp }
PaymentReceived { orderId, amount, paymentId, timestamp }
OrderShipped { orderId, trackingNumber, timestamp }

```

### Projections

- **CurrentOrderState**：用于查询的物化视图
- **OrderHistory**：用于审计的完整时间线
- **DailyOrderMetrics**：分析聚合数据

### 技术选型

- Event Store：EventStoreDB（专门构建，内置 Projections 支持）
- 备选方案：Kafka + 自定义 Projection 服务

## 缺点

- 团队学习曲线
- 相比 CRUD 复杂度增加
- 需要谨慎设计事件（一旦存储即不可变）
- 存储持续增长（事件永不删除）

## 替代方案

1. **审计表**：更简单，但无法支持时间维度查询
2. **基于现有数据库的 CDC**：复杂，且不改变数据模型
3. **混合方案**：仅对订单状态变更采用 Event Sourcing

## 待解决问题

- [ ] 事件 Schema 版本控制策略
- [ ] 事件保留策略
- [ ] 快照频率的性能优化

## 实施计划

1. 单一订单类型原型验证（2 周）
2. 团队 Event Sourcing 培训（1 周）
3. 完整实现和迁移（4 周）
4. 监控和优化（持续进行）

## 参考资料

- [Event Sourcing by Martin Fowler](https://martinfowler.com/eaaDev/EventSourcing.html)
- [EventStoreDB 文档](https://www.eventstore.com/docs)
```

## ADR 管理

### 目录结构

```
docs/
├── adr/
│   ├── README.md           # 索引和指南
│   ├── template.md         # 团队的 ADR 模板
│   ├── 0001-use-postgresql.md
│   ├── 0002-caching-strategy.md
│   ├── 0003-mongodb-user-profiles.md  # [已废弃]
│   └── 0020-deprecate-mongodb.md      # 取代 0003
```

### ADR 索引（README.md）

```markdown
# 架构决策记录

本目录包含 [项目名称] 的架构决策记录（ADR）。

## 索引

| ADR                                   | 标题                              | 状态       | 日期       |
| ------------------------------------- | -------------------------------- | ---------- | ---------- |
| [0001](0001-use-postgresql.md)        | 使用 PostgreSQL 作为主数据库       | 已采纳     | 2024-01-10 |
| [0002](0002-caching-strategy.md)      | Redis 缓存策略                    | 已采纳     | 2024-01-12 |
| [0003](0003-mongodb-user-profiles.md) | MongoDB 存储用户资料              | 已废弃     | 2023-06-15 |
| [0020](0020-deprecate-mongodb.md)     | 废弃 MongoDB                     | 已采纳     | 2024-01-15 |

## 创建新 ADR

1. 复制 `template.md` 为 `NNNN-title-with-dashes.md`
2. 填写模板内容
3. 提交 PR 进行评审
4. 批准后更新本索引

## ADR 状态说明

- **Proposed**：讨论中
- **Accepted**：已做出决策，正在实施
- **Deprecated**：不再适用
- **Superseded**：已被其他 ADR 取代
- **Rejected**：已评估但未采纳
```

### 自动化工具（adr-tools）

```bash
# 安装 adr-tools
brew install adr-tools

# 初始化 ADR 目录
adr init docs/adr

# 创建新 ADR
adr new "Use PostgreSQL as Primary Database"

# 取代某个 ADR
adr new -s 3 "Deprecate MongoDB in Favor of PostgreSQL"

# 生成目录
adr generate toc > docs/adr/README.md

# 关联相关 ADR
adr link 2 "Complements" 1 "Is complemented by"
```

## 评审流程

```markdown
## ADR 评审检查清单

### 提交前

- [ ] 上下文清晰说明了问题
- [ ] 考虑了所有可行方案
- [ ] 优缺点分析平衡且客观
- [ ] 记录了正面和负面后果
- [ ] 关联了相关 ADR

### 评审中

- [ ] 至少 2 名高级工程师已评审
- [ ] 已咨询受影响的团队
- [ ] 已考虑安全影响
- [ ] 已记录成本影响
- [ ] 已评估可逆性

### 采纳后

- [ ] ADR 索引已更新
- [ ] 已通知团队
- [ ] 已创建实施工单
- [ ] 已更新相关文档
```

## 最佳实践

### 应该做的

- **尽早编写 ADR** - 在实施开始之前
- **保持简短** - 最多 1-2 页
- **坦诚权衡取舍** - 列出真实的缺点
- **关联相关决策** - 构建决策关系图
- **更新状态** - 被取代时标记为废弃

### 不应该做的

- **不要修改已采纳的 ADR** - 编写新的 ADR 来取代
- **不要省略上下文** - 未来的读者需要了解背景
- **不要隐藏失败** - 被拒绝的决策同样有价值
- **不要模糊不清** - 明确的决策，明确的后果
- **不要忘记实施** - 没有行动的 ADR 是浪费

## 参考资源

- [Documenting Architecture Decisions (Michael Nygard)](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR 模板](https://adr.github.io/madr/)
- [ADR GitHub Organization](https://adr.github.io/)
- [adr-tools](https://github.com/npryce/adr-tools)
