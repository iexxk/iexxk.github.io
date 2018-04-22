---
title: DB-oracle-install
date: 2018-04-20 12:02:11
updated: 2018-04-20 12:02:11
categories: 数据库
tags: [oracle,sql]
---

## Docker 安装 Oracle

镜像：[sath89/oracle-12c](https://hub.docker.com/r/sath89/oracle-12c/)

| 类别   | host                                  | container                   | 备注                               |
| ------ | ------------------------------------- | --------------------------- | ---------------------------------- |
| port   | 1521                                  | 1521                        |                                    |
| port   | 8080                                  | 8080                        |                                    |
| volume | /dockerdata/manager/oracledata/initdb | /docker-entrypoint-initdb.d | 初始化导入数据库用(非必需)         |
| volume | /dockerdata/manager/oracledata/data   | /u01/app/oracle             |                                    |
| env    | IMPORT_FROM_VOLUME                    | true                        | 触发首次运行自动初始化数据(非必需) |

oracle初始用户

```yaml
port: 1521
sid: xe
service name: xe
username: system
password: oracle
user: sys
password: oracle
connect as sysdba: true
```

运行完成后，注意这里第一次运行要初始化，注意看日志，等待它完成

#### 配置

##### 修改数据库服务名`xe`为`pdborcl`

参考：[Oracle 更改服务名方法](https://www.jianshu.com/p/879e8085c012)

1.  进入容器内执行命令，连接Oracle，执行`sqlplus sys/oracle as sysdba` 进入oracle，其中sys为用户名，oracle为密码，sysdba作为系统dba登入

   ```shell
   show parameter service_name #显示服务名
   alter system set service_names='pdborcl' scope=both; #更改服务名为pdborcl
   ```

2. 服务端更改完成，客户端的连接也要更改`listener.ora`文件，这里不记录

#### 新建用户并导入dmp文件初始数据库

1. 通过plsql添加用户manage

   在`user`右键new 新建用户，设置 default tablespace=users，temp tablespace=temp

   role选项卡添加connect、dba、resource

2. ftp上传文件dmp备份文件到挂在目录`/dockerdata/manager/oracleinitdb/initdb`

3. 进入容器执行切换到`/docker-entrypoint-initdb.d`目录`imp manager/manager file=manager20180413am1052.dmp log=imp_sysdb.log grants=no full=y`导入恢复数据

```
create temporary tablespace yuhang_temp 
tempfile 'D:\oracledata\yuhang_temp.dbf' 
size 50m  
autoextend on  
next 50m maxsize 20480m  
extent management local;  
```

#### 问题

1. 导入表空间报错

   解决将`manager20180413am1052.dmp`文件内容中的 `MANAGERDATASPACE`替换`USERS`

   待优化处理：？？？

   ​

