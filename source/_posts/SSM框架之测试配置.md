---
title: idea+gradle+ssm框架之测试配置
date: 2017-05-08 21:16:28
categories: JavaEE
tags: [JavaEE,idea,gradle,Spring,SpringMVC,MyBatis,ssm框架]
---

## 项目配置

#### build.gradle

```groovy
group 'com.xuan'
version '1.0-SNAPSHOT'

apply plugin: 'groovy'
apply plugin: 'java'
apply plugin: 'war'
apply plugin: 'idea'

sourceCompatibility = 1.8

repositories {
    mavenCentral()
}

dependencies {
    compile group: 'org.codehaus.groovy', name: 'groovy-all', version: '2.4.7'
    compile group: 'javax.servlet', name: 'jstl', version: '1.2'
    // Spring
    compile group: 'org.springframework', name: 'spring-core', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-web', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-webmvc', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-jdbc', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-aop', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-context', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-beans', version: '4.3.4.RELEASE'
    compile group: 'org.springframework', name: 'spring-test', version: '4.3.4.RELEASE'
    // MyBatis
    compile group: 'org.mybatis', name: 'mybatis', version: '3.4.1'
    compile group: 'org.mybatis', name: 'mybatis-spring', version: '1.3.0'
    compile group: 'mysql', name: 'mysql-connector-java', version: '5.1.40'
    // junit
    compile group: 'junit', name: 'junit', version: '4.12'

    testCompile group: 'junit', name: 'junit', version: '4.12'

}
```



#### web.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_3_1.xsd"
         version="3.1">
    <servlet>
        <!--名称 -->
        <servlet-name>dispatcher</servlet-name>
        <!-- Servlet类 -->
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:config/spring/spring-mvc.xml</param-value>
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

#### spring-mvc.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context"
       xmlns:mvc="http://www.springframework.org/schema/mvc"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/mvc http://www.springframework.org/schema/mvc/spring-mvc.xsd">
    <!-- 自动扫描控制器，实现支持注解的IOC ,设置要扫描的包，一般含controller类的包-->
    <context:component-scan base-package="com.xuan"/>

    <!-- Spring MVC不处理静态资源 -->
    <mvc:default-servlet-handler/>

    <!-- 支持mvc注解驱动，控制器映射器和控制器适配器 -->
    <mvc:annotation-driven/>

    <!--静态文件访问权限配置（静态资源映射器）-->
    <mvc:resources mapping="statics/**" location="/WEB-INF/"/>

    <!-- 视图解析器 -->
    <bean id="internalResourceViewResolver"
          class="org.springframework.web.servlet.view.InternalResourceViewResolver">
        <!-- 前缀，设置页面的目录 -->
        <property name="prefix" value="/"/>
        <!-- 后缀，页面的后缀 -->
        <property name="suffix" value=".jsp"/>
    </bean>
    <import resource="spring-mybatis.xml"/>
</beans>
```

#### spring-mybatis.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:context="http://www.springframework.org/schema/context" xmlns:tx="http://www.springframework.org/schema/tx"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd">
    <!--加载jdbc文件-->
    <context:property-placeholder location="classpath:config/mybatis/jdbc-mysql.properties"/>
    <!-- 配置数据源 -->
    <bean id="dataSource" class="org.springframework.jdbc.datasource.DriverManagerDataSource">
        <property name="driverClassName" value="${jdbc.driverClassName}"/>
        <property name="url" value="${jdbc.url}"/>
        <property name="username" value="${jdbc.username}"/>
        <property name="password" value="${jdbc.password}"/>
    </bean>

    <!-- 配置Session工厂 -->
    <bean id="sqlSessionFactory" class="org.mybatis.spring.SqlSessionFactoryBean">
        <property name="dataSource" ref="dataSource"/>
        <!-- 加载mybatis-config.xml文件，mybatis配置文件路径 -->
        <property name="configLocation" value=""/>
        <!--自动扫描需要定义类别名的包，将包内的JAVA类的类名作为类别名-->
        <property name="typeAliasesPackage" value="com.xuan.model"/>

        <!-- 指定实体类映射文件，可以指定同时指定某一包以及子包下面的所有配置文件，可以直接指定文件 -->
        <property name="mapperLocations" value="classpath:sqlMapper/*.xml"/>
    </bean>

    <!--动态代理实现 不用写dao的实现 -->
    <bean id="mapperScannerConfigurer" class="org.mybatis.spring.mapper.MapperScannerConfigurer">
        <!-- 这里的basePackage 指定了dao层接口路劲，这里的dao接口不用自己实现 -->
        <property name="basePackage" value="com.xuan.dao"/>
        <!-- 如果只有一个数据源的话可以不用指定，但是如果有多个数据源的话必须要指定 -->
        <!-- <property name="sqlSessionFactoryBeanName" value="sqlSessionFactory" /> -->
        <!--直接指定了sqlsessionTemplate名称，这个和上面的其实是一样的 -->
        <!-- <property name="sqlSessionTemplateBeanName" value="sqlSession" /> -->
    </bean>

    <!-- 配置事务管理器 -->
    <bean id="transactionManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"/>
    </bean>

    <!-- 使用全注释事务 -->
    <tx:annotation-driven transaction-manager="transactionManager"/>
</beans>
```

#### jdbc-mysql.properties

```properties
# 将jdbc.jarDirection后的内容更改为gradle下载的
# mysql-connector-java-5.1.x.jar所在的路径，gradle自动下载的路径如下所示(未使用)
jdbc.jarDirection=/Users/xuan/.gradle/caches/modules-2/files-2.1/mysql\
/mysql-connector-java/5.1.40/ef2a2ceab1735eaaae0b5d1cccf574fb7c6e1c52/\
mysql-connector-java-5.1.40.jar
jdbc.driverClassName=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/goods?\
useUnicode=true&characterEncoding=UTF-8&useSSL=false
jdbc.username=root
jdbc.password=root
```

#### 配置文件路径

| 路径（根目录/）                                 | 说明                                       |
| ---------------------------------------- | ---------------------------------------- |
| src/main/webapp/WEB-INF/web.xml          | 基本配置文件(第一步，包含spring-mvc.xml)             |
| src/main/resources/config/spring/spring-mvc.xml | 配置spring（包含spring-mybatis.xml）           |
| src/main/resources/config/spring/spring-mybatis.xml | 配置mybatis(包含sqltest.xml和jdbc-mysql.properties) |
| src/main/resources/config/mybatis/jdbc-mysql.properties | 数据库连接信息配置                                |

### 项目示例：

#### 测试文件路径

| 路径（根目录/）                                 | 说明                 |
| ---------------------------------------- | ------------------ |
| src/main/resources/sqlMapper/sqltest.xml | 数据库语句              |
| src/main/java/.../dao/TestDao.java       | 持久层，连接数据库（sqltest） |
| src/main/java/.../controller/xuantest.java |                    |
|                                          |                    |

#### TestDao.java

```java
package com.xuan.dao;

import org.springframework.stereotype.Repository;

@Repository    //注册为持久层的bean
public interface TestDao {
    String findname();
}
```

#### sqltest.xml

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper    PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<!-- namespace的值就是dao接口的完整路劲，就这个demo而言namespace 就是TestDao.java的完整路劲 -->
<mapper namespace="com.xuan.dao.TestDao">
    <!-- 这里的id就是接口中方法的名称,resulType,返回的bean，这里为String -->
    <select id="findname" resultType="java.lang.String">
      SELECT email FROM t_user WHERE loginname='123'
    </select>
</mapper>
```

#### xuantest.java

```java
package com.xuan.controller;

import com.xuan.dao.TestDao;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;
import javax.annotation.Resource;

@Controller
public class xuantest {
        @Resource
        private TestDao testDao;
        @RequestMapping("test.html")
        public ModelAndView totestPage(){
           String a= testDao.findname();
           System.out.printf(a);
            return new ModelAndView("test");
        }
}
```

#### index.jsp

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

#### test.jsp

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>spring</title>
</head>
<body>
ssm配置成功
</body>
</html>
```



##### 参考:

[常用的两种spring、mybatis 配置方式](http://blog.csdn.net/qh_java/article/details/51601139)

[使用IDEA和gradle创建超市管理系统（一）](http://wenzhiquan.github.io/2017/01/01/idea_gradle_tssm_supermarket_manage_system_1/)

[使用IDEA和gradle搭建Spring MVC和MyBatis开发环境](http://wenzhiquan.github.io/2016/04/12/idea_gradle_ssm/)

[【ssm个人博客项目实战01】SSM环境搭建](http://www.jianshu.com/p/a25e0e81a3b5)