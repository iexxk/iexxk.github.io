---
title: SpringCould-Zuul
date: 2018-04-17 00:00:36
updated: 2018-04-17 00:00:36
categories: Spring
tags: [SpringCould,Zuul]
---

## SpringCould 路由网关(Zuul)

Zuul的主要功能是路由转发和过滤器。例如／api/user转发到到user服务，/api/shop转发到到shop服务。zuul默认和Ribbon结合实现了负载均衡的功能。

##### zuul功能点(下面只简单介绍勾选的)

- [ ] Authentication 认证
- [ ] Insights 洞察？
- [ ] Stress Testing 压力测试
- [ ] Canary Testing 金丝雀测试
- [ ] Dynamic Routing 动态路由
- [ ] Service Migration 服务迁移
- [ ] Load Shedding 加载脱落
- [ ] Security 安全
- [ ] Static Response handling 静态响应处理
- [ ] Active/Active traffic management 活动/活动流量管理

### 步骤

1. 新建springboot项目勾选如下

   - [x] web->web
   - [x] Could discovery-> eureka server
   - [x] Could routing->zuul

2. 在`EurekazuulApplication`启动类添加注解`@EnableZuulProxy`开启zuul功能`@EnableEurekaClient`也需要注册到服务中心

3. 在`application.yml`添加如下配置

   ```yaml
   server:
     port: 8095
   spring:
     application:
       name: zuul-client
   eureka:
     client:
       service-url:
         defaultZone: http://127.0.0.1:8091/eureka/   #注意要加eureka，不然找不到
   zuul:
     routes:
       api-a:
         path: /api-a/**  #以/api-a/ 开头的请求都转发给ribbon-client服务
         serviceId: ribbon-client
       api-b:
         path: /api-b/** #以/api-b/ 开头的请求都转发给feign-client服务
         serviceId: feign-client
   ```

4. 依次启动注册中心、ribbon服务端、feign服务端、zuul服务端

   http://127.0.0.1:8095/api-b/sayhi?name=32访问的就是feign服务端

   http://127.0.0.1:8095/api-a/resthi?name=32访问的就是ribbon服务端

5. 到此就实现了**路由功能**

##### 服务过滤

服务过滤安全校验功能等,新建一个`MyFilter`类注意加注解`@Component`,然后继承`ZuulFilter`类

```java
@Component
public class MyFilter extends ZuulFilter {

    @Override
    public String filterType() {
        return "pre";  //pre:路由之前,routing:路由之时,post:路由之后,error:发送错误调用
    }

    @Override
    public int filterOrder() {
        return 0;  //filterOrder:过滤的顺序
    }

    @Override
    public boolean shouldFilter() {
        return true;  //shouldFilter:这里可以写逻辑判断，是否要过滤，本文true,永远过滤。
    }

    @Override
    public Object run() throws ZuulException {
        //run：过滤器的具体逻辑。可用很复杂，包括查sql，nosql去判断该请求到底有没有权限访问。
        RequestContext ctx=RequestContext.getCurrentContext();
        HttpServletRequest request=ctx.getRequest();
        System.out.print("method:"+request.getMethod()+",url:"+request.getRequestURL().toString());
        Object token=request.getParameter("token");
        if (token==null){
            System.out.print("token is null");
            ctx.setSendZuulResponse(false);
            ctx.setResponseStatusCode(401);
            try {
                ctx.getResponse().getWriter().write("token is null");
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
        System.out.print("ok");
        return null;
    }
}
```

