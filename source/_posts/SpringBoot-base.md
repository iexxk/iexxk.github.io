---
title: SpringBoot-base
date: 2018-03-28 18:51:50
updated: 2018-04-12 02:22:05
categories: Spring
tags: [Java,Springboot]
---

## springboot 基础

### 注解

`@CrossOrigin` 跨域处理

### json处理

springboot集成`jackson`工具

简单使用

```java
//忽略编译该参数为json    
@JsonIgnore 
public String getPassword() {
    return password;
}
//bean to json
ObjectMapper mapper = new ObjectMapper();
User user=new User();
String jsonstr=mapper.writeValueAsString(user);

@RestController //返回实体类自动转json
public class UserControl {
    @RequestMapping(value = "register", method = RequestMethod.POST)
    public Msg userReg(@RequestBody User user) { //@RequestBody 请求参数为json自动转换实体类
        return user;
    }
}

```



