---
title: Linux之RPM打包
date: 2019-05-14 14:26:35
updated: 2019-06-03 13:51:28
categories: Linux 
tags: [RPM]
---

## 理论基础

##### 目录结构解释

1. BUILD是编译rpm包的临时目录
2. BUILDROOT是最后生成rpm包的临时安装目录
3. RPMS存放最终生成的rpm二进制包
4. SOURCES是源代码(.tar.gz)存放目录
5. SPECS用来存放spec文件
6. SRPMS存放最终生成的rpm源码包

##### spec文件标签解释

```bash
# 安装包名
Name: 
#版本号
Version: 1.0.0
Release:        1%{?dist}
#简介
Summary: This is pragram printf hell world hahah
#分组，可去掉
Group: Development/Tools
#协议
License: GPL
#资源路径(源代码路径)
Source0: %{name}-%{version}.tar.gz
#安装依赖
Requires: vim
#详细描述
%description
#编译前准备
%prep
%setup -q #自动解压？
#编译
%build
#安装
%install
mkdir -p $RPM_BUILD_ROOT/usr/bin
cp $RPM_BUILD_DIR/%{name}-%{version}/hello-world $RPM_BUILD_ROOT/usr/bin
#删除临时构建目录
%clean
rm -rf $RPM_BUILD_ROOT
#收集文件
%files
%doc
/usr/bin/hello-world

%changelog
```

## 实战hello-world

1. 安装制作工具`yum -y install rpmdevtools`会自动依赖安装`rpm-build`

2. 生成开发目录`rpmdev-setuptree`会在`~`目录生成`rpmbuild`文件目录

   ```bash
   `-- rpmbuild
       |-- BUILD
       |-- RPMS
       |-- SOURCES
       |-- SPECS
       `-- SRPMS
   ```

3. 创建源代码

   ```bash
   ~> mkdir -p rpmbuild/SOURCES/hello-world-1.0.0
   ~> cd rpmbuild/SOURCES/hello-world-1.0.0/
   hello-world-1.0.0> vim hello-world
   #hello-world文件内容如下，就是一个简单的输出hello world的脚本
   #!/bin/sh
   echo Hello World hahah
   #-----------------------------------------------------
   hello-world-1.0.0> chmod 755 hello-world
   hello-world-1.0.0> ./hello-world #测试脚本打印Hello World hahah
   ```

4. 打包源码`tar zcvf hello-world-1.0.0.tar.gz hello-world-1.0.0`

5. 编写spec文件`cd ~/rpmbuild/SPECS`然后`vim hello-world.spec`创建`hello-world.spec`文件，vim会自动根据后缀spec加载默认模版，修改模版如下

   ```bash
   Name: hello-world
   Version: 1.0.0
   Release:        1%{?dist}
   Summary: This is pragram printf hell world hahah
   
   Group: Development/Tools
   License: GPL
   Source0: %{name}-%{version}.tar.gz
   
   %description
   
   %prep
   %setup -q
   
   %build
   
   %install
   mkdir -p $RPM_BUILD_ROOT/usr/bin
   cp $RPM_BUILD_DIR/%{name}-%{version}/hello-world $RPM_BUILD_ROOT/usr/bin
   
   %clean
   rm -rf $RPM_BUILD_ROOT
   %files
   %doc
   /usr/bin/hello-world
   
   %changelog
   ```

6. 执行`rpmbuild -ba hello-world.spec`进行打包最后目录结构

   ```bash
   .
   |-- BUILD
   |   `-- hello-world-1.0.0
   |       |-- debugfiles.list
   |       |-- debuglinks.list
   |       |-- debugsources.list
   |       |-- elfbins.list
   |       `-- hello-world
   |-- BUILDROOT
   |-- RPMS
   |   `-- x86_64
   |       |-- hello-world-1.0.0-1.el7.x86_64.rpm
   |       `-- hello-world-debuginfo-1.0.0-1.el7.x86_64.rpm
   |-- SOURCES
   |   |-- hello-world-1.0.0
   |   |   `-- hello-world
   |   `-- hello-world-1.0.0.tar.gz
   |-- SPECS
   |   `-- hello-world.spec
   `-- SRPMS
       `-- hello-world-1.0.0-1.el7.src.rpm
   ```

7. 安装打包好的安装包`yum install ~/rpmbuild/RPMS/x86_64/hello-world-1.0.0-1.el7.x86_64.rpm`

8. 测试

   ```bash
   > hello-world
   Hello World hahah
   > yum remove hello-world #卸载刚刚安装的
   ```

## 创建本地yum源

1. 新建添加本地源`vim /etc/yum.repos.d/CentOS-Media.repo`，内容如下

   ```yaml
   [c7-media]
   name=CentOS-$releasever - Media
   baseurl=file:///root/nantianrepo/
   gpgcheck=0
   enabled=1
   gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
   ```

2. 安装`yum install createrepo`

3. 新建仓库目录结构，然后放入需要的安装包，及依赖包

   ```bash
   `-- ntrepo
       |-- CentOS-Local.rpeo
       `-- packages
           |-- CodeMeter-lite-6.50.2631-502.x86_64.rpm
           `-- hello-world-1.0.0-1.el7.x86_64.rpm
   ```

4. 在ntrepo目录执行`createrepo .`会生成多一个目录,以及包的索引

   ```bash
   `-- nantianrepo
       |-- CentOS-Local.rpeo
       |-- packages
       |   |-- CodeMeter-lite-6.50.2631-502.x86_64.rpm
       |   `-- hello-world-1.0.0-1.el7.x86_64.rpm
       `-- repodata
           |-- 14a98942df6d04-other.xml.gz
           |-- 16b2285eb13334fe6-filelists.xml.gz
           |-- 839450f23accab4617-primary.sqlite.bz2
           |-- 8e84312460f2957b7c3-other.sqlite.bz2
           |-- a2596c92ad4f0c5750156f-filelists.sqlite.bz2
           |-- d4e9d532b7bf9a0c2af-primary.xml.gz
           `-- repomd.xml
   ```

5. 然后执行`yum clean all`清理缓存

6. 最后测试安装`yum install hello-world`会自动依赖

## 下载rpm依赖包

1. 安装`yum ``install` `yum-plugin-downloadonly`

2. 下载依赖包`yum install –downloadonly –downloaddir= <依赖包存储路径> <需要下载依赖包的安装包名>`例如：

   ```bash
   yum install --downloadonly --downloaddir=/data/rpm  mongodb
   ```

### 常见问题

1. 错误信息分析，关键信息`cd jdk-8u77-linux-x64-1.0.0`

   ```bash
   执行(%prep): /bin/sh -e /var/tmp/rpm-tmp.QO57WH
   + umask 022
   + cd /root/rpmbuild/BUILD
   + cd /root/rpmbuild/BUILD
   + rm -rf jdk-8u77-linux-x64-1.0.0
   + /usr/bin/gzip -dc /root/rpmbuild/SOURCES/jdk-8u77-linux-x64-1.0.0.tar.gz
   + /usr/bin/tar -xf -
   + STATUS=0
   + '[' 0 -ne 0 ']'
   + cd jdk-8u77-linux-x64-1.0.0
   /var/tmp/rpm-tmp.QO57WH: line 35: cd: jdk-8u77-linux-x64-1.0.0: No such file or directory
   错误：/var/tmp/rpm-tmp.QO57WH (%prep) 退出状态不好
   ```

   原因，是因为解压之后路径找不到对应目录

   解决：

   1. 方式一手动解压，重新手动压缩

   2. 方式二修改spec文件中的prep，然后查看BUILD里面的实际解压目录`/root/rpmbuild/BUILD/jdk1.8.0_77`然后设置为实际目录即可

      ```properties
      %prep
      %setup -n jdk1.8.0_77
      ```

2. 编译后无法运行提示无架构

   ```bash
   [root@xuan SRPMS]# yum install jdk-1.8-77.src.rpm
   已加载插件：fastestmirror
   正在检查 jdk-1.8-77.src.rpm: jdk-1.8-77.src
   无法添加软件包 jdk-1.8-77.src.rpm 至操作中。不属于任何可兼容的架构：src
   错误：无须任何处理
   ```

   解决：


### 参考

[制作一个简单的rpm包:helloworld](https://wangbin.io/blog/it/yum-rpm-make.html)

[RPM 包制作](https://jin-yang.github.io/post/linux-create-rpm-package.html)

[rpmbuild SPEC文件说明]([http://abcdxyzk.github.io/blog/2014/02/10/rpm-rpmbuild-base/](http://abcdxyzk.github.io/blog/2014/02/10/rpm-rpmbuild-base/))

https://blog.csdn.net/wl_fln/article/details/7263668