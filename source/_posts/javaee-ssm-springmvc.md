---
title: idea+gradle+ssm框架之springMVC配置
date: 2017-04-29 23:06:28
updated: 2018-12-12 10:47:58categories: JavaEE
tags: [JavaEE,idea,gradle,Spring,SpringMVC,MyBatis,ssm框架]
---

#### 1. 新建grade项目步骤

相当于一个grade的工作空间

`New Project -> Gradle -> [java] -> Next -> {Groupld:"com.xuan",Artifactld:"worksapcename"} -> Next -> Next -> Finish`

#### 2. 在grade项目新建model

新建一个springmvc项目（这里是一个model）

`New Module->spring-[Spring MVC,Web Application,Application Server]->module name`

#### 3.运行程model

###### 注意：

运行不起，请处理`project structure`配置里面的问题，具体操作参考上一篇`eclipse项目导入idea`

#### 4.建立mvc目录结构

详见`JavaEE之MVC目录结构`和`idea之maven目录结构`笔记

#### 5.配置`web.xml`文件

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <context-param>
        <!--SpringMVC配置参数文件的位置 -->
        <param-name>contextConfigLocation</param-name>
        <param-value>classpath:spring-mvc.xml</param-value>
    </context-param>

    <listener>
        <listener-class>org.springframework.web.context.ContextLoaderListener</listener-class>
    </listener>

    <servlet>
        <!--名称 -->
        <servlet-name>dispatcher</servlet-name>
        <!-- Servlet类 -->
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:dispatcher-servlet.xml</param-value>
        </init-param>
        <!-- 启动顺序，数字越小，启动越早 -->
        <load-on-startup>1</load-on-startup>
    </servlet>
    <!--所有请求都会被dispatcher拦截 -->
    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
</web-app>
```

#### 6.Spring MVC配置文件`spring-mvc.xml`[^spring application context设置]

配置文件的目录设置在`web.xml`中的`contextConfigLocation`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc.xsd">
    <!-- 自动扫描包，实现支持注解的IOC ,设置要扫描的包，一般含controller类的包-->
    <context:component-scan base-package="com.xuan.web.controller" />

    <!-- Spring MVC不处理静态资源 -->
    <mvc:default-servlet-handler />

    <!-- 支持mvc注解驱动 -->
    <mvc:annotation-driven />

    <!-- 视图解析器 -->
    <bean
            class="org.springframework.web.servlet.view.InternalResourceViewResolver"
            id="internalResourceViewResolver">
        <!-- 前缀，设置页面的目录 -->
        <property name="prefix" value="/" />
        <!-- 后缀，页面的后缀 -->
        <property name="suffix" value=".jsp" />
    </bean>
</beans>
```

#### 7. DispatcherServlet配置文件`dispatcher-servlet.xml`[^spring servlet Application context设置]

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">

</beans>
```



### 测试

`index.jsp`文件

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title>$Title$</title>
  </head>
  <body>
  <a href="test.html">进入web测试页面</a>
  </body>
</html>
```

`test.jsp`文件

```
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title>$Title$</title>
  </head>
  <body>
  springmvc配置成功
  </body>
</html>
```

`TestController.java`

```java
@Controller
public class TestController {
    @RequestMapping("test.html")
    public ModelAndView totestPage(){
        return new ModelAndView("test.jsp");
    }
}
```

###### spring简单测试流程

```flow
index=>start: index.jsp请求test.html
DispatcherServlet=>operation: DispatcherServlet.java过滤找到分配到指定前端控制器(需要配置xml)
TestController=>operation: 前端控制器TestController.java
mvc=>operation: 后台业务逻辑（跳转逻辑）
modelAndView=>operation: 返回modelAndView
page=>operation: 前台页面test.jsp展示数据
e=>end
index->DispatcherServlet->TestController->mvc->modelAndView->page->cond



```





#### 参考：

 [Spring学习（二）——使用Gradle构建一个简单的Spring MVC Web应用程序](http://www.cnblogs.com/wenjingu/p/3822989.html)

[^spring application context设置]: `Project Structure->Modules->项目名->Spring->+->{name:"取个名字";选择设置的文件 }`
[^spring servlet Application context设置]: `Project Structure->Modules->项目名->Spring->+->{name:"取个名字";选择设置的文件;父设置spring application context}`

