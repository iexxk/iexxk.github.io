---
title: greenDAO3.1框架（一）认识
date: 2016-08-27 10:33:45
updated: 2018-12-12 10:47:58categories: greenDAO
tags: [greenDAO,ORM]
---
# 主流的ORM框架
>* LitePal
>* AFinal
>* greenDAO
[区别与性能分析](http://www.jianshu.com/p/8287873d97cd)

# greenDAO
## 介绍
greenDAO是一种Android数据库ORM（object/relational mapping）框架，与OrmLite、ActiveOrm、LitePal等数据库相比，单位时间内可以插入、更新和查询更多的数据，而且提供了大量的灵活通用接口。
[源码github](https://github.com/greenrobot/greenDAO) 
[官网](http://greenrobot.org/greendao/)

## GreenDao 3.0改动：
   使用过GreenDao的同学都知道，3.0之前需要通过新建GreenDaoGenerator工程生成Java数据对象（实体）和DAO对象，非常的繁琐而且也加大了使用成本。

GreenDao  3.0最大的变化就是采用注解的方式通过编译方式生成Java数据对象和DAO对象。


