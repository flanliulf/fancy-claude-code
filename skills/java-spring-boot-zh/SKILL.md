---
name: java-spring-boot
description: 构建生产级 Spring Boot 应用 - REST API、Security、Data、Actuator
sasmp_version: "1.3.0"
version: "3.0.0"
bonded_agent: 03-java-spring
bond_type: PRIMARY_BOND
allowed-tools: Read, Write, Bash, Glob, Grep

# 参数校验
parameters:
  spring_version:
    type: string
    default: "3.2"
    description: Spring Boot 版本
  module:
    type: string
    enum: [web, security, data, actuator, cloud]
    description: Spring 模块聚焦方向
---

# Java Spring Boot 技能

使用现代最佳实践构建生产就绪的 Spring Boot 应用。

## 概述

本技能涵盖 Spring Boot 开发，包括 REST API、安全配置、数据访问、Actuator 监控和云集成。遵循 Spring Boot 3.x 模式，着重于生产就绪性。

## 何时使用此技能

当你需要：
- 使用 Spring MVC/WebFlux 创建 REST API
- 配置 Spring Security（OAuth2、JWT）
- 使用 Spring Data 设置数据库访问
- 使用 Actuator 启用监控
- 集成 Spring Cloud

## 涵盖的主题

### Spring Boot 核心
- 自动配置与 Starter
- 应用属性与 Profiles
- Bean 生命周期与配置
- DevTools 与热重载

### REST API 开发
- @RestController 与 @RequestMapping
- 请求/响应处理
- 使用 Bean Validation 进行校验
- 使用 @ControllerAdvice 处理异常

### Spring Security
- SecurityFilterChain 配置
- OAuth2 与 JWT 认证
- 方法级安全（@PreAuthorize）
- CORS 与 CSRF 配置

### Spring Data JPA
- Repository 模式
- 查询方法与 @Query
- 分页与排序
- 审计与事务

### Actuator 与监控
- 健康检查与探针
- 使用 Micrometer 的指标
- 自定义端点
- Prometheus 集成

## 快速参考

```java
// REST 控制器
@RestController
@RequestMapping("/api/users")
@Validated
public class UserController {

    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return userService.findById(id)
            .map(ResponseEntity::ok)
            .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<User> createUser(@Valid @RequestBody UserRequest request) {
        User user = userService.create(request);
        URI location = URI.create("/api/users/" + user.getId());
        return ResponseEntity.created(location).body(user);
    }
}

// 安全配置
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
            .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .anyRequest().authenticated())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
            .build();
    }
}

// 全局异常处理器
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(EntityNotFoundException.class)
    public ProblemDetail handleNotFound(EntityNotFoundException ex) {
        return ProblemDetail.forStatusAndDetail(NOT_FOUND, ex.getMessage());
    }
}
```

## 配置模板

```yaml
# application.yml
spring:
  application:
    name: ${APP_NAME:my-service}
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:local}
  jpa:
    open-in-view: false
    properties:
      hibernate:
        jdbc.batch_size: 50

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      probes:
        enabled: true

server:
  error:
    include-stacktrace: never
```

## 常用模式

### 分层架构
```
Controller → Service → Repository → Database
     ↓           ↓          ↓
   DTOs      Entities    Entities
```

### 校验模式
```java
public record CreateUserRequest(
    @NotBlank @Size(max = 100) String name,
    @Email @NotBlank String email,
    @NotNull @Min(18) Integer age
) {}
```

## 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Bean 未找到 | 缺少 @Component | 添加注解或 @Bean |
| 循环依赖 | 构造器注入 | 使用 @Lazy 或重构 |
| 401 未授权 | Security 配置问题 | 检查 permitAll 路径 |
| 启动缓慢 | 过多自动配置 | 排除未使用的 Starter |

### 调试属性
```properties
debug=true
logging.level.org.springframework.security=DEBUG
spring.jpa.show-sql=true
```

### 调试清单
```
□ 检查 /actuator/conditions
□ 验证活跃的 Profiles
□ 审查 Security Filter Chain
□ 检查 Bean 定义
□ 测试健康检查端点
```

## 用法

```
Skill("java-spring-boot")
```

## 相关技能
- `java-testing` - Spring 测试模式
- `java-jpa-hibernate` - 数据访问
