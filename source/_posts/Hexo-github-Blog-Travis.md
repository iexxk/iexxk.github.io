---
title: github博客之Travis自动部署Hexo
date: 2017-12-07 18:16:37
updated: 2018-12-12 10:47:58categories: 杂谈
tags: [github,hexo,Travis]
---

### 自动部署原理流程

```mermaid
graph LR
O[本地新增博客文件] --> |git push|A[github:hexo分支] 
A --> |hexo编译源码|B[Travis CI编译]
B --> |静态网页文件 git push|C[github:master分支]
C --> D(博客显示)
```



### 搭建步骤

#### 流程



1. 注册[Travis CI](https://travis-ci.org/)
2. github生成access token
3. 在travis同步项目，以及配置token
4. github添加空白分支
5. 在空白分支里放入Hexo源码
6. 添加Travis CI配置文件
7. 注意Hexo源码里theme文件里面的过滤文件删掉，不然会上传不了主题，造成博客空白
8. 然后push到新建的空白分支

#### 资源

hexo编译源码地址：https://github.com/xuanfong1/xuanfong1.github.io/tree/hexo

静态网页生产文件地址：https://github.com/xuanfong1/xuanfong1.github.io/tree/master

### 参考

[使用 Travis CI 自动部署 Hexo](http://www.jianshu.com/p/5e74046e7a0f)