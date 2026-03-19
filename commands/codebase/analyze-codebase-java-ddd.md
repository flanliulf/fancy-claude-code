---
allowed-tools: Bash(find:*)、Bash(ls:*)、Bash(tree:*)、Bash(grep:*)、Bash(wc:*)、Bash(du:*)、Bash(head:*)、Bash(tail:*)、Bash(cat:*)、Bash(touch:*)、Bash(awk:*)、Bash(xargs:*)
description: 生成对整个采用 DDD 模式的 Java Spring Boot 微服务代码库的全面分析和文档
---

# 全面的 DDD Spring Boot 微服务代码库分析

## 项目发现阶段

### 目录结构 (按领域/模块组织)

!`find . -type d -not -path "./target/*" -not -path "./.git/*" -not -path "./.mvn/*" -not -path "./.gradle/*" -not -path "./build/*" | sort`

### 完整文件树

!`tree -a -I 'target|.git|.mvn|.gradle|build|*.log|*.class' -L 5`

### 文件数量与大小分析

- 总文件数: !`find . -type f -not -path "./target/*" -not -path "./.git/*" | wc -l`
- Java/Kotlin 代码文件数: !`find . -name "*.java" -o -name "*.kt" | grep -v 'target' | wc -l`
- 项目大小 (不含构建产物和 Git): !`find . -type f -not -path "./target/*" -not -path "./.git/*" -not -path "./.mvn/*" -not -path "./.gradle/*" -not -path "./build/*" -print0 | xargs -0 du -ch | tail -n 1 | awk '{print $1}'`

## 配置文件分析

### 构建与依赖管理

- Maven (pom.xml): @pom.xml
- Gradle (build.gradle): @build.gradle

### Spring Boot 核心配置

- 主要配置文件: !`find . -path "*/src/main/resources/application.yml" -o -path "*/src/main/resources/application.properties"`
- Profile 特定配置文件: !`find . -path "*/src/main/resources/application-*.yml" -o -path "*/src/main/resources/application-*.properties"`

### 容器化与 CI/CD

- Docker 文件: !`find . -name "Dockerfile*" -o -name "docker-compose*"`
- Kubernetes (K8s) 文件: !`find . -name "*.yaml" -o -name "*.yml" | grep -E "(k8s|kubernetes|deployment|service|helm)"`
- CI/CD 配置: !`find .github -name "*.yml" 2>/dev/null || find . -name ".gitlab-ci.yml" || find . -name "Jenkinsfile"`

## 源代码分析 (按 DDD 分层)

### 接口层 (Interfaces / Adapters)

- API 控制器 (Controllers): !`find . -path "*/interfaces/web/*" -o -path "*/adapter/in/web/*" | grep -E "Controller.java|Controller.kt" | head -15`
- 消息订阅者 (Subscribers): !`find . -path "*/interfaces/messaging/*" -o -path "*/adapter/in/messaging/*" | head -15`

### 应用层 (Application)

- 应用服务/用例 (Use Cases): !`find . -path "*/application/service/*" -o -path "*/application/usecase/*" | grep -E "Service.java|UseCase.java" | head -15`
- 数据传输对象 (DTOs): !`find . -path "*/application/dto/*" -o -path "*/application/command/*" -o -path "*/application/query/*" | head -20`

### 领域层 (Domain)

- 聚合根/实体 (Aggregates/Entities): !`find . -path "*/domain/model/*" -o -path "*/domain/aggregate/*" | grep -v 'Repository' | head -20`
- 仓储接口 (Repository Interfaces): !`find . -path "*/domain/model/*" -o -path "*/domain/aggregate/*" | grep 'Repository.java'`
- 领域服务 (Domain Services): !`find . -path "*/domain/service/*" | head -10`
- 领域事件 (Domain Events): !`find . -path "*/domain/event/*" | head -10`
- 值对象 (Value Objects): (通常通过命名或注解识别) !`find . -path "*/domain/model/*" | grep -E "Id.java|Address.java|Money.java"`

### 基础设施层 (Infrastructure)

- 仓储实现 (Repository Implementations): !`find . -path "*/infrastructure/persistence/*" -o -path "*/adapter/out/persistence/*" | grep 'RepositoryImpl.java' | head -15`
- 外部服务适配器 (Adapters): !`find . -path "*/infrastructure/acl/*" -o -path "*/adapter/out/messaging/*" | head -15`
- 配置文件 (Configuration): !`find . -path "*/infrastructure/configuration/*" -o -path "*/infrastructure/config/*" | head -10`

## 你的任务

基于以上所有发现的信息，创建一份包含以下内容的全面分析报告：

## 1. 项目概述

- **限界上下文 (Bounded Context)**: 描述此微服务代表哪个限界上下文 (如订单上下文、用户上下文)。
- **核心领域 (Core Domain)**: 识别并描述项目的核心业务领域。
- **技术栈**: Spring Boot 版本, Java/Kotlin 版本, 持久化框架 (JPA, MyBatis)。

## 2. 详细目录结构分析

解释按领域/模块组织的包结构，并说明 DDD 四层的作用：

- **interfaces / adapters**: 负责与外部系统交互 (如 Web, 消息队列)。
- **application**: 编排领域对象，处理用例流程，不包含业务规则。
- **domain**: 包含所有业务逻辑、聚合、实体、值对象和领域事件。是项目的核心。
- **infrastructure**: 提供技术实现，如数据库访问、消息发送、缓存等。

## 3. 文件分类解析

按 DDD 架构分层组织：

- **接口层**: Controllers, Message Listeners, DTO-Command 转换器。
- **应用层**: Application Services, Commands, Queries, DTOs。
- **领域层**: Aggregates (聚合根), Entities, Value Objects, Domain Services, Repository Interfaces, Domain Events。
- **基础设施层**: Repository Implementations, Anti-Corruption Layer (ACL), 数据库实体 (`@Entity` annotated classes), 外部服务客户端。

## 4. API 与事件分析

- **同步 API**: 记录所有 RESTful 端点及其对应的命令 (Command) 或查询 (Query)。
- **异步消息**: 记录发布的领域事件 (Domain Events) 和订阅的外部事件。
- **数据契约**: 分析 Commands, Queries, 和 Events 的数据结构。

## 5. 架构深入分析

- **架构风格**: 明确是六边形架构 (Hexagonal) 还是洋葱架构 (Onion)。
- **聚合设计**: 分析关键聚合根 (Aggregate Roots) 的设计，包括其边界和不变量。
- **数据流**: 描述一个典型用例的完整流程 (如：`Controller` -> `Application Service` -> `Aggregate` -> `Repository` -> `DB`)。
- **事务边界**: 确认事务通常在 `Application Service` 层面开启和结束。

## 6. 环境与设置分析

- **配置管理**: 如何管理不同环境的数据库连接、消息队列地址等。
- **启动与构建**: 本地开发启动命令，以及如何构建模块化的 DDD 项目。
- **部署策略**: 是将整个限界上下文部署为一个服务，还是有更细粒度的部署单元。

## 7. 技术栈分解

- **核心框架**: Spring Boot, Spring Data
- **领域层支持**: 是否使用特定 DDD 库 (如 Axon, jMolecules)。
- **持久化**: JPA/Hibernate, MyBatis, 或其他。
- **事件驱动**: Spring Events, Kafka, RabbitMQ。
- **构建工具**: Maven 多模块或 Gradle 多项目。

## 8. 可视化架构图 (六边形架构)

使用 ASCII 或 Mermaid 语法表示六边形/洋葱架构：
        ┌──────────────────┐      ┌──────────────────┐
        │   Web Adapter    │      │ Messaging Adapter│
        └────────┬─────────┘      └────────┬─────────┘
                 │                        │
                 ▼                        ▼
       ┌──────────────────────────────────────────┐
       │             Application Layer            │
       │      (Use Cases, Application Services)   │
       └───────────────────┬──────────────────────┘
                           │ (调用)
                           ▼
       ┌─────────────────────────────────────────────┐
       │                  Domain Layer               │
       │ (Aggregates, Domain Services, Repositories) │
       └───────────────────┬─────────────────────────┘
                           │ (实现)
                           ▼
       ┌──────────────────────────────────────────┐
       │            Infrastructure Layer          │
       │ ┌────────────────┐   ┌─────────────────┐ │
       │ │ DB Persistence │   │ Message Service │ │
       │ └────────────────┘   └─────────────────┘ │
       └──────────────────────────────────────────┘

## 9. 关键洞察与建议

- **领域模型纯洁性**: 领域层是否被基础设施或框架代码污染？
- **聚合边界合理性**: 聚合是否过大或过小？是否存在跨聚合的事务？
- **值对象使用**: 是否充分利用值对象来封装概念，避免基本类型偏执？
- **技术债务**: 基础设施层的实现是否过于复杂或与特定供应商绑定过深？
- **演进方向**: 建议如何重构不合理的领域模型或优化应用层逻辑。

最后，将所有输出写入一个名为 `codebase_java_ddd_cc.md` 的文件中。注意使用中文输出。
