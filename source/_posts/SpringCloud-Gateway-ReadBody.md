---

title: SpringCloud-Gateway-ReadBody
date: 2021-05-27 16:49:39
updated: 2021-05-27 20:03:31
categories: SpringCloud
tags: [SpringCloud,Gateway]
---

## 网关路由基础知识

[官网](https://docs.spring.io/spring-cloud-gateway/docs/2.2.8.RELEASE/reference/html/#modify-a-request-body-gatewayfilter-factory)

[SpringCloud版本对应关系](https://github.com/spring-cloud/spring-cloud-release/wiki/Spring-Cloud-Hoxton-Release-Notes)

gateway：异步网关，读取body可以通过`ReadBodyRoutePredicateFactory`进行缓存

zuul：同步阻塞式网关，因此读取或修改body就比较简单

```yaml
        - id: xkiot-cmdb
          uri: lb://xkiot-platform
          predicates:
            - Path=/cmdb/**
            # CustomReadBody 对应 CustomReadBodyRoutePredicateFactory
            # ReadBody 同理对应 ReadBodyRoutePredicateFactory
            - name: CustomReadBody
              args:
                inClass: '#{T(String)}'
                #需要在@Configuration的注解的类里面添加
                # @Bean
                # public Predicate bodyPredicate(){return o -> true;}
                predicate: '#{@bodyPredicate}' #注入实现predicate接口类            
          filters:
            # 设备token验证
            # DynamicToken对应 DynamicTokenGatewayFilterFactory
            # true对应DynamicTokenGatewayFilterFactory里面的Config类的参数
            - DynamicToken=true
            - StripPrefix=1   
```

## gateway读取body并进行签名校验

需求，只需要读取校验签名，因此不需要修改body，因此采用缓存方案进行读取，关键类`ReadBodyRoutePredicateFactory`

1. 在`@Configuration`的注解类里面添加该配置，或者新建个配置类，这里的`bodyPredicate`，会在第二部里面的yml的`predicate`进行关联

   ```java
       /**
        * 读取body断言需要注册bodyPredicate
        * @return
        */
       @Bean
       public Predicate bodyPredicate(){
           return o -> true;
       }
   ```

2. 首先加载`ReadBodyRoutePredicateFactory`类,也可以自定义重写该类，其他的修改body的类同理，加载需要在yml里面配置

   ```yml
           - id: xkiot-cmdb
             uri: lb://xkiot-platform
             predicates:
               - Path=/cmdb/**
               # CustomReadBody 对应 CustomReadBodyRoutePredicateFactory
               # ReadBody 同理对应 ReadBodyRoutePredicateFactory
               - name: CustomReadBody
                 args:
                   inClass: '#{T(String)}'
                   #需要在@Configuration的注解的类里面添加
                   # @Bean
                   # public Predicate bodyPredicate(){return o -> true;}
                   predicate: '#{@bodyPredicate}' #注入实现predicate接口类  
   ```

3. 然后实现一个过滤器，用于接受body，以及对body进行校验等

   ```java
   package com.xkiot.gateway.filter;
   
   import com.alibaba.fastjson.JSON;
   import com.xkiot.common.core.constant.CacheConstants;
   import com.xkiot.common.core.constant.Constants;
   import com.xkiot.common.core.domain.R;
   import com.xkiot.common.core.utils.ServletUtils;
   import com.xkiot.common.core.utils.StringUtils;
   import com.xkiot.common.core.web.domain.AjaxResult;
   import com.xkiot.common.redis.constant.RedisConstants;
   import com.xkiot.common.redis.service.RedisService;
   import org.slf4j.Logger;
   import org.slf4j.LoggerFactory;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.cloud.gateway.filter.GatewayFilter;
   import org.springframework.cloud.gateway.filter.factory.AbstractGatewayFilterFactory;
   import org.springframework.core.io.buffer.DataBufferFactory;
   import org.springframework.http.HttpStatus;
   import org.springframework.http.MediaType;
   import org.springframework.http.server.reactive.ServerHttpRequest;
   import org.springframework.http.server.reactive.ServerHttpResponse;
   import org.springframework.stereotype.Component;
   import org.springframework.web.server.ServerWebExchange;
   import reactor.core.publisher.Mono;
   
   import java.util.Collections;
   import java.util.List;
   
   @Component
   public class DynamicTokenGatewayFilterFactory extends AbstractGatewayFilterFactory<DynamicTokenGatewayFilterFactory.Config> {
       private static final Logger log = LoggerFactory.getLogger(DynamicTokenGatewayFilterFactory.class);
   
       private final static long EXPIRE_TIME = Constants.TOKEN_EXPIRE * 60;
   
       @Autowired
       private RedisService redisService;
   
       public DynamicTokenGatewayFilterFactory() {
           super(Config.class);
       }
   
       @Override
       public List<String> shortcutFieldOrder() {
           return Collections.singletonList("enabled");
       }
   
       @Override
       public GatewayFilter apply(DynamicTokenGatewayFilterFactory.Config config) {
           return (exchange, chain) -> {
               ServerHttpRequest request = exchange.getRequest();
               String requestBody = exchange.getAttribute("cachedRequestBodyObject");
               log.info("requestBody : {}", requestBody);
             //todo 添加验签代码等
               try {
                       ServerHttpRequest mutableReq = exchange.getRequest().mutate().header(CacheConstants.DETAILS_TERM_ID, sn)
                               .header(CacheConstants.DETAILS_TERM_ID, ServletUtils.urlEncode(sn)).build();
                       ServerWebExchange mutableExchange = exchange.mutate().request(mutableReq).build();
                       return chain.filter(mutableExchange);
               } catch (Exception e) {
                   ServerHttpResponse response = exchange.getResponse();
                   response.getHeaders().add("Content-Type", "application/json;charset=UTF-8");
                   return exchange.getResponse().writeWith(
   Mono.just(response.bufferFactory().wrap(JSON.toJSONBytes(AjaxResult.error(e.getMessage())))));
               }
               return chain.filter(exchange);
           };
       }
   
       public static class Config {
   
           private boolean enabled;
   
           public Config() {
           }
   
           public boolean isEnabled() {
               return enabled;
           }
   
           public void setEnabled(boolean enabled) {
               this.enabled = enabled;
           }
       }
   }
   ```

4. 引用第三步骤的过滤器

   ```yml
             filters:
               # 设备token验证
               # DynamicToken对应 DynamicTokenGatewayFilterFactory
               # true对应DynamicTokenGatewayFilterFactory里面的Config类的参数
               - DynamicToken=true
               - StripPrefix=1  
   ```

   

#### 参考

[API网关才是大势所趋？SpringCloud Gateway保姆级入门教程](https://zhuanlan.zhihu.com/p/373954549)

