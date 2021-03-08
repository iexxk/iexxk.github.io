---
title: Spring Boot Security cors跨域解决
date: 2018-03-30 15:42:12
updated: 2019-03-06 20:14:34
categories: JavaEE
tags: [springboot,cors,SpringSecurity]
---

### springboot security解决cors

添加配置文件

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer{
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**");
    }
}
```

在`WebSecurityConfig extends WebSecurityConfigurerAdapter`类里面添加

```java
    @Bean
    CorsConfigurationSource corsConfigurationSource()
    {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOrigins(Arrays.asList("https://example.com"));
        configuration.setAllowedMethods(Arrays.asList("GET","POST"));
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.cors().and()....
    }
```

### tomcat配置cors（废弃）

[官网](https://tomcat.apache.org/tomcat-8.5-doc/config/filter.html#CORS_Filter)

```bash
/data/tomcat/bin/catalina.sh version
>Using CATALINA_HOME:   /data/tomcat/
vim /data/tomcat/conf/web.xml
```

添加

```xml
<filter>
  <filter-name>CorsFilter</filter-name>
  <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
  <init-param>
    <param-name>cors.allowed.origins</param-name>
<!-- 如果设置*，cors.support.credentials不能设置true不然会启动报错 -->
<!--设置成前端的访问地址例如 访问http://192.168.101.210:8006,这里就可以设置成该地址 -->      
    <param-value>*</param-value>
  </init-param>
  <init-param>
    <param-name>cors.allowed.methods</param-name>
    <param-value>GET,POST,HEAD,OPTIONS,PUT</param-value>
  </init-param>
  <init-param>
    <param-name>cors.allowed.headers</param-name>
    <param-value>Content-Type,X-Requested-With,accept,Origin,Access-Control-Request-Method,Access-Control-Request-Headers</param-value>
  </init-param>
  <init-param>
    <param-name>cors.exposed.headers</param-name>
    <param-value>Access-Control-Allow-Origin,Access-Control-Allow-Credentials</param-value>
  </init-param>
  <init-param>
    <param-name>cors.support.credentials</param-name>
    <param-value>true</param-value>
  </init-param>
  <init-param>
    <param-name>cors.preflight.maxage</param-name>
    <param-value>10</param-value>
  </init-param>
</filter>
<filter-mapping>
  <filter-name>CorsFilter</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>
```

err:

```verilog
Access to XMLHttpRequest at 'http://192.168.101.210:8005/fun/login.do?loginName=admin&pwd=a123456&yzm=2giu&userType=1' from origin 'http://127.0.0.1:32768' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

其中`from origin`后面的地址设置到`cors.allowed.origins`,多个地址`,`分割

问题：这个经测试，发现option一直提示跨域

### filter解决跨域

新建一个`CorsFilter`类

```java
package com.xxx.controller.filter;

import javax.servlet.*;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;


public class CorsFilter implements Filter {

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
    }

    @Override
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain) throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;

        String currentOrigin = request.getHeader("Origin");
        response.setHeader("Access-Control-Allow-Origin", currentOrigin);   //  允许所有域名的请求
        response.setHeader("Access-Control-Allow-Credentials", "true");
        response.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS, HEAD");
        response.setHeader("Access-Control-Allow-Headers",
                "User-Agent,Origin,Cache-Control,Content-type,Date,Server,withCredentials,AccessToken");
        response.setHeader("Access-Control-Expose-Headers", "CUSTOMSESSIONID");
        response.setHeader("Access-Control-Request-Headers", "CUSTOMSESSIONID");
        response.setHeader("Access-Control-Max-Age", "3600");
        response.setHeader("Access-Control-Allow-Headers", "x-auth-token,Origin,Access-Token,X-Requested-With,Content-Type,Accept");
        response.setHeader("Access-Control-Allow-Credentials", "true");
        if (request.getMethod().equals("OPTIONS")) {
            response.setStatus(200);
            return;
        }

        chain.doFilter(req, res);
    }

    @Override
    public void destroy() {

    }
}
```

然后在`src\main\webapp\WEB-INF\web.xml`里配置,配成第一个过滤器

```xml
    <filter>
        <filter-name>corsFilter</filter-name>
        <filter-class>com.xxx.controller.innercs.filter.CorsFilter</filter-class>
    </filter>

    <filter-mapping>
        <filter-name>corsFilter</filter-name>
        <url-pattern>/*</url-pattern>
    </filter-mapping>
```

这个和tomcat不能同时配置，会导致同时设置两个跨域地址





### 跨域测试

chrome console输入

```bash
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://192.168.1.230:14083/app/geography/painting/',true);
xhr.send();
```

在network查看结果





#### 参考

[九种跨域方式实现原理](https://mp.weixin.qq.com/s/fAIl6IYugLb2p6E-4oBJTQ)

