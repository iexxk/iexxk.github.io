---
title: Spring Boot Security cors跨域解决
date: 2018-03-30 15:42:12
updated: 2019-02-26 22:48:13
categories: JavaEE
tags: [springboot,cors,SpringSecurity]
---

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

### tomcat配置cors

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





### 跨域测试

chrome console输入

```bash
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://192.168.1.230:14083/app/geography/painting/',true);
xhr.send();
```

在network查看结果





