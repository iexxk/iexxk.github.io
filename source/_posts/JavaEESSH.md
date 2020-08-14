---
title: JavaEE之ssh框架基础
date: 2017-06-19 22:14:28
updated: 2018-12-12 10:47:58categories: JavaEE
tags: [基础,java,面试]
---

## SSH基础知识

### 1 Hibernate

hibernate框架是一个ORM的持久层框架，ORM的含义是对象关系映射，简单理解就是通过对象和关系型数据库之间建立映射信息，以后再操作对象就相当于操作数据库了。hibernate框架是对JDBC进行了轻量级的封装，可以更方便简单的对数据库完成增删改查的操作。同时也提供了查询的方式和查询的策略。例如HQL和QBC的查询方式等。还提供了缓存的策略，效率会更高。

##### 优点

1. 对象/关系数据库映射(ORM)

   它使用时只需要操纵对象，使开发更对象化，抛弃了数据库中心的思想，完全的面向对象思想

2. 透明持久化(persistent)

   带有持久化状态的、具有业务功能的单线程对象，此对象生存期很短。这些对象可能是普通的JavaBeans/POJO，这个对象没有实现第三方框架或者接口，唯一特殊的是他们正与（仅仅一个）Session相关联。一旦这个Session被关闭，这些对象就会脱离持久化状态，这样就可被应用程序的任何层自由使用。（例如，用作跟表示层打交道的数据传输对象。）      

3. 事务Transaction(org.hibernate.Transaction)

   应用程序用来指定原子操作单元范围的对象，它是单线程的，生命周期很短。它通过抽象将应用从底层具体的JDBC、JTA以及CORBA事务隔离开。某些情况下，一个Session之内可
   能包含多个Transaction对象。尽管是否使用该对象是可选的，但无论是使用底层的API还是使用Transaction对象，事务边界的开启与关闭是必不可少的。

4. 它没有侵入性，即所谓的轻量级框架

5.  移植性会很好

6. 缓存机制，提供一级缓存和二级缓存

7. 简洁的HQL编程

##### 缺点

1. Hibernate在批量数据处理时有弱势
2. 针对单一对象简单的增删查改，适合于Hibernate,而对于批量的修改，删除，不适合用Hibernate,这也是OR框架的弱点；要使用数据库的特定优化机制的时候，不适合用
3. 优化策略应用不当会导致大量的资源消耗.

##### mybatis与hibernate区别

1. mybatis是把sql语句与java代码分离了，sql语句在xml文件配置的
2. hibernate是ORM框架,它对jdbc进行了封装,在分层结构中处于持久化层，它能建立面向对象的域模型和关系数据模型之间的映射.它大大简化了dao层的编码工作
3. mybatis是半自动的，hibernate是全自动的，就是说mybatis可以配置sql语句，对于sql调优来说是比较好的，hibernate会自动生成所有的sql语句，调优不方便，hibernate用起来难度要大于mybatis

### 2 Spring

##### 优点

1. Spring能有效地组织你的中间层对象，不管你是否选择使用了EJB。如果你仅仅使用了Struts或其他为J2EE的 API特制的framework，Spring致力于解决剩下的问题。
2. Spring能消除在许多工程中常见的对Singleton的过多使用。根据我的经验，这是一个很大的问题，它降低了系统的可测试性和面向对象的程度。
3. 通过一种在不同应用程序和项目间一致的方法来处理配置文件，Spring能消除各种各样自定义格式的属性文件的需要。曾经对某个类要寻找的是哪个魔法般的属性项或系统属性感到不解，为此不得不去读Javadoc甚至源编码？有了Spring，你仅仅需要看看类的JavaBean属性。Inversion of Control的使用（在下面讨论）帮助完成了这种简化。


4. 通过把对接口编程而不是对类编程的代价几乎减少到没有，Spring能够促进养成好的编程习惯。
5. Spring被设计为让使用它创建的应用尽可能少的依赖于他的APIs。在Spring应用中的大多数业务对象没有依赖于Spring。
6. 使用Spring构建的应用程序易于单元测试。
7. Spring能使EJB的使用成为一个实现选择,而不是应用架构的必然选择。你能选择用POJOs或local EJBs来实现业务接口，却不会影响调用代码。
8. Spring帮助你解决许多问题而无需使用EJB。Spring能提供一种EJB的替换物，它们适用于许多web应用。例如，Spring能使用AOP提供声明性事务管理而不通过EJB容器，如果你仅仅需要与单个数据库打交道，甚至不需要一个JTA实现。 
9. Spring为数据存取提供了一个一致的框架,不论是使用的是JDBC还是O/R mapping产品（如Hibernate）。


##### Ioc

 Inversion of Control 控制反转。

实现IoC的思想就只有两种：依赖注入（Dependency Injection，简称DI）和依赖查找（Dependency Lookup）。

##### AOP

 Aspect Oriented Programming 面向切面编程。

  Spring实现面向切面编程使用的是动态代理技术，并且会根据实际情况来选择使用基于子类的还是基于接口的动态代理。

##### 理解

1. 它的核心之一IoC，降低了我们程序的耦合度，使我们可以把项目设计成为一个可插拔的组件式工程。
2. 它的另一大核心AOP，使我们在开发过程中，精力得到释放，可以更专注的去理解客户的需求。并且在后期维护时，可以只维护很少的一部分。
3. 它提供的事务管理机制，采用声明的方式来配置事务，从而在维护时无需改动源码，解决了程序硬编码的弊端。
4. 它提供的DAO模板使我们的持久层开发又多了一种途径。
5. 它可以整合其他时下流行的框架，使我们在管理项目时，更加清晰，明确。

### 3 Struts2 

##### 优点

1. 对框架API和ServletAPI的依赖减少
2. 可扩展性提高
3. 框架对插件的可插拔
4. 拦截器
5. 可测程度大大提高

##### 缺点

1. 在并发量比较大的场景中,.每次请求都要创建一个Action,并维护很长的调用链(至少18个拦截器+OGNL解析+Action+Result),资源消耗比较大.

##### 使用场景

1. SSH对于中小型项目提供了一套完整的解决方案.在表关系相对简单,数据量不大,并发量不高的项目中,能够极大的提高开发效率.
2. 表关系复杂或数据量比较大时,可以使用Mybatis替换Hibernate.
3. 并发量很高时可以使用SpringMVC替换struts

##### 框架处理步骤

1. 客户端初始化一个指向Servlet容器（例如tomcat）的请求
2. 这个请求经过一系列的过滤器（Filter）（这些过滤器中有一个叫做ActionContextCleanUp的可选过滤器，这个过滤器对于Struts2和其他框架的集成很有帮助，例如：SiteMesh Plugin） 
3. 接着StrutsPrepareAndExecuteFilter被调用，StrutsPrepareAndExecuteFilter询问ActionMapper来解析和判断该次请求是否需要由struts2框架来处理.
4. 如果ActionMapper判断需要struts2来处理请求，StrutsPrepareAndExecuteFilter会把请求的处理交给ActionProxy 
5. ActionProxy通过Configuration Manager加载框架的配置文件，找到需要调用的Action以及拦截器配置信息
6. ActionProxy创建一个ActionInvocation的实例。 
7. ActionInvocation实例使用命名模式来调用，在调用Action的过程前后，涉及到相关拦截器（Intercepter）的调用。 
8. 一旦Action执行完毕，ActionInvocation负责根据struts.xml中的配置找到对应的返回结果配置。根据配置找到对应的Result处理类来处理结果集.大多数情况输出会交由模版语言(JSP,FreeMarker)完成输出内容拼装

#### 参考

[Java就业企业面试问题-ssh框架（强烈推荐）](http://bbs.itheima.com/thread-329951-1-1.html)