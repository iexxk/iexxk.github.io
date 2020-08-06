---
title: DB-MongoDB-Summary
date: 2019-01-25 09:52:17
updated: 2020-08-06 09:59:52
categories: 数据库
tags: [MongoDB]
---

### 原理

![mongo](http://gt163.cn:14033/blog/20200806095944.png)

#### 分片(shard)

分片是存储了一个集合部分数据的MongoDB实例,每个分片 可以是一台服务器运行单独一个Mongod实例，但是为了提高系统的可靠性实现自动故障恢复，一个分片应该是一个复制集。    通过分片，我们将一个集合拆分为多个数据块，这些数据块分别部署在不同的机器上，这样可以做到增加单台机器的磁盘可用空间，同时将查询分配到不同的机器上，减轻单台机器的负载。

#### 路由(Router/mongos)

mongos是一个前置路由，我们的应用客户端并不是直接与分片连接，而是与mongos路由连接，mongos接收到客户端请求后根据查询信息将请求任务分发到对应的分片，在正式生产环境中，为确保高可用性，一般会配置两台以上的mongos路由，以确保当其中一台宕机后集群还能保持高可用。

#### 配置(config)

配置服务器相当于集群的大脑，它存储了集群元信息:集群中有哪些分片、分片的是哪些集合以及数据块的分布集群启动后，当接收到请求时，如果mongos路由没有缓存配置服务器的元信息，会先从配置服务器获取分片集群对于的映射信息。同样的，为了保持集群的高可用，一般会配置多台配置服务器。

## 命令详解

```bash
mongod
--dbpath 数据库路径(数据文件)
--logpath 日志文件路径
--master 指定为主机器
--slave 指定为从机器
--source 指定主机器的IP地址
--pologSize 指定日志文件大小不超过64M.因为resync是非常操作量大且耗时，最好通过设置一个足够大的oplogSize来避免resync(默认的 oplog大小是空闲磁盘大小的5%)。
--logappend 日志文件末尾添加
--port 启用端口号
--fork 在后台运行
--only 指定只复制哪一个数据库
--slavedelay 指从复制检测的时间间隔
--auth 是否需要验证权限登录(用户名和密码)
--shardsvr 此实例为shard（分片），默认侦听27018端口
--configsvr 此实例为config server，默认侦听27019端口
```

### 基础知识

`mongod` 核心数据库进程

`mongos` 分片群集的控制器和查询路由器

`mongo` 交互式的MongoDB Shell

### mongo命令行

```bash
#启动分片服务--shardsvr指定实例为分片，默认端口为27018
mongod --shardsvr --directoryperdb --replSet shard1
#进入分片服务命令行
mongo --port 27018
#启动配置服务--configsvr指定实例为配置，默认端口为27019
mongod --configsvr --directoryperdb --replSet config --smallfiles
#进入配置服务命令行
mongo --port 27019
#查看集群状态
mongos> sh.status()
```

### docker集群搭建mongo分片服务

服务架构：

服务器两台组成docker swarm

由

* mongo-server1-shard1:27018(内|shard1主)
* mongo-server1-shard2:27018(内|shard2主)
* mongo-server2-shard1:27018(内|shard1从)
* mongo-server2-shard2:27018(内|shard2从)
* mongo-config1:27019(内|主)
* mongo-config2:27019(内|从)
* mongo-router:27017(外|每个节点一个)

8个服务组成

#### 搭建步骤（有顺序）

1. 创建服务脚本并启动

   ```yaml
    mongo-server1-shard1:
       image: mongo
       restart: always
       command: mongod --shardsvr --directoryperdb --replSet shard1
     #  ports:
     #    - 14017:27017
     #  environment:
     #    MONGO_INITDB_ROOT_USERNAME: root
     #    MONGO_INITDB_ROOT_PASSWORD: example
       volumes:
         - /data/v-yinfu/mongo/shard1/configdb:/data/configdb
         - /data/v-yinfu/mongo/shard1/db:/data/db    
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_8_centos]
     mongo-server1-shard2:
       image: mongo
       restart: always
       command: mongod --shardsvr --directoryperdb --replSet shard2
       volumes:
         - /data/v-yinfu/mongo/shard2/configdb:/data/configdb
         - /data/v-yinfu/mongo/shard2/db:/data/db  
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_8_centos]         
     mongo-server2-shard1:
       image: mongo
       restart: always
       command: mongod --shardsvr --directoryperdb --replSet shard1
       volumes:
         - /data/v-yinfu/mongo/shard1/configdb:/data/configdb
         - /data/v-yinfu/mongo/shard1/db:/data/db  
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_13_centos] 
     mongo-server2-shard2:
       image: mongo
       restart: always
       command: mongod --shardsvr --directoryperdb --replSet shard2
       volumes:
         - /data/v-yinfu/mongo/shard2/configdb:/data/configdb
         - /data/v-yinfu/mongo/shard2/db:/data/db  
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_13_centos]         
     mongo-config1:
       image: mongo
       restart: always
       command: mongod --configsvr --replSet replConfig --directoryperdb --smallfiles
       volumes:
         - /data/v-yinfu/mongo/config1/configdb:/data/configdb
         - /data/v-yinfu/mongo/config1/db:/data/db  
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_8_centos]   
     mongo-config2:
       image: mongo
       restart: always
       command: mongod --configsvr --replSet replConfig --directoryperdb --smallfiles
       volumes:
         - /data/v-yinfu/mongo/config2/configdb:/data/configdb
         - /data/v-yinfu/mongo/config2/db:/data/db  
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_13_centos]           
     mongo-router:
       image: mongo
       restart: always
       command: mongos --configdb replConfig/mongo-config1:27019,mongo-config2:27019 --bind_ip 0.0.0.0 --port 27017
       ports:
         - 14017:27017
       volumes:
         - /data/v-yinfu/mongo/router/configdb:/data/configdb
         - /data/v-yinfu/mongo/router/db:/data/db        
       depends_on:
         - mongo-config1  
       deploy:
         mode: global
       #  replicas: 1
         restart_policy:
           condition: on-failure
   ```

   #### 初始化（添加）配置服务器

2. 编写初始化脚本，首先初始化config配置服务,这里只需要初始化一个`mongo-config1`服务另一个会自动初始化

   ```bash
   docker exec -it $(docker ps | grep "mongo-config1" | awk '{ print $1 }') bash -c "echo 'rs.initiate({_id: \"replConfig\",configsvr: true, members: [{ _id : 0, host : \"mongo-config1:27019\" },{ _id : 1, host : \"mongo-config2:27019\" }, ]})' | mongo --port 27019"
   #--------------------------等效于以下命令----------------------------
   #查看容器id
   docker ps
   #进入mongo-config1容器
   docker exec -it <mongo-config1容器id> bash
   #进入容器后，连接mongo
   mongo --port 27019
   #然后执行mongo初始化命令
   rs.initiate(
     {
       _id: "replConfig",
       configsvr: true,
       members: [
         { _id : 0, host : "mongo-config1:27019" },
         { _id : 1, host : "mongo-config2:27019" }
       ]
     }
   )
   # 校验可以进入容器
   mongo --port 27019
   # 可以看到两个容器前面分别是
   replConfig:PRIMARY>
   replConfig:SECONDARY>
   # 也可以通过这个命令查看
   rs.conf()
   ```

   其他常用命令

   ```mysql
   #查看config配置
   rs.conf()
   #重置config配置，执行失败需要升级啥的看，代理方式删除挂载卷
   rs.reconfig()
   ```

3. 校验检查`mongo-router`服务是否连接成功,可以查看`Cannot reach any nodes for set replConfig`这个日志是否停止，或者进入容器执行`mongo`校验，如果2没有初始化成功，执行`mongo`会报错，成功会进入`mongos>`命令行

   #### 初始化（添加）分片服务器

4. 初始化`shard`服务，还是两种方式，一是脚本，二是手动

   ```bash
   #初始化shard1
   docker exec -it $(docker ps | grep "shard1" | awk '{ print $1 }') bash -c "echo 'rs.initiate({_id : \"shard1\", members: [{ _id : 0, host : \"mongo-server1-shard1:27018\" },{ _id : 1, host : \"mongo-server2-shard1:27018\" }]})' | mongo --port 27018"
   #初始化shard2
   docker exec -it $(docker ps | grep "shard2" | awk '{ print $1 }') bash -c "echo 'rs.initiate({_id : \"shard2\", members: [{ _id : 0, host : \"mongo-server1-shard2:27018\" },{ _id : 1, host : \"mongo-server2-shard2:27018\" }]})' | mongo --port 27018"
   #--------------等效于以下命令--------------------------------
   #进入容器省略
   #进入mongo-server1-shard1
   mongo --port 27018
   rs.initiate(
     {
       _id : "shard1",
       members: [
         { _id : 0, host : "mongo-server1-shard1:27018" },
         { _id : 1, host : "mongo-server2-shard1:27018" }
       ]
     }
   )
   
   #进入mongo-server1-shard2
   mongo --port 27018
   rs.initiate(
     {
       _id : "shard2",
       members: [
         { _id : 0, host : "mongo-server1-shard2:27018" },
         { _id : 1, host : "mongo-server2-shard2:27018" }
       ]
     }
   )
   #额外-----------------------
   //添加额外分片
   rs.add( { host: "mongodb3.example.net:27017", priority: 0, votes: 0 } )
   //添加仲裁
   rs.addArb("shard34:27018");
   //移除节点
   rs.remove("shard34:27018");
   //设置从分片可读
   db.getMongo().setSlaveOk();
   ```

   #### 添加分片集群到`mongos`中

5. 添加分片集群到`mogons`,只用添加一个即可`mongo-router`，另一个自动就有了

   ```bash
   #添加shard1分片集群到mogons
   docker exec -it $(docker ps | grep "mongo-router" | awk '{ print $1 }') bash -c "echo 'sh.addShard(\"shard1/mongo-server1-shard1:27018,mongo-server2-shard1:27018\")' | mongo "
   #添加shard1分片集群到mogons
   docker exec -it $(docker ps | grep "mongo-router" | awk '{ print $1 }') bash -c "echo 'sh.addShard(\"shard2/mongo-server1-shard2:27018,mongo-server2-shard2:27018\")' | mongo "
   ###---------------------等效于以下命令-----
   mongo
   sh.addShard("shard1/shard11:27018,shard12:27018,shard13:27018")
   sh.addShard("shard2/shard21:27018,shard22:27018,shard23:27018")
   sh.addShard("shard3/shard31:27018,shard32:27018,shard33:27018")
   
   ```

6. 查看片的状态`sh.status()`

   ```json
    sharding version: {
           "_id" : 1,
           "minCompatibleVersion" : 5,
           "currentVersion" : 6,
           "clusterId" : ObjectId("5c4b110ca28b26d76cfee0e3")
     }
     shards:
           {  "_id" : "shard1",  "host" : "shard1/mongo-server1-shard1:27018,mongo-server2-shard1:27018",  "state" : 1 }
           {  "_id" : "shard2",  "host" : "shard2/mongo-server1-shard2:27018,mongo-server2-shard2:27018",  "state" : 1 }
     active mongoses:
           "4.0.5" : 2
     autosplit:
           Currently enabled: yes
     balancer:
           Currently enabled:  yes
           Currently running:  no
           Failed balancer rounds in last 5 attempts:  0
           Migration Results for the last 24 hours:
                   No recent migrations
     databases:
           {  "_id" : "config",  "primary" : "config",  "partitioned" : true }
                   config.system.sessions
                           shard key: { "_id" : 1 }
                           unique: false
                           balancing: true
                           chunks:
                                   shard1  1
                           { "_id" : { "$minKey" : 1 } } -->> { "_id" : { "$maxKey" : 1 } } on : shard1 Timestamp(1, 0)
   ```

   #### 使能分片数据库

7. `sh.enableSharding("<database>")`仅仅只是标记数据库使能分片

   ```json
   mongos> sh.enableSharding("test")
   {
   	"ok" : 1,
   	"operationTime" : Timestamp(1563271100, 3),
   	"$clusterTime" : {
   		"clusterTime" : Timestamp(1563271100, 3),
   		"signature" : {
   			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
   			"keyId" : NumberLong(0)
   		}
   	}
   }
   ```

   err:`sun.reflect.GeneratedMethodAccessor109.invoke(Unknown Source)`

8. `sh.shardCollection("<database>.<table>",{_id:1})`

   ```
   db.table1.stats();
   { 
       "sharded" : true, 
       "shards" : { 
       }
   }   
   ```

   

9. 在`admin`执行`db.runCommand({"shardcollection":"app_test.MusicList","key":{"seat":1}})`

10. 在`app_test`执行`db.MusicList.ensureIndex({"seat":1},{background: 1})`

## 集群分析

| 模式：主+备+备+仲+仲（主备不区分） | 宕机设备  | mongo可读写 |                              |
| ---------------------------------- | --------- | ----------- | ---------------------------- |
| 主+备+仲+仲                        | -备       | 可用        | 选举时间3～4秒(偶尔发生)     |
| 主+仲+仲                           | -备-备    | 可用        | 选举<1秒，且最后一个节点为主 |
| 主+仲                              | -备-备-仲 | 不可用      | 最后一个主降级为从           |
| 主+备+仲                           | -备-仲    | 可用        |                              |
| 主+备                              | -备-仲-仲 | 不可用      | 无主                         |
| 主+备+备                           | -仲-仲    | 可用        |                              |

## 总结：

1. 3节点(1注+2副本)可宕机一台，5节点模式（1主+2副本+2仲裁）可宕机2台

2. 仲裁节点：等效于副本，参与选举，但是不能成为主节点，不存储数据

3. 节点主副本其实是不区分的，启动时随机选一个做主节点，当发现宕机是会选举一个新的主节点，当宕机过多，不足以达到高可用，主节点会自动降级，当前主从副本就不会出现主节点，mongo存储数据就会提示错误，没有主节点

4. 路由节点可以不用见主从

5. 配置节点主从可以全部宕机也能正常写数据，但是数据不会自动分片，以及不能进行分片等设置查询操作，涉及配置操作都会失败

6. 数据迁移(Sharded Cluster Balancer)，当一个分片数据过多时，会发生数据平衡，让每个分片数据相差不大

7. 数据回滚，当一个节点宕机，会通过oplog进行节点数据恢复，当数据大于oplog文件设置的大小（没设置是按磁盘的%比设置的）时，数据会被覆盖，4以前的版本，如果数据30分钟内没回滚完（未测），也会终止不会回滚，并提示错误，具体参考[MongoDB副本集的工作原理](https://www.cnblogs.com/wilber2013/p/4154406.html)

8. 读写默认通过主节点，副本节点读数据需要设置副本可读

9. 分片的设置，需要先使能库设置分片库，然后再设置分片表，删了表需要重新使能分片表

10. 当数据达到一定大小才会开始分片(60M?)

11. db.stats()默认byte，可以用参数db.stats(1024*1024)转换为mb

    ```json
    {
        "db" : "xxx",   //当前数据库
        "collections" : 27,  //当前数据库多少表 
        "objects" : 18738550,  //当前数据库所有表多少条数据
        "avgObjSize" : 1153.54876188392, //每条数据的平均大小 byte
        "dataSize" : 21615831152.0,  //所有数据的总大小
        "storageSize" : 23223312272.0,  //所有数据占的磁盘大小 
        "numExtents" : 121,
        "indexes" : 26,   //索引数 
        "indexSize" : 821082976,  //索引大小 
        "fileSize" : 25691160576.0,  //预分配给数据库的文件大小
        "nsSizeMB" : 16,
        "dataFileVersion" : {
            "major" : 4,
            "minor" : 5
        },
        "extentFreeList" : {
            "num" : 1,
            "totalSize" : 65536
        },
        "ok" : 1.0
    }
    ```

    





## 参考

[docker-swarm部署mongo分片集群](https://juejin.im/post/5c3d59aef265da613a543dbc)

[Deploy a Sharded Cluster](https://docs.mongodb.com/manual/tutorial/deploy-shard-cluster/)

[MongoDB搭建分片集群](https://www.mtyun.com/library/MongoDB-shard-cluster)

[MongoDB副本集的工作原理](https://www.cnblogs.com/wilber2013/p/4154406.html)