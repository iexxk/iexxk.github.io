---
title: Java-Type
date: 2018-05-29 14:39:59
updated: 2018-05-29 14:39:59
categories: Java
tags: [Java,Type]
---

type泛型解析

```java
Map<String, Integer> map;

type.getRawType();   //返回Map
type.getActualTypeArguments()[0];  //返回string
type.getActualTypeArguments()[1];  //返回Integer
```





参考：

https://github.com/jeasonlzy/okhttp-OkGo/wiki/JsonCallback