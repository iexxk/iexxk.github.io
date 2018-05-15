---
title: DB-MySQL-Summary
date: 2018-04-05 20:40:41
updated: 2018-05-15 18:58:42
categories: 数据库
tags: [mysql]
---

## 常用命令

```mysql
#连接mysql
mysql -u root -p
show status like 'Threads%';
+-------------------+-------+
| Variable_name     | Value |
+-------------------+-------+
| Threads_cached    | 8     | #连接缓存数
| Threads_connected | 81    | #打开的连接数,如果该连接数大于max_connections当前最大连接数会报错
| Threads_created   | 181   | #创建过的线程数
| Threads_running   | 1     | #正在运行的连接数
+-------------------+-------+
show variables like '%max_connections%';
+-----------------+-------+
| Variable_name   | Value |
+-----------------+-------+
| max_connections | 151   | #当前设置的最大连接数
+-----------------+-------+
 show processlist; #显示前100条的连接，如果显示所有show full processlist;
+------+------+------------------+------+---------+------+----------+------------------+
| Id   | User | Host             | db   | Command | Time | State    | Info             |
+------+------+------------------+------+---------+------+----------+------------------+
| 1100 | root | localhost        | NULL | Query   |    0 | starting | show processlist |
| 1147 | root | 10.255.0.2:52580 | xhzg | Sleep   | 7226 |          | NULL             |
+------+------+------------------+------+---------+------+----------+------------------+
 
```





mysql配置my.cnf，添加挂在卷`      - /dockerdata/manager/mysqldata/config:/etc/mysql/conf.d`

然后在挂在卷创建配置文件，添加配置`my.cnf` 文件名字随便

```properties
[mysql]
# 设置mysql客户端默认字符集
default-character-set=utf8
[mysqld]
skip-name-resolve
#设置3306端口
port = 3306
# 设置mysql的安装目录
basedir=/usr/local/mysql
# 设置mysql数据库的数据的存放目录
datadir=/usr/local/mysql/data
# 允许最大连接数
max_connections=200
# 服务端使用的字符集默认为8比特编码的latin1字符集
character-set-server=utf8
# 创建新表时将使用的默认存储引擎
default-storage-engine=INNODB
lower_case_table_names=1
max_allowed_packet=16M
sql_mode=ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```





#### 常见错误

1. `Too many connections`症状，不断重启运行springboot并访问，出现如下错误

   ```verilog
   2018-04-05 21:48:56.824 ERROR 6838 --- [           main] com.xhzg.xhzg.XhzgApplicationTests       : nested exception is org.apache.ibatis.exceptions.PersistenceException: 
   ### Error querying database.  Cause: org.springframework.jdbc.CannotGetJdbcConnectionException: Failed to obtain JDBC Connection; nested exception is com.mysql.jdbc.exceptions.jdbc4.MySQLNonTransientConnectionException: Data source rejected establishment of connection,  message from server: "Too many connections"
   ### The error may exist in com/xhzg/xhzg/mapper/UserMapper.java (best guess)
   ### The error may involve com.xhzg.xhzg.mapper.UserMapper.loadUserByUsername
   ### The error occurred while executing a query
   ### Cause: org.springframework.jdbc.CannotGetJdbcConnectionException: Failed to obtain JDBC Connection; nested exception is com.mysql.jdbc.exceptions.jdbc4.MySQLNonTransientConnectionException: Data source rejected establishment of connection,  message from server: "Too many connections"
   ```

   解决：快速解决重启mysql释放`Threads_connected`连接数，或者等待一会儿，也会慢慢释放连接数,另一种更改`max_connections`最大连接数启动mysql添加参数`--ulimit nofile=65536:65536`

   参考：

   [Docker容器中MySQL最大连接数被限制为214的解决方案](https://www.yanning.wang/archives/559.html)

   [[Increasing mysql max_connections to 1024 in a docker container](https://stackoverflow.com/questions/39054410/increasing-mysql-max-connections-to-1024-in-a-docker-container)]

2. 错误

   ```JAVA
   [Err] 1055 - Expression #1 of ORDER BY clause is not in GROUP BY clause and contains nonaggregated column 'information_schema.PROFILING.SEQ' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
   ```

   解决：

   删除配置文件`sql_mode=ONLY_FULL_GROUP_BY`这个属性值

   ```mysql
   mysql>SELECT @@sql_mode;
   mysql>SELECT @@GLOBAL.sql_mode;
   ```
   参考：https://www.zhihu.com/question/37942423

3. navicat客户端，连接mysql 8.0以上报错,提示授权啥的错误

