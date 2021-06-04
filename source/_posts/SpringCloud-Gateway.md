---
title: SpringCloud-Gateway
date: 2021-04-26 11:17:40
updated: 2021-05-27 16:48:11
categories: SpringCloud
tags: [SpringCloud,Gateway]
---

# SpringCloud Gateway设计改造

因为要做一个兼容多网络协议，多报文兼容的动态网关

## 设计架构

[![gSZKje.png](https://z3.ax1x.com/2021/04/26/gSZKje.png)](https://imgtu.com/i/gSZKje)

## 动态路由相关设置类

#### `RouteDefinitionRepository` 路由存储器

用于存储路由规则的接口，通过实现它，可以进行自定义存储路由规则到不同的中间件(redis/db等)

实现三个方法

```java
@Component
public class RedisRouteDefinitionRepository implements RouteDefinitionRepository {
    private static final Logger log = LoggerFactory.getLogger(RedisRouteDefinitionRepository.class);
    public static final String GATEWAY_ROUTES = CacheConstants.GATEWAY_ROUTES;
    @Autowired
    private RedisService redisService;

    @Override
    public Flux<RouteDefinition> getRouteDefinitions() {
        log.debug("get route info by redis/db");
        List<RouteDefinition> routeDefinitions = new ArrayList<>();
        //定义路由信息，可以从redis/db等地方获取路由信息
        redisService.getAllCacheMapValues(GATEWAY_ROUTES).stream().forEach(routeDefinition -> {
            routeDefinitions.add(JSON.parseObject(routeDefinition.toString(), RouteDefinition.class));
        });
        return Flux.fromIterable(routeDefinitions);
    }

    @Override
    public Mono<Void> save(Mono<RouteDefinition> route) {
        log.debug("save route info to redis/db");
        return route.flatMap(routeDefinition -> {
            redisService.setCacheMapValue(GATEWAY_ROUTES, routeDefinition.getId(), JSON.toJSONString(routeDefinition));
            return Mono.empty();
        });
    }

    @Override
    public Mono<Void> delete(Mono<String> routeId) {
        log.debug("delete route info by redis/db");
        return routeId.flatMap(id -> {
            if (redisService.getCacheMapValue(GATEWAY_ROUTES, id)) {
                redisService.delCacheMapValue(GATEWAY_ROUTES, id);
                return Mono.empty();
            }
            return Mono.defer(() -> Mono.error(new BaseException("路由配置没有找到: " + routeId)));
        });
    }
}
```

#### `ApplicationEventPublisherAware`事件发布接口

```java
@Service
public class GatewayServiceHandler implements ApplicationEventPublisherAware {
    private static final Logger log = LoggerFactory.getLogger(GatewayServiceHandler.class);

    @Autowired
    private RedisRouteDefinitionRepository routeDefinitionWriter;

    private ApplicationEventPublisher publisher;

    @Override
    public void setApplicationEventPublisher(ApplicationEventPublisher applicationEventPublisher) {
        this.publisher = applicationEventPublisher;
    }

    /**
     * 保存或更新多个路由配置
     * @param gatewayRouteList
     * @return
     */
    public String saveOrUpdateMultiRouteConfig(List<JSONObject> gatewayRouteList) {
        log.debug("begin add multi route config");
        gatewayRouteList.forEach(gatewayRoute -> {
            RouteDefinition definition = handleData(gatewayRoute);
            routeDefinitionWriter.save(Mono.just(definition)).subscribe();
        });
        this.publisher.publishEvent(new RefreshRoutesEvent(this));
        return "success";
    }

    /**
     * json数据转换为路由实体
     * @param gatewayRoute
     * @return
     */
    private RouteDefinition handleData(JSONObject gatewayRoute) {
        RouteDefinition definition;
        definition = JSONObject.toJavaObject(gatewayRoute, RouteDefinition.class);
        return definition;
    }
}
```

然后添加一个设置接口

```java
@RestController
@RequestMapping("/route")
public class RouteConfigController extends BaseController {
    @Autowired
    private GatewayServiceHandler gatewayServiceHandler;

    /**
     * 新增更新路由配置接口
     *
     * @param gatewayRouteList
     * @return
     */
    @PostMapping
    public AjaxResult add(@Validated @RequestBody List<JSONObject> gatewayRouteList) {
        String result = gatewayServiceHandler.saveOrUpdateMultiRouteConfig(gatewayRouteList);
        return AjaxResult.success(result);
    }
}
```

测试发送路由配置添加请求`{{gateway}}/route`

json报文数据如下:

```json
[
    {
        "id": "xkiot-auth",
        "order": 2,
        "predicates": [
            {
                "args": {
                    "pattern": "/auth/**"
                },
                "name": "Path"
            }
        ],
        "uri": "lb://xkiot-auth"
    },
    {
        "id": "xkiot-system",
        "order": 1,
        "predicates": [
            {
                "args": {
                    "pattern": "/system/**"
                },
                "name": "Path"
            }
        ],
        "uri": "lb://xkiot-system"
    }
]
```

其中`order`设置为0，代表不起用该路由配置，`id`代表服务id，`uri`代表微服务地址，`predicates`路由规则，对应的yml配置如下

```yaml
spring:
  cloud:
    gateway:
      routes:
        # 认证中心
        - id: xkiot-auth
          uri: lb://xkiot-auth
          predicates:
            - Path=/auth/**
          filters:
            # 验证码处理
            - CacheRequestFilter
            - ValidateCodeFilter
            - StripPrefix=1
        # 系统模块
        - id: xkiot-system
          uri: lb://xkiot-system
          predicates:
            - Path=/system/**
          filters:
            - StripPrefix=1
```

redis数据存储如下：

[![g9i63D.png](https://z3.ax1x.com/2021/04/27/g9i63D.png)](https://imgtu.com/i/g9i63D)



### 参考

[Srping cloud gateway 实现动态路由(MySQL持久化+redis分布式缓存)](https://www.blog-china.cn/blog/liuzaiqingshan/home/229/1594793543872)

[Nacos+Spring Cloud Gateway动态路由配置](https://developer.aliyun.com/article/759553)

