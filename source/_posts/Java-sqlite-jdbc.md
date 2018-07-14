---
title: Java-sqlite-jdbc
date: 2018-07-13 16:29:56
updated: 2018-07-13 16:53:14
categories: Java
tags: [Java,Sqlite]
---

#### java读取sqlit db文件

首先在`pom.xml`引入依赖包

```xml
<!-- https://mvnrepository.com/artifact/org.xerial/sqlite-jdbc -->
<dependency>
    <groupId>org.xerial</groupId>
    <artifactId>sqlite-jdbc</artifactId>
    <version>3.23.1</version>
</dependency>
```



读取数据db

```java
@Before
public void loadDb() {
    try {
        connection = DriverManager.getConnection("jdbc:sqlite:C:\\Users\\Administrator\\Desktop\\data.db");
        System.out.println("连接成功");
    } catch (SQLException e) {
    	e.printStackTrace();
    }
}
```

读取完关闭数据库

```java
@After
public void after() {
    try {
        connection.close();
    } catch (SQLException e) {
        e.printStackTrace();
    }
}
```

单行读取数据

```java
public Map queryMap(String sql) throws SQLException {
    HashMap row = null;
    System.out.print("执行：" + sql);
    ResultSet rs = connection.createStatement().executeQuery(sql);
    if (rs.next()) {
        ResultSetMetaData md = rs.getMetaData();
        int columns = md.getColumnCount();
        row = new HashMap(columns);
        for (int i = 1; i <= columns; ++i) {
            if (i > 1) System.out.print(",  ");
            row.put(md.getColumnName(i), rs.getObject(i));
            System.out.print(rs.getObject(i) + " " + md.getColumnName(i));
        }
    }
    rs.close();
    return row;
}
```

多行读取数据

```java
public List queryList(String sql) throws SQLException {
    System.out.print("执行：" + sql);
    ResultSet rs = connection.createStatement().executeQuery(sql);
    ResultSetMetaData md = rs.getMetaData();
    int columns = md.getColumnCount();
    ArrayList list = new ArrayList(50);
    while (rs.next()) {
        HashMap row = new HashMap(columns);
        for (int i = 1; i <= columns; ++i) {
            if (i > 1) System.out.print(",  ");
            row.put(md.getColumnName(i), rs.getObject(i));
            System.out.print(rs.getObject(i) + " " + md.getColumnName(i));
        }
        list.add(row);
    }
    rs.close();
    return list;
}
```

#### 注意事项

1. `ResultSet`连续查询会覆盖之前的，无论是不是新的`ResultSet`都是共享一个，因此读完数据保存到map马上关闭
2. ` connection.createStatement()`这个对象也不能共享全局，会出现数据库未关闭的错误