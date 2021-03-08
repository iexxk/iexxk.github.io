---
title: 分布式计算
date: 2018-12-10 16:56:57
updated: 2018-12-12 10:47:58
categories: BigData
tags: [DistributedComputing,BigData]
---

## 三大主流分布式计算系统

### Hadoop

Hadoop常用于离线的复杂的[大数据分析](http://www.ethinkbi.com/)处理

Hadoop采用MapReduce分布式计算框架，并根据GFS开发了HDFS分布式文件系统，根据BigTable开发了HBase数据存储系统。

### Spark

Spark常用于离线的快速的大数据处理

Spark使用内存来存储数据

### Storm

Storm常用于在线的实时的大数据处理

Storm不进行数据的收集和存储工作，它直接通过网络实时的接受数据并且实时的处理数据，然后直接通过网络实时的传回结果。







#### 参考

[主流的三大分布式计算系统：Hadoop，Spark和Storm](https://blog.csdn.net/AlbertFly/article/details/78357317)