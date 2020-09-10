---
title: ubuntu14.04 使用 idea
date: 2017-02-28 09:32:53
updated: 2020-09-09 17:01:13
categories: Tools
tags: [idea,tomcat,Ubuntu]
---
### 常见问题
##### idea配置

idea添加tomcat出现`application server libraries not found`

*原因：* 权限不足

*解决:* sudo chown -R 【用户名】 【tomcat目录】

