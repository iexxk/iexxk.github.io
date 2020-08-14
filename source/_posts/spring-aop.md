---
title: Spring-AOP
date: 2018-12-17 17:31:06
updated: 2018-12-21 23:27:26
categories: Spring
tags: [Spring,AOP,log]
---

## Spring AOP

基于动态代理实现（动态生成插入方法invoke）

#### 术语

* **连接点**(Join point)： 能够拦截（插入方法）的地方

* **切点**(Poincut)： 具体定位的连接点

* **增强/通知**(Advice)：表示添加到切点的一段**逻辑代码**，并定位连接点的**方位信息**。

  Spring AOP提供了5种Advice类型给我们：前置`@Before`、后置`@After`、返回`@AfterReturning`、异常`@AfterThrowing`、环绕`@Around`给我们使用！

* **织入**(Weaving)：将`增强/通知`添加到目标类的具体连接点上的过程

* **引入/引介**(Introduction)：允许我们**向现有的类添加新方法或属性**。是一种**特殊**的增强！

* **切面**(Aspect)：切面由切点和`增强/通知`组成，它既包括了横切逻辑的定义、也包括了连接点的定义。

#### 切入点定义

1. `execution `表达式

   eg:  `@Pointcut("execution(public * com.exxk.aop..*Controller.*(..))")` 

   `*`代表任意值

   `aop..`表示aop包下面的任何子包和自己

   `(..)`表示任何参数

2. `@annotation`注解

   eg: `@annotation(com.willson.common.annotation.Log)`

#### 注解类名字解释

##### `@Target` :

说明了Annotation所修饰的对象范围，eg`@Target({ ElementType.PARAMETER, ElementType.METHOD })`其中`ElementType`的取值有

* `CONSTRUCTOR`:用于描述构造器
* `FIELD`:用于描述域
* `LOCAL_VARIABLE`:用于描述局部变量
* `METHOD`:用于描述方法
* `PACKAGE`:用于描述包
* `PARAMETER`:用于描述参数
* `TYPE`:用于描述类、接口(包括注解类型) 或enum声明

##### `@Retention`

定义了该Annotation被保留的时间长短，eg`@Retention(RetentionPolicy.RUNTIME)`,其中`Retention`取值有

* `SOURCE`:在源文件中有效（即源文件保留）
* `CLASS`:在class文件中有效（即class保留）
* `RUNTIME`:在运行时有效（即运行时保留）

##### `@Documented`

 用于描述其它类型的annotation应该被作为被标注的程序成员的公共API，因此可以被例如javadoc此类的工具文档化。Documented是一个标记注解，没有成员。

#### springboot aop log实战

1. 引入依赖`org.springframework.boot:spring-boot-starter-aop`

2. 定义一个接口作为测试

   ```java
   package com.exxk.aop;
   @RestController
   @RequestMapping("/aop/")
   public class AopController {
       private Logger logger=Logger.getLogger(String.valueOf(getClass()));
       @GetMapping("test")
       //@Log(tag = "我是注解")
       public String aop(){
           logger.info("业务代码执行中...");
           return "aop 测试";
       }
   }
   ```

3. 定义aop切面类

   ```java
   @Aspect
   @Component
   public class LogAspect {
       private Logger logger=Logger.getLogger(String.valueOf(getClass()));
   
       //定义切入点，切入点定义注意，某些类不能动态代理
       @Pointcut("execution(public * com.exxk.aop.AopController.aop())")
       public void pointCut(){}
   
       //切入点前插入的内容
       @Before("pointCut()")
       public void doBefore(JoinPoint joinPoint){
           logger.info("切入点前执行的内容:");
           ServletRequestAttributes attributes= (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
           if (attributes != null) {
               HttpServletRequest request=attributes.getRequest();
               logger.info("URL:"+request.getRequestURL().toString());
           }
       }
   
       @AfterReturning(returning = "ret",pointcut = "pointCut()")
       public void doAfterReturning(Object ret){
           logger.info("切点运行完之后执行的内容:");
           logger.info("response:"+ret);
       }
   }
   ```

4. 调用接口之后打印日志

   ```verilog
   com.exxk.aop.LogAspect             : 切入点前执行的内容:
   com.exxk.aop.LogAspect             : URL:http://127.0.0.1:8080/aop/test
   com.exxk.aop.AopController         : 业务代码执行中...
   com.exxk.aop.LogAspect             : 切点运行完之后执行的内容:
   com.exxk.aop.LogAspect             : response返回:aop 测试
   ```

5. 添加自定义注解类

   ```java
   @Target({ ElementType.PARAMETER, ElementType.METHOD })
   @Retention(RetentionPolicy.RUNTIME)
   public @interface Log {
       String tag() default "";
   }
   ```

6. 如果要使用注解格式修改切入点为注解

   ```java
       //定义切入点
       //@Pointcut("execution(public * com.exxk.aop..*Controller.*(..))")
       //@Pointcut("execution(public * com.exxk.aop.AopController.aop())")
       @Pointcut("@annotation(com.exxk.aop.Log)")
       public void pointCut(){}
   ```

7. 在接口上添加注解`@Log(tag = "我是注解")`

8. 在切入点，eg:`doBefore`添加获取注解的内容

   ```java
   //获取注解
   Signature signature = joinPoint.getSignature();
   MethodSignature methodSignature = (MethodSignature) signature;
   Method method = methodSignature.getMethod();
   Log log= method.getAnnotation(Log.class);
   logger.info("获取注解内容："+log.tag());
   ```

9. 最后访问测试，打印日志如下

   ```verilog
   com.exxk.aop.LogAspect             : 切入点前执行的内容:
   com.exxk.aop.LogAspect             : URL:http://127.0.0.1:8080/aop/test
   com.exxk.aop.LogAspect             : 获取注解内容：我是注解
   com.exxk.aop.AopController         : 业务代码执行中...
   com.exxk.aop.LogAspect             : 切点运行完之后执行的内容:
   com.exxk.aop.LogAspect             : response返回:aop 测试
   ```

### 优化注解

1. [CGLIB](https://blog.csdn.net/qq1723205668/article/details/56481476)实现AOP在`application.properties`配置文件添加

   ```
   spring.aop.auto=true
   spring.aop.proxy-target-class=false
   ```









### 参考

[Spring Boot中使用AOP统一处理Web请求日志](http://blog.didispace.com/springbootaoplog/)

[使用Spring Boot的AOP处理自定义注解](https://crane-yuan.github.io/2018/01/11/spring-boot-aop-custom-annotation/)

[java 自定义注解之ElementType.PARAMETER](https://blog.csdn.net/qwdafedv/article/details/79939704)

[使用Spring AOP记录Controller层操作日志](https://github.com/ameizi/DevArticles/issues/152)

[Spring AOP就是这么简单啦](https://juejin.im/post/5b06bf2df265da0de2574ee1)

