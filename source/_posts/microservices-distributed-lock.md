---
title: 微服务之分布式锁
date: 2018-07-20 17:14:58
updated: 2018-12-12 10:47:58
categories: Microservices
tags: [Microservices,redis,lock,Distributed]
---

### 缓存分布式锁

### 官方分布式锁[redisson](https://github.com/redisson/redisson)-----[文档](https://github.com/redisson/redisson/wiki/%E7%9B%AE%E5%BD%95)

#### 基于redis缓存分布式锁

- [ ] redis宕机(已锁/未锁)
- [ ] 其中一个线程服务宕机(已锁)
- [ ] 

##### redis SETNX 命令详解

**SETNX key value** 

将 `key` 的值设为 `value` ，当且仅当 `key` 不存在。

若给定的 `key` 已经存在，则 [SETNX](http://redisdoc.com/string/setnx.html#setnx) 不做任何动作。

[SETNX](http://redisdoc.com/string/setnx.html#setnx) 是『SET if Not eXists』(如果不存在，则 SET)的简写。

`jedis.setnx(key,value);`   `key` 锁id ，`value` 过期时间





### 参考

[分布式锁的三种实现的对比](https://www.jianshu.com/p/c2b4aa7a12f1)