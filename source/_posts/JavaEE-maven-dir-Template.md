---
title: idea ssm 目录结构
date: 2017-05-04 17:16:28
updated: 2018-12-12 10:47:58
categories: JavaEE
tags: [JavaEE,idea,maven]

---

### 项目基本目录结构

| 项目根/               | 说明                   | Mark as         |
| :----------------- | -------------------- | --------------- |
| pom.iml            | 项目资源目录配置文件[^可视化配置界面] | `自动生成`          |
| src/main/java      | 源代码目录，存放java代码       | Sources         |
| src/main/resources | 配置（资源）文件存放目录         | Resources       |
| src/main/webapp    | 存放静态网页目录             | web目录[^web目录设置] |
| src/test/java      | 测试代码目录               | Tests           |
| src/test/resources | 测试配置（资源）文件目录         | Tests Resources |
| target/            | 输出根目录                | Excluded        |

[^可视化配置界面]: 在`Project Structure`->`Modules`->`Sources`
[^web目录设置]: 在`Project Structure`->`Modules`->`项目名`->`Web`->`配置xml的位置和web的目录和保护的资源目录`

### 项目额外目录结构

| 项目根/                | 说明                                       | Mark as |
| ------------------- | ---------------------------------------- | ------- |
| src/site            | 与site相关资源目录                              |         |
| src/main/filters    | 资源过滤文件目录                                 |         |
| src/main/assembly   | Assembly descriptors                     |         |
| src/mian/config     | 配置文件目录                                   |         |
| src/main/scripts    | Application/Library scripts              |         |
| src/test/filters    | 测试资源过滤文件目录                               |         |
| target/classes      | 项目主体输出目录                                 |         |
| target/test-calsses | 项目测试输出目录                                 |         |
| target/site         | 项目site输出目录                               |         |
| LICENSE.md          | 项目license                                |         |
| NOTICE.md           | Notices and attributions required by libraries that the project depends on |         |
| README.md           | 项目readme                                 |         |

##### 子项目打包

`clean package -pl module_name -am `

-am --also-make 同时构建所列模块的依赖模块； 

-amd -also-make-dependents 同时构建依赖于所列模块的模块；

 -pl --projects <arg> 构建制定的模块，模块间用逗号分隔；

 -rf -resume-from <arg> 从指定的模块恢复反应堆。 



##### 参考：

[7天学会Maven（第二天——Maven 标准目录结构）](http://www.cnblogs.com/haippy/archive/2012/07/05/2577233.html)

