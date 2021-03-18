---
title: Git常用操作
date: 2018-08-07 14:34:06
updated: 2021-03-18 18:23:07
categories: Tools
tags: [git]
---

## 回滚

#### 回退` reset` (未push)

* --soft  保留源码,只回退到commit 信息到某个版本.不涉及index的回退,如果还需要提交,直接commit即可.
* --hard 源码也会回退到某个版本,commit和index 都回回退到某个版本.(注意,这种方式是改变本地代码仓库源码) 
* --mixed 会保留源码,只是将git commit和index 信息回退到了某个版本.

[![62oLTK.png](https://s3.ax1x.com/2021/03/18/62oLTK.png)](https://imgtu.com/i/62oLTK)

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

## 初始化工程

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

## 分支覆盖

属于分支回滚的一部分

#### idea操作

idea操作，切换到被覆盖的分支，然后在git->log里面找到需要覆盖到本分支的提交，然后右键点击Reset Current Branch to Here,在弹出的选项里面选择hard

#### 命令操作

```bash
#切换到被覆盖的分支(master),然后执行
git reset --hard origin/test
#然后推送就行了，到此test分支内容就完全替换了master分支了
git push -f
```

## [分支归档](https://stackoverflow.com/questions/1307114/how-can-i-archive-git-branches)

分支归档主要用于，分支太多，想删除，但是又怕以后会用到，因此就可以使用归档

```bash
#deploy150换成你要归档的分支名
#----------------------------------归档--------------------------------------
#切换到要归档的分支
git checkout deploy150 
#给当前分支打标签，标签规范archive/>分支名>,archive归档的意思，也就是创建一个归档标签，-m注释参数可选
git tag archive/deploy150 deploy150 -m "deploy150分支备份归档"
#切出要归档的分支，这里随便切换一个分支出去
git checkout master
#删除要归档的分支，之所以要切换出去，因为不能在要删除的分支上删除自己
git branch -D deploy150
#删除要归档的远程分支
git branch -d -r origin/deploy150 
#推送归档的标签
git push --tags 
#推送删除的分支记录，用于删除服务端的分支
git push origin :deploy150 
#---------------------------------恢复---------------------------------------
#从备份标签恢复到分支，并切换到该分支上，这里恢复只是恢复本地，要恢复服务器push就可以了
git checkout -b deploy150 archive/deploy150
```

## 标签删除

```bash
#删除本地，本地没有也可以执行删除，test1是tag名字，要删除指定tag，替换成自己的就行
git tag -d test1
#推送删除服务器上面的
git push origin :refs/tags/test1
```

## 常见问题

1. idea使用git导入项目时提示`ssh variant 'simple' does not support setting port`

   解决：执行`git config --global ssh.variant ssh`，详细见[fatal: ssh variant 'simple' does not support setting port](https://stackoverflow.com/questions/48417505/fatal-ssh-variant-simple-does-not-support-setting-port)



##### 参考

[git reset revert 回退回滚取消提交返回上一版本](http://yijiebuyi.com/blog/8f985d539566d0bf3b804df6be4e0c90.html)