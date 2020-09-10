---
title: git创建空白分支
date: 2017-12-07 16:43:37
updated: 2020-09-09 17:01:50
categories: Tools
tags: [git,分支]
---
### 场景需求

有时需要新建一个完全独立的空白分支，作为资源存储等，例如hexo博客源码

#### 解决

````shell
git clone git@xxxxxxxxx.git #克隆项目到本地，需要提前配置号ssh key等权限
git checkout --orphan <新的分支名> #创建新的空白分支
#如果提示error: The following untracked working tree files would be overwritten by checkout:
git clean -d -fx #会清除所有git clone下的所有文件，只剩.git
#然后重新执行
git checkout --orphan <新的分支名> #会提示一下unable to create,无视，只要分支名改变就算成功
git rm -rf . #清除所有git文件历史，为了空白分支
git commit -m "提交信息"
git push origin <新的分支名> #推送远程分支
#提示该错误error: src refspec hexo does not match any.
#解决因为不能提交空分支，重新添加文件，提交分支
git add README.md
git commit -m "提交信息"
git push origin <新的分支名> #推送远程分支
````

