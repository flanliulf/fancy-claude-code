---
name: java-testing
description: 测试 Java 应用 - JUnit 5、Mockito、集成测试、TDD 模式
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 04-java-testing
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# 参数校验
parameters:
  test_type:
    type: string
    enum: [unit, integration, e2e, contract]
    description: 要创建的测试类型
  framework:
    type: string
    default: junit5
    enum: [junit5, testng]
    description: 测试框架
---

# Java 测试技能

使用现代测试实践为 Java 应用编写全面的测试。

## 概述

本技能涵盖使用 JUnit 5、Mockito、AssertJ 进行 Java 测试，以及使用 Spring Boot Test 和 Testcontainers 进行集成测试。包括 TDD 模式和测试覆盖率策略。

## 何时使用此技能

当你需要：
- 使用 JUnit 5 编写单元测试
- 使用 Mockito 创建 Mock 对象
- 使用 Testcontainers 构建集成测试
- 实施 TDD/BDD 实践
- 提升测试覆盖率

## 涵盖的主题

### JUnit 5
- @Test、@Nested、@DisplayName
- @ParameterizedTest 与数据源
- 生命周期注解
- 扩展与自定义注解

### Mockito
- @Mock、@InjectMocks、@Spy
- 打桩（when/thenReturn）
- 验证（verify、times）
- BDD 风格（given/willReturn）

### AssertJ
- 流式断言
- 集合断言
- 异常断言
- 自定义断言

### 集成测试
- @SpringBootTest 切片测试
- Testcontainers 配置
- MockMvc 用于 API 测试
- 数据库测试

## 快速参考

```java
// 使用 Mockito 的单元测试
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    @DisplayName("Should find user by ID")
    void shouldFindUserById() {
        // 准备
        User user = new User(1L, "John");
        given(userRepository.findById(1L)).willReturn(Optional.of(user));

        // 执行
        Optional<User> result = userService.findById(1L);

        // 验证
        assertThat(result)
            .isPresent()
            .hasValueSatisfying(u ->
                assertThat(u.getName()).isEqualTo("John"));
        then(userRepository).should().findById(1L);
    }
}

// 参数化测试
@ParameterizedTest
@CsvSource({
    "valid@email.com, true",
    "invalid-email, false",
    "'', false"
})
void shouldValidateEmail(String email, boolean expected) {
    assertThat(validator.isValid(email)).isEqualTo(expected);
}

// 使用 Testcontainers 的集成测试
@Testcontainers
@SpringBootTest
class OrderRepositoryIT {

    @Container
    static PostgreSQLContainer<?> postgres =
        new PostgreSQLContainer<>("postgres:15");

    @DynamicPropertySource
    static void configure(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private OrderRepository repository;

    @Test
    void shouldPersistOrder() {
        Order saved = repository.save(new Order("item", 100.0));
        assertThat(saved.getId()).isNotNull();
    }
}

// 使用 MockMvc 的 API 测试
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void shouldReturnUser() throws Exception {
        given(userService.findById(1L))
            .willReturn(Optional.of(new User(1L, "John")));

        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.name").value("John"));
    }
}
```

## 测试数据构建器

```java
public class UserTestBuilder {
    private Long id = 1L;
    private String name = "John Doe";
    private String email = "john@example.com";
    private boolean active = true;

    public static UserTestBuilder aUser() {
        return new UserTestBuilder();
    }

    public UserTestBuilder withName(String name) {
        this.name = name;
        return this;
    }

    public UserTestBuilder inactive() {
        this.active = false;
        return this;
    }

    public User build() {
        return new User(id, name, email, active);
    }
}

// 用法
User user = aUser().withName("Jane").inactive().build();
```

## 覆盖率目标

```xml
<!-- JaCoCo 配置 -->
<configuration>
    <rules>
        <rule>
            <element>BUNDLE</element>
            <limits>
                <limit>
                    <counter>LINE</counter>
                    <value>COVEREDRATIO</value>
                    <minimum>0.80</minimum>
                </limit>
            </limits>
        </rule>
    </rules>
</configuration>
```

## 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Mock 不生效 | 缺少 @ExtendWith | 添加 MockitoExtension |
| 测试中出现 NPE | Mock 未初始化 | 检查 @InjectMocks |
| 不稳定测试 | 共享状态 | 隔离测试数据 |
| 上下文加载失败 | 缺少 Bean | 使用 @MockBean |

### 调试清单
```
□ 单独运行测试以隔离问题
□ 检查 Mock 设置是否匹配调用
□ 验证 @BeforeEach 的初始化
□ 审查 @Transactional 边界
□ 检查是否存在共享的可变状态
```

## 用法

```
Skill("java-testing")
```

## 相关技能
- `java-testing-advanced` - 高级测试模式
- `java-spring-boot` - Spring 切片测试
