---
title: Git-repo
date: 2019-12-18 10:17:39
updated: 2019-12-19 14:37:59
categories: Git
tags: [git,repo]
---

## git多项目管理方案

* [Git-submodule](https://git-scm.com/docs/git-submodule)
* [Gitslave](http://gitslave.sourceforge.net/)
* [Git-subtree](https://github.com/apenwarr/git-subtree/)
* [Git-repo](https://gerrit.googlesource.com/git-repo/) 采用(原因安卓几百个子项目都采用它)

### git-repo 多项目管理

#### [安装](https://storage.googleapis.com/git-repo-downloads/repo)

```bash
# Debian/Ubuntu. 系统
$ sudo apt-get install repo
# Gentoo. 系统
$ sudo emerge dev-vcs/repo
# 其他系统下载脚本
curl https://storage.googleapis.com/git-repo-downloads/repo
# 添加执行权限
chmod a+rx repo
# 需要全局执行命令根据自己的系统进行配置环境变量,也可以放进项目里面，再项目里面运行
# mac 安装
mv repo /usr/local/bin
```

#### [使用](https://source.android.com/source/using-repo.html)

```bash
# 修改repo文件里面的地址，不然需要外网
#  REPO_URL = 'https://gerrit.googlesource.com/git-repo'
   REPO_URL = 'https://mirrors.ustc.edu.cn/aosp/git-repo'
# 也可以使用环境变量，或者使用命令时代参数
repo init --repo-url=https://gerrit-google.tuna.tsinghua.edu.cn/git-repo
```

##### repo init

```bash
./repo init -u your_project_git_url
./repo init -u git@github.com:xuanfong1/springLeaning.git
#----------------------可选参数-----------------------------------------
#-b 选取的 manifest 仓库分支，默认 master
#-m 选取的默认配置文件，默认 default.xml
#--depth=1 git clone 的深度，一般如在 Jenkins 上打包时可用，加快代码 clone 速度
#--repo-url=URL 使用自定义的 git-repo 代码，如前面说到的 fix 了 bug 的 git-repo
#--no-repo-verify 不验证 repo 的源码，如果自定义了 repo url 那么这个一般也加上
#----------------------------------------------------------------------
```





