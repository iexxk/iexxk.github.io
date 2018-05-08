---
title: SSM实战之返回json
date: 2017-06-07 19:14:28
updated: 2018-01-28 21:41:27categories: JavaEE
tags: [idea,gradle,SpringMVC,json,jackson,annotation-driven]
---

### 1.返回普通的json

返回字符串，实体类

##### 三个步骤

* Jackson jar包是否存在于工程

  ```groovy
    // https://mvnrepository.com/artifact/com.fasterxml.jackson.core/jackson-databind
    compile group: 'com.fasterxml.jackson.core', name: 'jackson-core', version: '2.8.8'
    compile group: 'com.fasterxml.jackson.core', name: 'jackson-databind', version: '2.8.8'
    compile group: 'com.fasterxml.jackson.core', name: 'jackson-annotations', version: '2.8.8'
  ```

* `<mvc:annotation-driven/>` 是否配置（默认配置方案，不支持返回map）

* 返回方法上面是否添加了`@ResponseBody`注解。

  ```java
      @RequestMapping(value = "/test", method = RequestMethod.POST)
      @ResponseBody
      public String test( User user,HttpServletRequest req, HttpServletResponse response){
        return "json数据";
      }
  ```

### 2.map自动转换json ,`<mvc:annotation-driven/>` 的自定义配置

[解决springmvc ResponseBody请求返回406的问题](http://blog.csdn.net/tang19880721/article/details/50786294)

### 注意不能用.html后缀