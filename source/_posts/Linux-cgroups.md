---
title: Linux资源管理之cgroups
date: 2019-08-20 10:10:43
updated: 2019-08-20 10:23:04
categories: Linux
tags: [cgroups]
---

## 简介

cgroups 的全称是control groups，cgroups为每种可以控制的资源定义了一个子系统。docker也是通过该原理进行限制资源。

* cpu 子系统，主要限制进程的 cpu 使用率。
* cpuacct 子系统，可以统计 cgroups 中的进程的 cpu 使用报告。
* cpuset 子系统，可以为 cgroups 中的进程分配单独的 cpu 节点或者内存节点。
* memory 子系统，可以限制进程的 memory 使用量。
* blkio 子系统，可以限制进程的块设备 io。
* devices 子系统，可以控制进程能够访问某些设备。
* net_cls 子系统，可以标记 cgroups 中进程的网络数据包，然后可以使用 tc 模块（traffic control）对数据包进行控制。
* freezer 子系统，可以挂起或者恢复 cgroups 中的进程。
* ns 子系统，可以使不同 cgroups 下面的进程使用不同的 namespace。

## 安装







## 参考

[Linux资源管理之cgroups简介](https://tech.meituan.com/2015/03/31/cgroups.html)