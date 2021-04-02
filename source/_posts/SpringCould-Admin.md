---
title: SpringCould-Admin
date: 2021-04-02 10:05:12
updated: 2021-04-02 17:15:21
categories: SpringCloud
tags: [SpringCloud,spring-boot-admin]
---

在项目运行时，偶尔需要排查问题，需要看日志信息，但是平常只开了info级别的，对于调试找问题不是很方便，所以需要改日志重启，这里在不重启的情况下修改springboot的日志级别

## 名词介绍

* spring-boot-starter-actuator 是监控springboot的健康情况的一个依赖工具包

  包含三类功能

  1. 应用配置：日志级别、环境变量等
  2. 度量指标：心跳、内存、中间件状态
  3. 操作控制：重启、更新配置等

## 简单实现动态修改日志级别

1. 引入依赖

   ```groovy
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
   ```

2. 配置`loggers`接口,这里分别开了三个接口`/actuator/loggers`、`/actuator/info`、`/actuator/health`

   ```properties
   management.endpoints.web.exposure.include=loggers,health,info
   ```

3. 访问`GET /actuator/loggers`就可以得到所有包的日志级别了

   [![ce6aE8.png](https://z3.ax1x.com/2021/04/02/ce6aE8.png)](https://imgtu.com/i/ce6aE8)

4. 查询特定包的日志级别`GET /actuator/loggers/<package path>`

   ```json
   # GET /actuator/loggers/com.exxk.adminClient
   ---------------------------------------------
   # RETURN
   {
       "configuredLevel": null,
       "effectiveLevel": "INFO"
   }
   ```

5. 修改特定包的日志级别`POST /actuator/loggers/<package path>`然后添加 `BODY JSON `内容`{"configuredLevel": "DEBUG"}`，请求成功后对应包的日志级别就改变了，访问就会输出设置的日志级别的日志了

   ```json
   # POST /actuator/loggers/com.exxk.adminClient
   # BODY
   {
       "configuredLevel": "DEBUG"
   }
   -----------------------------------------------
   # RETURN 204 No Content
   ```

## [Spring Boot Admin](https://github.com/codecentric/spring-boot-admin)可视化管理服务

[官方文档](https://codecentric.github.io/spring-boot-admin/current/)

### 服务端配置

1. 引入依赖，注意版本号要和spring boot的版本一致，不然启动会报错

   ```groovy
   // https://mvnrepository.com/artifact/de.codecentric/spring-boot-admin-starter-server
   implementation group: 'de.codecentric', name: 'spring-boot-admin-starter-server', version: '2.2.2'
   ```

2. 在启动类上面添加注解`@EnableAdminServer`

3. 运行，然后访问`http://127.0.0.1:8080`

##### ~~添加用登陆校验~~ (未配置完，暂时不需要)

1. 添加依赖

   ```groovy
   // https://mvnrepository.com/artifact/de.codecentric/spring-boot-admin-server-ui-login
   implementation group: 'de.codecentric', name: 'spring-boot-admin-server-ui-login', version: '1.5.7'
   implementation 'org.springframework.boot:spring-boot-starter-security'
   ```

2. 添加Spring Security配置

   ```java
   @Configuration(proxyBeanMethods = false)
   public class SecuritySecureConfig extends WebSecurityConfigurerAdapter {
   
       private final AdminServerProperties adminServer;
   
       public SecuritySecureConfig(AdminServerProperties adminServer) {
           this.adminServer = adminServer;
       }
   
       @Override
       protected void configure(HttpSecurity http) throws Exception {
           SavedRequestAwareAuthenticationSuccessHandler successHandler = new SavedRequestAwareAuthenticationSuccessHandler();
           successHandler.setTargetUrlParameter("redirectTo");
           successHandler.setDefaultTargetUrl(this.adminServer.path("/"));
   
           http.authorizeRequests(
                   (authorizeRequests) -> authorizeRequests.antMatchers(this.adminServer.path("/assets/**")).permitAll()
                           .antMatchers(this.adminServer.path("/login")).permitAll().anyRequest().authenticated()
           ).formLogin(
                   (formLogin) -> formLogin.loginPage(this.adminServer.path("/login")).successHandler(successHandler).and()
           ).logout((logout) -> logout.logoutUrl(this.adminServer.path("/logout"))).httpBasic(Customizer.withDefaults())
                   .csrf((csrf) -> csrf.csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
                           .ignoringRequestMatchers(
                                   new AntPathRequestMatcher(this.adminServer.path("/instances"),
                                           HttpMethod.POST.toString()),
                                   new AntPathRequestMatcher(this.adminServer.path("/instances/*"),
                                           HttpMethod.DELETE.toString()),
                                   new AntPathRequestMatcher(this.adminServer.path("/actuator/**"))
                           ))
                   .rememberMe((rememberMe) -> rememberMe.key(UUID.randomUUID().toString()).tokenValiditySeconds(1209600));
       }
   
       // Required to provide UserDetailsService for "remember functionality"
       @Override
       protected void configure(AuthenticationManagerBuilder auth) throws Exception {
           auth.inMemoryAuthentication().withUser("user").password("{noop}password").roles("USER");
       }
   
   }
   ```

3. 在配置文件设置密码

   ```properties
   spring.boot.admin.client.username=admin
   spring.boot.admin.client.password=admin
   ```

   



### 客户端配置

1. 添加依赖

   ```groovy
   implementation group: 'de.codecentric', name: 'spring-boot-admin-starter-client', version: '2.2.2'
   ```

2. 添加配置

   ```properties
   spring.boot.admin.client.url=http://localhost:8080
   #生产根据需要开放端口，*代表全部开放
   management.endpoints.web.exposure.include=* 
   #健康信息显示所有
   management.endpoint.health.show-details=always
   ```

3. 启动运行，就可以看到该springboot已经注册到了admin server里面去了，可以去日志配置界面动态修改日志级别了

   [![ceLZ7D.png](https://z3.ax1x.com/2021/04/02/ceLZ7D.png)](https://imgtu.com/i/ceLZ7D)





### 常见问题

1. `/actuator/httptrace`网络接口追踪404，解决建议用**Sleuth**

