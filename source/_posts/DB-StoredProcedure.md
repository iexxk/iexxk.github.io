---
title: DB-StoredProcedure
date: 2018-04-07 21:44:21
updated: 2018-04-25 20:41:28
categories: 数据库
tags: [mysql,DB]
---

## mysql存储过程

### 变量

##### 系统变量`两个@@`

```Mysql
show variables; #查看系统内置变量
select @@变量名; #查看系统变量的值，如select @@version
set 变量名 = 值; #修改变量（局部修改）命令 如set autocommit = 3;
```

##### 自定义变量`一个@`

```mysql
set @变量名 = 值; #自定义变量语法，如`set @name = 'saboran';
select @name; #查看变量的值
```

### 函数

```mysql
create function 函数名(参数列表) returns 数据类型
    begin
        // 函数体 
        // 返回值
    end
```

