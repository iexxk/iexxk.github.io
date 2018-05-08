---
title: DB-redis-install
date: 2018-04-04 17:02:11
updated: 2018-04-25 20:47:32
categories: 数据库
tags: [redis,nosql]
---

## docker swarm 安装 redis

1. 创建redis挂载目录`/dockerdata/v-redis`

2. 并在该目录`vim redis.conf`新建配置文件，配置文件添加如下内容

   ```
   requirepass <登陆密码，最好64位以上>
   ```

3. 编辑`vim stack-redis.yml`,内容如下

   ```yaml
   version: '3'
   services:
     redis:
       image: redis
       restart: always
       ports:
         - 14007:6379
       command: "redis-server /data/redis.conf"
       volumes:
         - "/dockerdata/v-redis:/data"
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == xuanps]
   ```

4. 运行启动`docker stack deploy -c stack-redis.yml redis`

5. 测试命令

   ```Bash
   #本地直接redis-cli不需要任何参数
   redis-cli -h host -p port -a password
   #进入redis，用改名了进行密码登陆
   AUTH "password"
   #查询所有key
   keys *
   ```

## springboot 连接redis

1. 添加`pom.xml`依赖

   ```Xml
   		<dependency>
   			<groupId>org.springframework.boot</groupId>
   			<artifactId>spring-boot-starter-data-redis</artifactId>
   		</dependency>
   ```

2. 编辑`application.yml`添加redis连接信息

   ```yaml
   spring:
     redis:
       database: 0
       host: 112.74.51.136
       port: 14007
       password: <你的密码>
   ```

3. 编写测试类

   ```Java
   	@Autowired
   	StringRedisTemplate stringRedisTemplate;
   	@Test
   	public void testredis(){
   		stringRedisTemplate.opsForValue().set("testconnect","hello world");
   		String test= stringRedisTemplate.opsForValue().get("testconnect");
   		log.info(test);
   	}
   ```



####  idea redis插件iedis



