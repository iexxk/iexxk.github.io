---
title: SSM实战之用户登陆流程
date: 2017-05-17 17:42:28
categories: JavaEE
tags: [JavaEE,idea,gradle,Spring,SpringMVC,MyBatis,实战]
---

### 1. 显示层

前端页面`login.jsp`

在`InternalResourceViewResolver`配置jsp目录

```jsp
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>欢迎登陆</title>
</head>
<body>
<form id="login" action="<c:url value='/user/login.do'/>" method="post">
    <h1>Log In</h1>
    <fieldset id="inputs">
        <input id="username" name="name" type="text" placeholder="Username" autofocus required>
        <input id="password" name="password" type="password" placeholder="Password" required>
    </fieldset>
    <fieldset id="actions">
        <input type="submit" id="submit" value="Log in">
        <a href="">Forgot your password?</a><a href="">Register</a>
    </fieldset>
</form>
</body>
</html>
```

前端控制层`UserController.java`

在`spring-mvc.xml`配置`<context:component-scan base-package="com.xuan.user.controller"/>`

```java
@Controller
@RequestMapping(value = "user")
public class UserController {
    @Resource
    private UserService userService;
  	@RequestMapping(value = "/login",method = RequestMethod.POST)
    public ModelAndView login(User user, HttpServletRequest req) {
        ModelAndView modelAndView = new ModelAndView("index");
        if (user == null) {
            return new ModelAndView("login").addObject("message", "登陆信息不能为空！");
        }
        if (StringUtils.isEmpty(user.getName()) || StringUtils.isEmpty(user.getPassword())){
            return new ModelAndView("login").addObject("message", "用户名或密码不能为空！");
        }
        user = userService.login(user);
        modelAndView.addObject("user", user);
        return modelAndView;
    }
}
```

### 2.业务控制层

service接口层

业务接口`UserService.java`

```java
public interface UserService {
    public User login(User user);
}
```

service接口实现层（impl）

业务实现`UserServiceImpl.java`

```java
@Service("userService")
public class UserServiceImpl implements UserService{
    @Resource
    private UserDao userDao;
    @Override
    public User login(User user) {
        return userDao.findByUser(user);
    }
}
```

### 3.持久层

在`spring-beans.xml`配置`MapperScannerConfigurer`

```
<context:component-scan base-package="com.xuan"/>
```

接口层`UserDao.jva`

```java
@Repository //注册为持久层的bean
public interface UserDao {
    User findByUser(@Param("user") User user);
}
```

sqlmapper数据库语句

在`spring-bean.xml`配置`SqlSessionFactoryBean`

`userMapper.xml`

```xml-dtd
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!-- namespace的值就是dao接口的完整路劲，就这个demo而言namespace 就是TestDao.java的完整路劲 -->
<mapper namespace="com.xuan.user.dao.UserDao">
    <select id="findByUser" parameterType="com.xuan.user.model.User" resultType="com.xuan.user.model.User">
        SELECT * FROM x_user WHERE (`name`=#{user.name} OR `email`=#{user.email} OR `phone`=#{user.phone}) AND `password`=#{user.password};
    </select>
</mapper>
```

###  4. 实体

model实体层

在`mybatis-conf.xml`配置`<typeAliases><package name="com.xuan.user.model"/></typeAliases>`

实体类`User.java`

```java
public class User(){
  	.....
    private String name;
    private String password;
  	.....
}
```

