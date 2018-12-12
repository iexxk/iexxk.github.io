---
title: idea+gradle+ssm框架之整合模板
date: 2017-05-09 08:16:28
updated: 2018-01-28 21:41:27
categories: JavaEE
tags: [JavaEE,idea,gradle,Spring,SpringMVC,MyBatis,ssm框架]
---

### 1. 新建项目ssm_template

`creat project->gradle{java+web}->{GroupId:com.xuan;artifactId:ssm_template}->next->finsh`

### 2. 创建项目目录和文件

| 根目录/                              | 描述                                       |
| --------------------------------- | ---------------------------------------- |
| src/main/webapp/WEB-INF/web.xml   | `Project Structure->Modules->+ssm_template->ssm_template_main->Web Gradle...->{点击+web.xml:src\main\webapp\WEB-INF\web.xml}`[^1] |
| src/main/java                     | Mark as： Sources(默认是，不用配置)，java代码目录      |
| src/main/resources                | Mark as： Resources(默认是，不用配置)，配置资源文件目录    |
| src/main/resources/config         | 配置文件目录（例如：spring-mvc.xml）                |
| src/main/resources/sqlMapper      | 数据库语句配置目录                                |
| src/main/java/com.xuan/dao        | 数据库接口层                                   |
| src/main/java/com.xuan/controller |                                          |

[^1]: 勾上source root{.../resources,.../java}配置Artifacts,删除`Web Application:Exploded`下红色的目录

### 3.配置web.xml

```xml
 <servlet>
        <!--名称 -->
        <servlet-name>dispatcher</servlet-name>
        <!-- Servlet类 -->
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
            <param-name>contextConfigLocation</param-name>
            <param-value>classpath:config/spring-mvc.xml</param-value>
        </init-param>
        <!-- 启动顺序，数字越小，启动越早 -->
        <load-on-startup>1</load-on-startup>
    </servlet>
    <!--所有请求都会被dispatcher拦截 -->
    <servlet-mapping>
        <servlet-name>dispatcher</servlet-name>
        <url-pattern>/</url-pattern>
    </servlet-mapping>
```

### 4. 配置build.gradle

导入相关的ssm包

```groovy
apply plugin: 'groovy'  //+
apply plugin: 'idea'  //+
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
}
```

### 5. 配置spring-mvc.xml

右键`new spring config`需要先导包才能直接new

路径：`/src/main/resources/config/spring-mvc.xml`

project structure配置：Create Spring facet `spring mvc`

```xml
<!-- 自动扫描控制器，实现支持注解的IOC ,设置要扫描的包，一般含controller类的包（解释有问题，不扫描dao，会提示错误，但不影响运行）-->
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
```

### 6. 配置spring-mybatis.xml

右键`new spring config`

路径：`/src/main/resources/config/spring-mybatis.xml`

project structure配置：Create Spring facet `spring mybatis` parent contest`spring mvc`

```xml
    <!--加载jdbc文件-->
    <context:property-placeholder location="classpath:config/jdbc-mysql.properties"/>
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
```

### 7. 配置jdbc-mysql.properties

```properties
# 将jdbc.jarDirection后的内容更改为gradle下载的
# mysql-connector-java-5.1.x.jar所在的路径，gradle自动下载的路径如下所示(未使用)
jdbc.jarDirection=/Users/xuan/.gradle/caches/modules-2/files-2.1/mysql\
/mysql-connector-java/5.1.40/ef2a2ceab1735eaaae0b5d1cccf574fb7c6e1c52/\
mysql-connector-java-5.1.40.jar
jdbc.driverClassName=com.mysql.jdbc.Driver
jdbc.url=jdbc:mysql://localhost:3306/ssm_template?\
useUnicode=true&characterEncoding=UTF-8&useSSL=false
jdbc.username=root
jdbc.password=root
```

### 8. 创建数据库`ssm_template`

```sql
CREATE DATABASE /*!32312 IF NOT EXISTS*/`ssm_template` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `ssm_template`;

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for ssm_test
-- ----------------------------
DROP TABLE IF EXISTS `ssm_test`;
CREATE TABLE `ssm_test` (
  `name` varchar(255) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of ssm_test
-- ----------------------------
INSERT INTO `ssm_test` VALUES ('ssm', 'ssm框架搭建完成');
```

### 9. 测试相关文件

##### `index.jsp`

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title>$Title$</title>
  </head>
  <body>
  <a href="test">点击测试ssm框架</a>
  <br>
  name:${ssmTest.name}
  <br>
  value:${ssmTest.value}
  </body>
</html>
```

#####  `SsmTest.java`

```java
public class SsmTest {
    String name;
    String value;

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }
}
```

##### `SsmTestDao.java`

```java
@Repository
public interface SsmTestDao {
    SsmTest getSsm(String name);
}
```

##### `TestController.java`

```java
@Controller
public class TestController {
    @Resource
    private SsmTestDao ssmTestDao;
    @RequestMapping("test")
    public String totestPage(Model model){
       SsmTest ssmTest= ssmTestDao.getSsm("ssm");
       System.out.printf(""+ssmTest.getValue()+","+ssmTest.getName());
      model.addAttribute("ssmTest",ssmTest);
        return "index";
    }
}
```

##### `ssm_test.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!--doctype必须加-->
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!-- namespace的值就是dao接口的完整路劲，就这个demo而言namespace 就是TestDao.java的完整路劲 -->
<mapper namespace="com.xuan.dao.SsmTestDao">
    <!-- 这里的id就是接口中方法的名称,resulType,返回的bean，这里为String -->
    <select id="getSsm" parameterType="String" resultType="com.xuan.model.SsmTest">
        SELECT * FROM ssm_test WHERE name= #{name}
    </select>
</mapper>
```

### 相关配置截图

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/tomcat.png)

![目录结构](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/dir.png)

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/spring.png)

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/tomcat2.png)

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/web.png)

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/artif.png)

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/sour.png)

### 项目地址：

https://github.com/xuanfong1/ssm_template

#### 如果运行不起，注意out目录，删除重试