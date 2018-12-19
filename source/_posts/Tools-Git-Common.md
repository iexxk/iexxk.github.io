---
title: Git常用操作
date: 2018-08-07 14:34:06
updated: 2018-12-12 14:28:30
categories: 工具
tags: [git]
---

#### 回退` reset` (未push)

* --soft  保留源码,只回退到commit 信息到某个版本.不涉及index的回退,如果还需要提交,直接commit即可.
* --hard 源码也会回退到某个版本,commit和index 都回回退到某个版本.(注意,这种方式是改变本地代码仓库源码) 
* --mixed 会保留源码,只是将git commit和index 信息回退到了某个版本.

![](https://raw.githubusercontent.com/xuanfong1/xuanfong1.github.io/master/image/src_dir/1533623741056.png)

#### 回退`revert`(已push)

git revert用于反转提交,执行evert命令时要求工作树必须是干净的. 

git revert用一个新提交来消除一个历史提交所做的任何修改.

revert 之后你的本地代码会回滚到指定的历史版本,这时你再 git push 既可以把线上的代码更新.(这里不会像reset造成冲突的问题)

```sh
git revert c011eb3c20ba6fb38cc94fe5a8dda366a3990c61
```



## 清除已提交内容，解决.gitignore无效

添加.gitignore执行如下

```bash
git rm -r --cached .
git add .
git commit -m 'clear track'
```



### 部署合并远程分支

```bash

```



### 初始化工程

##### Git global setup

```
git config --global user.name "liangxuan"
git config --global user.email "liangx@3sreform.com"
```

##### Create a new repository

```
git clone ssh://git@192.168.1.230:14020/xuan/test.git
cd test
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

##### Existing folder

```
cd existing_folder
git init
git remote add origin ssh://git@192.168.1.230:14020/xuan/test.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

##### Existing Git repository

```
cd existing_repo
git remote rename origin old-origin
git remote add origin ssh://git@192.168.1.230:14020/xuan/test.git
git push -u origin --all
git push -u origin --tags
```





##### 参考

[git reset revert 回退回滚取消提交返回上一版本](http://yijiebuyi.com/blog/8f985d539566d0bf3b804df6be4e0c90.html)