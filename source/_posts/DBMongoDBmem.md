---
title: mongoDB内存
date: 2019-08-20 11:37:52
updated: 2019-08-22 18:10:40
categories: 数据库
tags: [mongoDB]
---

## 常用命令

```bash
#查看mongo内存使用命令
mongostat
---------------------------------------------------------------------------------------
insert query update delete getmore command dirty  used flushes vsize   res qrw arw net_in net_out conn                time
     2    10      4     *0       0     3|0  0.1% 80.0%       0 8.98G 7.85G 0|0 5|0  10.8k   68.6k   30 Aug 20 11:51:55.367
    *0    *0     *0     *0       0     2|0  0.1% 80.0%       0 8.98G 7.85G 0|0 5|0   212b   62.0k   29 Aug 20 11:51:56.368
     2    10      4     *0       0     2|0  0.1% 80.0%       0 8.98G 7.86G 0|0 5|0  10.8k   68.2k   29 Aug 20 11:51:57.367
    *0     3      1     *0       0     2|0  0.1% 80.0%       0 8.98G 7.86G 0|0 5|0  5.38k   65.1k   29 Aug 20 11:51:58.367
    *0    *0     *0     *0       0     1|0  0.1% 80.0%       0 8.98G 7.86G 0|0 5|0   157b   61.8k   29 Aug 20 11:51:59.368
--------------------------------------------------------------
```



[WiredTiger存储引擎](https://docs.mongodb.com/manual/core/wiredtiger/)

wiredTiger对内存使用会分为两大部分，一部分是内部内存，另外一部分是文件系统的缓存。内部内存默认值有一个计算公式{ 50% of(RAM-1GB) ,or256MB }，索引和集合的内存都被加载到内部内存，索引是被压缩的放在内部内存，集合则没有压缩。wiredTiger会通过文件系统缓存，自动使用其他所有的空闲内存，放在文件系统缓存里面的数据，与磁盘上的数据格式一致，可以有效减少磁盘I/O。

mongodb不干涉内存管理，将内存管理工作交给操作系统去处理。在使用时必须随时监测内存使用情况，因为mongodb会把所有能用的内存都用完。

```bash
For example, on a system with a total of 4GB of RAM the WiredTiger cache will use 1.5GB of RAM (0.5 * (4 GB - 1 GB) = 1.5 GB). Conversely, a system with a total of 1.25 GB of RAM will allocate 256 MB to the WiredTiger cache because that is more than half of the total RAM minus one gigabyte (0.5 * (1.25 GB - 1 GB) = 128 MB < 256 MB).

NOTE

In some instances, such as when running in a container, the database can have memory constraints that are lower than the total system memory. In such instances, this memory limit, rather than the total system memory, is used as the maximum RAM available.

To see the memory limit, see hostInfo.system.memLimitMB.

By default, WiredTiger uses Snappy block compression for all collections and prefix compression for all indexes. Compression defaults are configurable at a global level and can also be set on a per-collection and per-index basis during collection and index creation.

Different representations are used for data in the WiredTiger internal cache versus the on-disk format:

Data in the filesystem cache is the same as the on-disk format, including benefits of any compression for data files. The filesystem cache is used by the operating system to reduce disk I/O.
Indexes loaded in the WiredTiger internal cache have a different data representation to the on-disk format, but can still take advantage of index prefix compression to reduce RAM usage. Index prefix compression deduplicates common prefixes from indexed fields.
Collection data in the WiredTiger internal cache is uncompressed and uses a different representation from the on-disk format. Block compression can provide significant on-disk storage savings, but data must be uncompressed to be manipulated by the server.
Via the filesystem cache, MongoDB automatically uses all free memory that is not used by the WiredTiger cache or by other processes.
```





## 参考

[mongodb——内存](https://www.jianshu.com/p/0e1f214d512c)

