---
title: SpringCloud-边车服务设计
date: 2021-06-24 15:44:28
updated: 2021-07-02 16:27:04
categories: SpringCloud
tags: [SpringCloud,sidecar]
---

## 基础概念

sidecar： 微服务异构，就是指可以让其他第三方(语言)服务，接入springcloud（nacos）里面进行管理等

框架源码：[alibaba/spring-cloud-alibaba:Sidecar](https://github.com/alibaba/spring-cloud-alibaba/blob/master/spring-cloud-alibaba-docs/src/main/asciidoc-zh/sidecar.adoc)

## 需求

1. 需要接入第三方服务，第三方服务以接口方式提供

2. 第三方服务可以被其他第三方服务替换
3. 第三方服务可能不支持集群部署，就是部署多个相同的实例，数据不共享
4. 需要支持集群部署
5. 需要监控第三方服务
6. 集成到alibaba springcloud框架
7. 接入方式feign

## 设计

项目框架采用边车模式（sidecar），但是不集成`alibaba-sidecar`,手动进行实现，因为需要支持多同类型第三方服务，需要对数据进行包装，

备选方案：集成`alibaba-sidecar`,因为异构只能直接代理，因此数据的包装可以采用过滤器和解码器进行处理

#### 支持同类型第三方服务扩展替换

采用工厂设计模式进行搭建工程

#### 支持集群部署

采用边车系统部署模式，一个第三方服务一个该服务

#### 支持第三方服务监控

采用重写心跳，在心跳里面对第三方服务进行监控并绑定为自己的服务状态。

测试发现心跳是down的状态不熔断，只是降级。

```java
@Component
public class SidecarHealthIndicator extends AbstractHealthIndicator {

    @Autowired
    AiConfig aiConfig;

    @Override
    protected void doHealthCheck(Health.Builder builder) throws Exception {
        try {
            String result;
            if (aiConfig.aiFaceType.equals(FaceType.NT.name())) {
                result = HttpUtil.get(aiConfig.aiFaceUrl + "/version", aiConfig.aiFaceUrlTimeout);
                builder.withDetail("version", result);
            } else if (aiConfig.aiFaceType.equals(FaceType.KS.name())) {
                result = HttpUtil.get(aiConfig.aiFaceUrl + "/version", aiConfig.aiFaceUrlTimeout);
                JSONObject r = JSONUtil.parseObj(result);
                builder.withDetail("version", r.getStr("platform_version"));
            } else {
                result = HttpUtil.get(aiConfig.aiFaceUrl + "/version", aiConfig.aiFaceUrlTimeout);
                builder.withDetail("version", result);
            }
            builder.up();
        } catch (Exception e) {
            builder.down(e);
        }
    }
}
```

#### 第三方服务不支持集群，数据不共享（不考虑异常情况）

##### 方案1: 在业务包装接口里面实现向其他实例进行数据同步

在数据存储类型的接口里面查询该服务的其他实例，然后发同样的数据到该服务的其他实例。

注意事项：由于该服务也部署了复数个实例，因此估计需要采用redis等中间件实现那些服务已经发送过，不然会形成服务间的死循环

##### 方案2: 利用feign的重试机制

在接口里面返回指定错误码，然后根据错误码进行重试，然后计数重试次数（可采用redis进行计数），当重试次数达到了实例的个数，就说明每个实例都请求了一次了，数据都存在于每个实例了。

缺点：如果10个实例，每个实例处理请求时间2s，10个就需要20s，因为是按顺序进行请求的

##### 方案3: 利用feign拦截器异步请求其他实例（目前采用）

可以在拦截器里面设置header标志，标志其他服务不需要拦截，向其他服务请求，不然也会形成服务间的死循环

拦截器两种实现方式

* 在feign指定配置类`@FeignClient(...,configuration = MyConfiguration.class) `
* 实现`1⃣️feign.RequestInterceptor/2⃣️HandlerInterceptor/3⃣️ClientHttpRequestInterceptor`接口，进行全局拦截

这里采用接口拦截模式，配置模式会在其他项目里面引入

拦截器用`2⃣️HandlerInterceptor`,因为`1⃣️feign.RequestInterceptor`不知道为什么拦截不生效

具体实现见**附录一：spring HandlerInterceptor器的实现并读取body**

###### 步骤：

1. 继承`HttpServletRequestWrapper`实现一个读取并保存requestBody的类`BodyReaderHttpServletRequestWrapper.java`

2. 新建一个过滤器`BodyReadFilter.java`用于调用`BodyReaderHttpServletRequestWrapper`进行保存body

3. 新建一个拦截器`StatefulFeignInterceptor.java`实现`HandlerInterceptor`中的`preHandle`

4. 新建一个配置`StatefulConfig.java`用于启用拦截器`StatefulFeignInterceptor`

注意：如果要在拦截器里面使用`@Autowired`功能，就必须使用bean注入该类，不能用注解`@Component`等进行注入

向其他服务发送请求的逻辑，在`StatefulFeignInterceptor`里面的`preHandle`进行实现就可以了，代码如下

sub的作用时为了防止死循环，子服务不进行转发

```java
 if ("true".equals(request.getHeader("sub"))) {
            log.info("sub request " + request.getRequestURI());
        } else {
            ThreadUtil.execAsync(() -> {
                String uri = request.getRequestURI();
                log.info("main request " + uri);
                List<String> urls = aiConfig.aiFaceStatefulUrls;
                if (urls.contains(uri)) {
                    BodyReaderHttpServletRequestWrapper requestWrapper = null;
                    try {
                        requestWrapper = new BodyReaderHttpServletRequestWrapper(request);
                    } catch (IOException e) {
                        log.error("read body error: {}", e.getMessage());
                    }
                    String body = IoUtil.read(requestWrapper.getInputStream(), requestWrapper.getCharacterEncoding());
                    log.debug("请求体：{}", body);
                    String ip = discoveryProperties.getIp();
                    List<ServiceInstance> instanceList = discoveryClient.getInstances("xkiot-ai");
                    for (ServiceInstance serviceInstance : instanceList) {
                        if (!ip.equals(serviceInstance.getHost())) {
                            String url = serviceInstance.getUri().toString() + uri;
                            HttpRequest.post(url).header("sub", "true").body(body).execute(true).body();
                        }
                    }
                }
            });
        }
        return true;
```

注意事项：如果服务里面需要创建一个用户id，然后每台服务的用户id要一致，只能通过接口传入用户id，或者把用户id共享到redis内存里面（比较麻烦）




##### 方案4: 利用feign解码器异步请求其他实例

解码器是对请求结果进行处理，因此如果使用该模式，估计需要用中间件redis来解决服务间的死循环

##### 方案5: 幻想方案，在某个地方设置或重写，可以让feign支持向所有实例发送请求

##### 方案6: 幻想方案，利用事务或异步请求合并处理结果，该模式可以解决异常情况

##### 方案7: 解决第三方有状态服务的部署，第三方服务实现数据共享



## 附录一：spring HandlerInterceptor器的实现并读取body

`BodyReaderHttpServletRequestWrapper.java`

```java
import org.springframework.util.StreamUtils;

import javax.servlet.ReadListener;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletRequestWrapper;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class BodyReaderHttpServletRequestWrapper extends HttpServletRequestWrapper {

    private byte[] requestBody = null;//用于将流保存下来

    public BodyReaderHttpServletRequestWrapper(HttpServletRequest request) throws IOException {
        super(request);
        requestBody = StreamUtils.copyToByteArray(request.getInputStream());
    }

    @Override
    public ServletInputStream getInputStream() {
        final ByteArrayInputStream bodyStream = new ByteArrayInputStream(requestBody);
        return new ServletInputStream() {
            @Override
            public int read() {
                return bodyStream.read();  // 读取 requestBody 中的数据
            }

            @Override
            public boolean isFinished() {
                return false;
            }

            @Override
            public boolean isReady() {
                return false;
            }

            @Override
            public void setReadListener(ReadListener readListener) {
            }
        };
    }

    @Override
    public BufferedReader getReader() {
        return new BufferedReader(new InputStreamReader(getInputStream()));
    }

}
```

`BodyReadFilter.java`

```java
import org.springframework.stereotype.Component;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;

@Component
@WebFilter(urlPatterns = "/**", filterName = "BodyReadFilter")
public class BodyReadFilter implements Filter {
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        ServletRequest requestWrapper = null;
        if (servletRequest instanceof HttpServletRequest) {
            requestWrapper = new BodyReaderHttpServletRequestWrapper((HttpServletRequest) servletRequest);
        }
        if (requestWrapper == null) {
            filterChain.doFilter(servletRequest, servletResponse);
        } else {
            filterChain.doFilter(requestWrapper, servletResponse);
        }
    }
}
```

`StatefulFeignInterceptor.java`

```java
import cn.hutool.core.io.IoUtil;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


@Slf4j
public class StatefulFeignInterceptor implements HandlerInterceptor {

    @Autowired
    AiConfig aiConfig;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {

        if (aiConfig.aiFaceStatefulUrls.contains(request.getRequestURI())) {
            BodyReaderHttpServletRequestWrapper requestWrapper = new BodyReaderHttpServletRequestWrapper(request);
            String body = IoUtil.read(requestWrapper.getInputStream(), requestWrapper.getCharacterEncoding());
            log.debug("请求体：{}", body);
        }
        return true;
    }

}
```

`StatefulConfig.java`

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class StatefulConfig implements WebMvcConfigurer {

    /**
     * 解决StatefulFeignInterceptor里面的使用Autowired注入为null的问题
     *
     * @return
     */
    @Bean
    public StatefulFeignInterceptor statefulFeignInterceptor() {
        return new StatefulFeignInterceptor();
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(statefulFeignInterceptor()).addPathPatterns("/**");
    }
}
```







## 额外

Nacos 的cp/ap模式

AP模式(nacos默认模式)不支持数据一致性，所以只支持服务注册的临时实例

CP模式支持服务注册的永久实例，满足数据的一致性

这里的数据一致性，让我一度认为是指服务的所有实例数据一致，让我以为可以设置过后，每个实例都会发请求



### 参考

[SpringBoot常用拦截器（HandlerInterceptor，ClientHttpRequestInterceptor，RequestInterceptor）](http://www.cxyzjd.com/article/qq_42145871/108824056)

