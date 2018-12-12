---
title: Spring Boot Security cors跨域解决
date: 2018-03-30 15:42:12
updated: 2018-04-25 20:47:32
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





### 跨域测试

chrome console输入

```bash
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://192.168.1.230:14083/app/geography/painting/',true);
xhr.send();
```

在network查看结果





