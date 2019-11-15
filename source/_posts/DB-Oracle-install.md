---
title: DB-oracle-install
date: 2018-04-20 12:02:11
updated: 2019-11-15 11:53:24
categories: 数据库
tags: [oracle,sql]
---

## Docker 安装 Oracle

镜像：[sath89/oracle-12c](https://hub.docker.com/r/sath89/oracle-12c/)

挂载需要修改权限

`chown -R 1001:1001 /data/oracle`

docker run -d --name oracle -p 8080:8080 -p 1521:1521  -e TZ=Asia/Shanghai sath89/oracle-12c

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

到处dmp文件：`exp manager/manager buffer=64000 file=/test.dmp full=y`

#### 配置

##### 修改数据库服务名`xe`为`pdborcl`

参考：[Oracle 更改服务名方法](https://www.jianshu.com/p/879e8085c012)

1. 进入容器内执行命令，连接Oracle，执行`sqlplus sys/oracle as sysdba` 进入oracle，其中sys为用户名，oracle为密码，sysdba作为系统dba登入

   ```shell
   show parameter service_name #显示服务名
   alter system set service_names='pdborcl' scope=both; #更改服务名为pdborcl
   ```

2. 添加表空间`MANAGERDATASPACE`

   ```sql
    CREATE TABLESPACE MANAGERDATASPACE
    LOGGING
    DATAFILE '/u01/app/oracle/oradata/xe/MANAGERDATASPACE.DBF'
    SIZE 32M
    AUTOEXTEND ON
    NEXT 32M MAXSIZE UNLIMITED
    EXTENT MANAGEMENT LOCAL;
   ```

3. 服务端更改完成，客户端的连接也要更改`listener.ora`文件，这里不记录

#### 新建用户并导入dmp文件初始数据库

1. 通过plsql添加用户manage

   在`user`右键new 新建用户，设置 default tablespace=users，temp tablespace=temp

   role选项卡添加connect、dba、resource

2. ftp上传文件dmp备份文件到挂在目录`/dockerdata/manager/oracleinitdb/initdb`

3. 进入容器执行切换到`/docker-entrypoint-initdb.d`目录`imp manager/manager file=manager20180413am1052.dmp log=imp_sysdb.log grants=no full=y`导入恢复数据

#### 数据库前的准备工作

```sql
--创建表空间
create tablespace SY_DB logging datafile '/u01/app/oracle/oradata/SY_DB.DBF' size 50m autoextend on next 50m maxsize 20480m extent management local;
--创建用户
create user SY_DB identified by "SY_DB@2018"   default tablespace SY_DB  temporary tablespace TEMP  profile DEFAULT password expire;
-- Grant/Revoke role privileges
grant dba to SY_DB;
--给用户分配权限
grant create any table to SY_DB;
grant create any view to SY_DB;
grant create user to SY_DB;
grant drop tablespace to SY_DB;
grant unlimited tablespace to SY_DB;
--查询用户密码有效期
select * from dba_profiles where profile='DEFAULT' and resource_name='PASSWORD_LIFE_TIME';
--查询用户和密码
select username,password from dba_users;
--修改用户密码（密码里面最好不要有@符号，不然执行导入命令时一直无权限）
alter user SY_DB identified by mimaoracle;
--去除用户密码有效期
ALTER PROFILE DEFAULT LIMIT PASSWORD_LIFE_TIME UNLIMITED;
--创建虚拟目录存储导出文件
create directory db_bak as '/docker-entrypoint-initdb.d';
```

#### 数据库导入导出(容器bash执行)

```bash
--数据泵导入文件
impdp SY_DB/mimaoracle DIRECTORY=db_bak  DUMPFILE=SY_DB20190829.DMP  SCHEMAS=SY_DB
--数据泵导出文件
expdp SY_DB/"""SY_DB@2018"""@orcl DIRECTORY=db_bak  DUMPFILE=SY_DB20190829.DMP  SCHEMAS=SY_DB;
```

#### 修改字符集

```sql
-- 进入sql命令行
sqlplus sys/oracle as sysdba
--若此时数据库服务器已启动，则先执行 SHUTDOWN IMMEDIATE 命令关闭数据库服务器，
然后执行以下命令:
SQL>shutdown immediate
SQL>STARTUP MOUNT
SQL>ALTER SYSTEM ENABLE RESTRICTED SESSION;
SQL>ALTER SYSTEM SET JOB_QUEUE_PROCESSES=0;
SQL>ALTER SYSTEM SET AQ_TM_PROCESSES=0;
SQL>ALTER DATABASE OPEN;
SQL>ALTER DATABASE CHARACTER SET ZHS16GBK;
SQL>ALTER DATABASE CHARACTER SET INTERNAL_USE ZHS16GBK; 
--执行错误,未解决该错误
--ERROR at line 1:
--ORA-12712: new character set must be a superset of old character set
SQL>SHUTDOWN IMMEDIATE
SQL>STARTUP
```



#### 问题

1. 导入表空间报错

   解决将`manager20180413am1052.dmp`文件内容中的 `MANAGERDATASPACE`替换`USERS`

   待优化处理：？？？

   

