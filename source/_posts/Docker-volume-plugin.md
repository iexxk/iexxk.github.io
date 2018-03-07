---
title: Docker-volume-plugin
date: 2018-03-04 22:30:39
updated: 2018-03-07 17:58:47
categories: Docker
tags: [Docker,volume]
---

### docker 卷插件

[官方插件列表](https://docs.docker.com/engine/extend/legacy_plugins/#volume-plugins)

[官方插件商店](https://store.docker.com/search?category=volume&q=&type=plugin)

#### [rancher/convoy](https://github.com/rancher/convoy)

主要功能快照、备份、还原

总结：适用于单节点，单主机，的本地卷管理

#### [calavera/**docker-volume-glusterfs**](https://github.com/calavera/docker-volume-glusterfs)

看[centos7 安装 GlusterFS]()

#### [Pure Storage Docker Volume Plugin](https://store.docker.com/plugins/pure-docker-volume-plugin?tab=description)

#### [Hedvig Docker Volume Plugin](https://store.docker.com/plugins/hedvig-docker-volume-plugin)

依赖于hedvig cluster

#### [REX-Ray](https://rexray.readthedocs.io/en/stable/user-guide/schedulers/docker/plug-ins/)

github: [rexray/rexray](https://github.com/rexray/rexray)

参考：[每天5分钟玩转 OpenStack **Rex-Ray**](https://www.ibm.com/developerworks/community/blogs/132cfa78-44b0-4376-85d0-d3096cd30d3f/entry/Swarm_%E5%A6%82%E4%BD%95%E5%AD%98%E5%82%A8%E6%95%B0%E6%8D%AE_%E6%AF%8F%E5%A4%A95%E5%88%86%E9%92%9F%E7%8E%A9%E8%BD%AC_Docker_%E5%AE%B9%E5%99%A8%E6%8A%80%E6%9C%AF_103?lang=en)

...........居然没找到一个合适的提供者

[rexray/cis-nfs](https://github.com/rexray/csi-nfs)  待测试，NFS似乎不满足需求