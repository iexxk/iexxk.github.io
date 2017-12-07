---
title: JavaEE之Oracle搭建
date: 2017-07-17 23:34:28
categories: SQL
tags: [sql,环境搭建]
---

### 环境安装

1. 下载[Oracle](http://www.oracle.com/technetwork/database/enterprise-edition/downloads/index.html) 12c(Enterprise),总共两个文件（File1，File2），可右键复制链接迅雷下载


2. 两个文件都解压

3. 双击`setup.exe`运行

   注：解决`[INS-30131]`错误：计算机管理添加C盘共享，权限设置为管理员完全权限，其他用户可读。

4. 安装选项

   - [x] 创建配置数据库

   - [x] 桌面类
   - [x] 创建新windos用户(root,xuanxuan)
   - [x] 输入口令(数据库名orcl.lan;口令Mimais163)
   - [x] 弹窗口令管理修改 sys(mimais163R)system(mimais163A)

   ​

#### 参考:

[Oracle Database 12c安装教程(Windows版)](http://www.jianshu.com/p/9d9f978630be)

[Oracle 12c Windows安装、介绍及简单使用(图文)](http://blog.csdn.net/anxpp/article/details/51345074)

