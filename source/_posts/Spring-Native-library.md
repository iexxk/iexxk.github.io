---
title: Spring-Native-library
date: 2019-08-31 16:01:36
updated: 2019-08-31 16:21:12
categories: Spring
tags: [Spring]
---

错误1:

```verilog
Exception in thread "main" java.lang.UnsatisfiedLinkError: Unable to load library 'NVSSDK':
libNVSSDK.so: 无法打开共享对象文件: 没有那个文件或目录
libossdk.so: 无法打开共享对象文件: 没有那个文件或目录
Native library (linux-x86-64/libNVSSDK.so) not found in resource path ([file:/opt/bpf/package/term_model/NetCameraCapture/NetCameraCapture-0.0.1-SNAPSHOT.jar])
```

解决

```bash
vi /etc/ld.so.conf
ldconfig
```

