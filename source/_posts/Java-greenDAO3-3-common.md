---
title: greenDAO3.1框架（三）常用注解
date: 2016-08-27 10:33:45
updated: 2018-01-28 21:41:27categories: greenDAO
tags: [greenDAO,ORM]
---
### 类注解
>* *@Entity* 标记了一个Java类作为一个greenDAO实体
```java
@Entity
public class Test {
...
}
```

### 基本属性注解
>* *@Id* 必须是long类型，在数据库作为主键，参数autoincrement是否自增
```java
@Id(autoincrement = true)
private Long id;
```

>* *@Property* 指定改字段的列名，如果不指定将使用默认值（eg:customName对应数据库列名为CUSTOM_NAME）
```java
@Property(nameInDb = "USER_NAME")
private String customName;
```

>* *@Transient* 这个属性将不会作为数据表中的一个字段
```java
@Transient
private int tempUsageCount;
```

>* *@NotNull* 该字段不能为null（作用于long, int, short, byte类型）
```java
@NotNull
private int repos;
```

>* *@Index* 索引(unique唯一)
```java
 @Index(unique = true)
 private String name;
```

>* *@Unique* 添加唯一键（隐含为其创建了一个索引）
```java
@Unique private String name;
```

# 问题
知识点：int 是基本类型，直接存数值，而integer是对象，用一个引用指向这个对象
问题描述：在实体类用int等基本类型，默认不标记注解，在建数据库也会全部设置NOT NULL
解决：因此需要在实体类里写对象类型。
2016-11-29 16:18:24 发现使用中文字段名默认生成为ANSI,出现乱码，尽量使用因为的字段别名


