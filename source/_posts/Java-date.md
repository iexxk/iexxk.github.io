---
title: Java 日期总结
date: 2018-04-05 00:11:33
updated: 2018-04-05 00:17:01
categories: Java
tags: [Java,Date]
---

### java 日期操作

```Java
//java8
LocalDateTime today_start = LocalDateTime.of(LocalDate.now(), LocalTime.MIN);//当天零点
LocalDateTime today_start = LocalDateTime.of(LocalDate.now(), LocalTime.MAX);//当天23:59:59
today_start.format(DateTimeFormatter.ofPattern("yyyyMMddHHmmss")); //时间格式化
//LocalDateTime 转 Date
Date out = Date.from(today_start.atZone(ZoneId.systemDefault()).toInstant()); 
SimpleDateFormat sdf = new SimpleDateFormat("yyyyMMddHHmmss");
sdf.format(out);  //时间格式化
```

