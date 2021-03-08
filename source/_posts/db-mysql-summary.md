---
title: DB-MySQL-Summary
date: 2018-04-05 20:40:41
updated: 2019-03-06 21:39:52
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

## 备份与恢复

```bash
#备份数据库 manage geoserver两个
mysqldump -uroot -plfadmin --databases manage geoserver > ~/manageandgeoserver20180829.sql
# 恢复
mysql -uroot -plfadmin <manageandgeoserver20180829.sql
# 检查校验,进入mysql命令行
mysql -u root -p
# 显示所有数据库
mysql>  show databases;
# 使用 manage数据库
mysql> use manage;
# 显示所有用表
mysql> show tables;
#远程连接
mysql>  mysql -h172.16.16.8 -P14036 -uroot -p
```

参考 [MySql数据库备份与恢复——使用mysqldump 导入与导出方法总结](https://blog.csdn.net/helloxiaozhe/article/details/77680255)

## 主从库

1. 修改主从配置库的配置文件

主库配置：

```properties
[mysqld]
init_connect='SET NAMES utf8'
character-set-server=utf8
#无效屏蔽
# 设置mysql数据库的数据的存放目录
#datadir=/data/app/mysqldata/master/
#socket=/data/app/mysqldata/master/mysql.sock
#user=mysql
#port=3306

#Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-bin=mysql-bin
server-id=1
binlog-ignore-db=information_schema
binlog-ignore-db=mysql
binlog-do-db=shenqics
#无效屏蔽
#[mysqld_safe]
#log-error=/data/app/mysqldata/master/mysqld.log
#pid-file=/data/app/mysqldata/master/mysqld.pid

[client]
default-character-set=utf8

[mysql]
default-character-set=utf8
```

从数据库配置：

```properties
[mysqld]
init_connect='SET NAMES utf8'
character-set-server=utf8
#无效屏蔽
#datadir=/data/app/mysqldata/slave/
#socket=/data/app/mysqldata/slave/mysql.sock
#user=mysql
#port=3307

#Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0

log-bin=mysql-bin
server-id=2
binlog-ignore-db=information_schema
binlog-ignore-db=mysql
#只会复制shenqics该数据库，其他不会
replicate-do-db=shenqics
replicate-ignore-db=mysql
log-slave-updates
slave-skip-errors=all
slave-net-timeout=60

#无效屏蔽
#[mysqld_safe]
#log-error=/data/app/mysqldata/slave/mysqld.log
#pid-file=/data/app/mysqldata/slave/mysqld.pid

[client]
default-character-set=utf8

[mysql]
default-character-set=utf8
```

2. 启动服务

   ```yaml
    mysql-master:
       restart: always
       image: mysql:5.7.18
       environment:
         MYSQL_ROOT_PASSWORD: admin
       volumes:
         - /data/v-yinfu/mysql/master/data:/var/lib/mysql
         - /data/v-yinfu/mysql/master/config:/etc/mysql/conf.d
       ports:
         - target: 3306
           published: 14036
           protocol: tcp
           mode: host   
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_8_centos]      
     mysql-slave:
       restart: always
       image: mysql:5.7.18
       environment:
         MYSQL_ROOT_PASSWORD: admin
       volumes:
         - /data/v-yinfu/mysql/slave/data:/var/lib/mysql
         - /data/v-yinfu/mysql/slave/config:/etc/mysql/conf.d
       ports:
         - target: 3306
           published: 14037
           protocol: tcp
           mode: host   
       deploy:
         replicas: 1
         restart_policy:
           condition: on-failure
         placement:
           constraints: [node.hostname == VM_16_13_centos]     
   ```

3. 授权

   进入主库容器执行`mysql -uroot -p`

   ```mysql
   #ip为从库ip，设置为只有从库可以访问
   GRANT REPLICATION SLAVE ON *.* TO 'app_sync'@'172.16.16.13' IDENTIFIED BY 'password';
   GRANT ALL ON *.* TO 'app_root'@'%' IDENTIFIED BY 'password';
   GRANT SELECT ON *.* TO 'app_read'@'%' IDENTIFIED BY 'password';
   FLUSH PRIVILEGES;
   ```

4. 然后执行`show master status;`

   ```verilog
   +------------------+----------+--------------+--------------------------+-------------------+
   | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB         | Executed_Gtid_Set |
   +------------------+----------+--------------+--------------------------+-------------------+
   | mysql-bin.000003 |     1164 | shenqics     | information_schema,mysql |                   |
   +------------------+----------+--------------+--------------------------+-------------------+
   1 row in set (0.00 sec)
   ```

5. 进入从库容器执行`mysql -uroot -p`

   ```mysql
   stop slave;
   change master to master_host='172.16.16.8',master_port=14036,master_user='app_sync',master_password='password',master_log_file='mysql-bin.000003', master_log_pos=1164;
   start slave;
   show slave status;
   #授权
   GRANT SELECT ON *.* TO 'app_read'@'%' IDENTIFIED BY 'password';
   FLUSH PRIVILEGES;
   ```

6. 执行`show slave status\G;`检查是否这两个为yes

   ```ver
   Slave_IO_Running: Connecting
   Slave_SQL_Running: Yes
   ```

7. 重新注册

   ```mysql
   stop slave;
   change master to master_host='172.16.16.8',master_port=14036,master_user='app_sync',master_password='admin',master_log_file='mysql-bin.000005', master_log_pos=361;
   start slave;
   #清除log,执行start slave报错时
   reset slave;
   start slave;
   ```

8. 再次执行第6步检查



### mysql创建用户命令详解

创建用户

`GRANT 权限 ON 数据库.表名 TO '用户'@'主机' IDENTIFIED BY '密码' `

* 权限：all,select,等
* 主机：指定ip地址访问、localhost或127.0.0.1（本地访问）、%（任意主机均可访问）
* 密码：为空时则不需要密码

eg: 

```mysql
GRANT REPLICATION SLAVE ON *.* TO 'app_sync'@'172.16.16.13' IDENTIFIED BY 'admin';
#意思是创建一个专门的用户（app_sync）进行从库复制，复制任何库和任何表,密码是admin,可以访问的ip只有来源172.16.16.13（从库ip）
```

删除用户`drop user test@'172.16.16.13';`



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

4. 设置主从模式时，使用用户`'app_sync'@'172.16.16.13'`连接时提示，以及一直`Slave_IO_Running: Connecting`

   ```verilog
   ERROR 1045 (28000): Access denied for user 'app_sync'@'10.255.0.2' (using password: YES)
   ```

   解决：部署时设置host模式

   原因：非host模式连接时,访问客户端ip是内部ip不是host的ip

5. 错误

   ```verilog
   java.sql.SQLException: Incorrect string value: '\xF0\x9F\x90\xB6' for column 'UserNickname' at row 1
   ```

   解决：

   1. 在mysql配置文件添加后，重启

      ```mysql
      [client]
      default-character-set = utf8mb4
      
      [mysql]
      default-character-set = utf8mb4
      
      [mysqld]
      character-set-client-handshake = FALSE
      character-set-server = utf8mb4
      collation-server = utf8mb4_unicode_ci
      ```

   2. 修改数据表的编码

      `ALTER TABLE TABLE_NAME CONVERT TO CHARACTER SET utf8mb4;`

   3. 修改数据库连接

      `jdbc:mysql://localhost:3306/"+DATABASENAME+"?useunicode=true&characterEncoding=utf8`

      方式一：去掉参数`&characterEncoding=utf8`和`useunicode=true`

      方式二(建议)：添加`autoReconnect=true`

      

