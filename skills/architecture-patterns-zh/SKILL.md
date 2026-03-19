---
name: architecture-patterns
description: 实现经过验证的后端架构模式，包括 Clean Architecture、Hexagonal Architecture 和 Domain-Driven Design。适用于设计复杂后端系统或重构现有应用以提升可维护性。
---

# 架构模式

掌握经过验证的后端架构模式，包括 Clean Architecture、Hexagonal Architecture 和 Domain-Driven Design，构建可维护、可测试且可扩展的系统。

## 何时使用此 Skill

- 从零开始设计新的后端系统
- 重构单体应用以提升可维护性
- 为团队建立架构标准
- 从紧耦合架构迁移到松耦合架构
- 实施 Domain-Driven Design 原则
- 创建可测试、可 Mock 的代码库
- 规划微服务拆分

## 核心概念

### 1. Clean Architecture（Uncle Bob）

**层次（依赖方向由外向内）：**

- **Entities**：核心业务模型
- **Use Cases**：应用业务规则
- **Interface Adapters**：Controller、Presenter、Gateway
- **Frameworks & Drivers**：UI、数据库、外部服务

**核心原则：**

- 依赖方向始终指向内层
- 内层对外层一无所知
- 业务逻辑独立于框架
- 无需 UI、数据库或外部服务即可测试

### 2. Hexagonal Architecture（端口与适配器）

**组成部分：**

- **Domain Core**：业务逻辑
- **Ports**：定义交互契约的接口
- **Adapters**：端口的具体实现（数据库、REST、消息队列）

**优势：**

- 轻松替换实现（测试时使用 Mock）
- 核心与技术无关
- 关注点清晰分离

### 3. Domain-Driven Design（DDD）

**战略模式：**

- **Bounded Contexts**：为不同领域建立独立模型
- **Context Mapping**：上下文之间的关联方式
- **Ubiquitous Language**：统一的领域术语

**战术模式：**

- **Entities**：具有唯一标识的对象
- **Value Objects**：由属性定义的不可变对象
- **Aggregates**：一致性边界
- **Repositories**：数据访问抽象
- **Domain Events**：已发生的领域事件

## Clean Architecture 模式

### 目录结构

```
app/
├── domain/           # 实体与业务规则
│   ├── entities/
│   │   ├── user.py
│   │   └── order.py
│   ├── value_objects/
│   │   ├── email.py
│   │   └── money.py
│   └── interfaces/   # 抽象接口
│       ├── user_repository.py
│       └── payment_gateway.py
├── use_cases/        # 应用业务规则
│   ├── create_user.py
│   ├── process_order.py
│   └── send_notification.py
├── adapters/         # 接口实现
│   ├── repositories/
│   │   ├── postgres_user_repository.py
│   │   └── redis_cache_repository.py
│   ├── controllers/
│   │   └── user_controller.py
│   └── gateways/
│       ├── stripe_payment_gateway.py
│       └── sendgrid_email_gateway.py
└── infrastructure/   # 框架与外部关注点
    ├── database.py
    ├── config.py
    └── logging.py
```

### 实现示例

```python
# domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """核心用户实体 - 不依赖任何框架。"""
    id: str
    email: str
    name: str
    created_at: datetime
    is_active: bool = True

    def deactivate(self):
        """业务规则：停用用户。"""
        self.is_active = False

    def can_place_order(self) -> bool:
        """业务规则：仅活跃用户可下单。"""
        return self.is_active

# domain/interfaces/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.user import User

class IUserRepository(ABC):
    """端口：定义契约，不包含实现。"""

    @abstractmethod
    async def find_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass

# use_cases/create_user.py
from domain.entities.user import User
from domain.interfaces.user_repository import IUserRepository
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class CreateUserRequest:
    email: str
    name: str

@dataclass
class CreateUserResponse:
    user: User
    success: bool
    error: Optional[str] = None

class CreateUserUseCase:
    """用例：编排业务逻辑。"""

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def execute(self, request: CreateUserRequest) -> CreateUserResponse:
        # 业务校验
        existing = await self.user_repository.find_by_email(request.email)
        if existing:
            return CreateUserResponse(
                user=None,
                success=False,
                error="Email already exists"
            )

        # 创建实体
        user = User(
            id=str(uuid.uuid4()),
            email=request.email,
            name=request.name,
            created_at=datetime.now(),
            is_active=True
        )

        # 持久化
        saved_user = await self.user_repository.save(user)

        return CreateUserResponse(
            user=saved_user,
            success=True
        )

# adapters/repositories/postgres_user_repository.py
from domain.interfaces.user_repository import IUserRepository
from domain.entities.user import User
from typing import Optional
import asyncpg

class PostgresUserRepository(IUserRepository):
    """适配器：PostgreSQL 实现。"""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def find_by_id(self, user_id: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE id = $1", user_id
            )
            return self._to_entity(row) if row else None

    async def find_by_email(self, email: str) -> Optional[User]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM users WHERE email = $1", email
            )
            return self._to_entity(row) if row else None

    async def save(self, user: User) -> User:
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (id, email, name, created_at, is_active)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (id) DO UPDATE
                SET email = $2, name = $3, is_active = $5
                """,
                user.id, user.email, user.name, user.created_at, user.is_active
            )
            return user

    async def delete(self, user_id: str) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM users WHERE id = $1", user_id
            )
            return result == "DELETE 1"

    def _to_entity(self, row) -> User:
        """将数据库行映射为实体。"""
        return User(
            id=row["id"],
            email=row["email"],
            name=row["name"],
            created_at=row["created_at"],
            is_active=row["is_active"]
        )

# adapters/controllers/user_controller.py
from fastapi import APIRouter, Depends, HTTPException
from use_cases.create_user import CreateUserUseCase, CreateUserRequest
from pydantic import BaseModel

router = APIRouter()

class CreateUserDTO(BaseModel):
    email: str
    name: str

@router.post("/users")
async def create_user(
    dto: CreateUserDTO,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
):
    """Controller：仅处理 HTTP 相关逻辑。"""
    request = CreateUserRequest(email=dto.email, name=dto.name)
    response = await use_case.execute(request)

    if not response.success:
        raise HTTPException(status_code=400, detail=response.error)

    return {"user": response.user}
```

## Hexagonal Architecture 模式

```python
# 核心领域（六边形中心）
class OrderService:
    """领域服务 - 不依赖任何基础设施。"""

    def __init__(
        self,
        order_repository: OrderRepositoryPort,
        payment_gateway: PaymentGatewayPort,
        notification_service: NotificationPort
    ):
        self.orders = order_repository
        self.payments = payment_gateway
        self.notifications = notification_service

    async def place_order(self, order: Order) -> OrderResult:
        # 业务逻辑
        if not order.is_valid():
            return OrderResult(success=False, error="Invalid order")

        # 使用端口（接口）
        payment = await self.payments.charge(
            amount=order.total,
            customer=order.customer_id
        )

        if not payment.success:
            return OrderResult(success=False, error="Payment failed")

        order.mark_as_paid()
        saved_order = await self.orders.save(order)

        await self.notifications.send(
            to=order.customer_email,
            subject="Order confirmed",
            body=f"Order {order.id} confirmed"
        )

        return OrderResult(success=True, order=saved_order)

# 端口（接口）
class OrderRepositoryPort(ABC):
    @abstractmethod
    async def save(self, order: Order) -> Order:
        pass

class PaymentGatewayPort(ABC):
    @abstractmethod
    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        pass

class NotificationPort(ABC):
    @abstractmethod
    async def send(self, to: str, subject: str, body: str):
        pass

# 适配器（实现）
class StripePaymentAdapter(PaymentGatewayPort):
    """主适配器：连接 Stripe API。"""

    def __init__(self, api_key: str):
        self.stripe = stripe
        self.stripe.api_key = api_key

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        try:
            charge = self.stripe.Charge.create(
                amount=amount.cents,
                currency=amount.currency,
                customer=customer
            )
            return PaymentResult(success=True, transaction_id=charge.id)
        except stripe.error.CardError as e:
            return PaymentResult(success=False, error=str(e))

class MockPaymentAdapter(PaymentGatewayPort):
    """测试适配器：无外部依赖。"""

    async def charge(self, amount: Money, customer: str) -> PaymentResult:
        return PaymentResult(success=True, transaction_id="mock-123")
```

## Domain-Driven Design 模式

```python
# Value Objects（不可变）
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Email:
    """Value Object：经过校验的邮箱。"""
    value: str

    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError("Invalid email")

@dataclass(frozen=True)
class Money:
    """Value Object：带币种的金额。"""
    amount: int  # 以分为单位
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

# Entities（具有唯一标识）
class Order:
    """Entity：拥有标识，状态可变。"""

    def __init__(self, id: str, customer: Customer):
        self.id = id
        self.customer = customer
        self.items: List[OrderItem] = []
        self.status = OrderStatus.PENDING
        self._events: List[DomainEvent] = []

    def add_item(self, product: Product, quantity: int):
        """实体中的业务逻辑。"""
        item = OrderItem(product, quantity)
        self.items.append(item)
        self._events.append(ItemAddedEvent(self.id, item))

    def total(self) -> Money:
        """计算属性。"""
        return sum(item.subtotal() for item in self.items)

    def submit(self):
        """带业务规则的状态转换。"""
        if not self.items:
            raise ValueError("Cannot submit empty order")
        if self.status != OrderStatus.PENDING:
            raise ValueError("Order already submitted")

        self.status = OrderStatus.SUBMITTED
        self._events.append(OrderSubmittedEvent(self.id))

# Aggregates（一致性边界）
class Customer:
    """Aggregate Root：控制对内部实体的访问。"""

    def __init__(self, id: str, email: Email):
        self.id = id
        self.email = email
        self._addresses: List[Address] = []
        self._orders: List[str] = []  # 仅存储 Order ID，而非完整对象

    def add_address(self, address: Address):
        """Aggregate 强制执行不变约束。"""
        if len(self._addresses) >= 5:
            raise ValueError("Maximum 5 addresses allowed")
        self._addresses.append(address)

    @property
    def primary_address(self) -> Optional[Address]:
        return next((a for a in self._addresses if a.is_primary), None)

# Domain Events
@dataclass
class OrderSubmittedEvent:
    order_id: str
    occurred_at: datetime = field(default_factory=datetime.now)

# Repository（聚合持久化）
class OrderRepository:
    """Repository：持久化/获取聚合。"""

    async def find_by_id(self, order_id: str) -> Optional[Order]:
        """从存储中重建聚合。"""
        pass

    async def save(self, order: Order):
        """持久化聚合并发布事件。"""
        await self._persist(order)
        await self._publish_events(order._events)
        order._events.clear()
```

## 参考资源

- **references/clean-architecture-guide.md**：详细的层次划分说明
- **references/hexagonal-architecture-guide.md**：端口与适配器模式
- **references/ddd-tactical-patterns.md**：Entities、Value Objects、Aggregates
- **assets/clean-architecture-template/**：完整的项目结构模板
- **assets/ddd-examples/**：领域建模示例

## 最佳实践

1. **依赖规则**：依赖方向始终指向内层
2. **接口隔离**：保持接口小而专注
3. **业务逻辑归于领域层**：框架远离核心
4. **测试独立性**：核心逻辑无需基础设施即可测试
5. **Bounded Contexts**：清晰的领域边界
6. **Ubiquitous Language**：一致的领域术语
7. **精简 Controller**：将逻辑委托给 Use Cases
8. **充血领域模型**：数据与行为结合

## 常见陷阱

- **贫血领域模型**：Entity 只有数据没有行为
- **框架耦合**：业务逻辑依赖框架
- **臃肿 Controller**：业务逻辑写在 Controller 中
- **Repository 泄漏**：暴露 ORM 对象
- **缺少抽象**：核心层直接依赖具体实现
- **过度设计**：简单 CRUD 也用 Clean Architecture
