---
title: DB-redis-base
date: 2018-04-04 22:03:37
updated: 2018-04-25 20:41:28
categories: 数据库
tags: [nosql,redis]
---

### redis springboot常用命令

```java
	@Autowired
	StringRedisTemplate redisTemplate;
	//----------------------------------------------------------------------
	//给key设置value
	redisTemplate.opsForValue().set("key","value"); //SET key "value"
	//取key的value
	redisTemplate.opsForValue().get("key");//GET key
	//设置key在new Date()过期
	redisTemplate.expireAt("key",new Date()); //EXPIREAT key timestamp
	redisTemplate.getExpire("testttl"); //返回过期时间

```



#### 注意

reids重新设值会覆盖`expireAt`过期时间的设置