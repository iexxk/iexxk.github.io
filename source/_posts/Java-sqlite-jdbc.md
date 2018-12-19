---
title: Java-sqlite-jdbc
date: 2018-07-13 16:29:56
updated: 2018-12-12 10:47:58
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

3. 问题，该驱动目前好像不支持alpine系统，因此用docker打包式，基础镜像用alpine会加载不了驱动

   ```verilog
   [WARN]: Failed to load native library:sqlite-3.15.1-6f7bc1af-1dba-4675-84c7-aaf90017dff0-libsqlitejdbc.so. osinfo: Linux/x86_64
   [WARN]: java.lang.UnsatisfiedLinkError: /tmp/sqlite-3.15.1-6f7bc1af-1dba-4675-84c7-aaf90017dff0-libsqlitejdbc.so: Error relocating /tmp/sqlite-3.15.1-6f7bc1af-1dba-4675-84c7-aaf90017dff0-libsqlitejdbc.so: __isnan: symbol not found
   ```

   解决：替换基础镜像，这里用`java:8-jre`他的基础系统是`debian `

   参考: [Failed to load native library:sqlite-3.15.1](https://github.com/itzg/dockerfiles/issues/133)

   解决：居然是版本问题，换成`3.8.11.2`可以读取

### 测试

利用docker镜像测试jdbc驱动包

准备测试代码`SQLiteJDBC.java`

```java
import java.sql.*;

public class SQLiteJDBC
{
  public static void main( String args[] )
  {
    Connection c = null;
    try {
      Class.forName("org.sqlite.JDBC");
      c = DriverManager.getConnection("jdbc:sqlite:test.db");
    } catch ( Exception e ) {
      System.err.println( e.getClass().getName() + ": " + e.getMessage() );
      System.exit(0);
    }
    System.out.println("Opened database successfully");
  }
}
```

然后准备好db测试数据库文件、`SQLiteJDBC.java`测试代码文件、[sqlit-jdbc驱动包](https://bitbucket.org/xerial/sqlite-jdbc/downloads/):[sqlite-jdbc-3.8.11.2.jar](https://bitbucket.org/xerial/sqlite-jdbc/downloads/sqlite-jdbc-3.8.11.2.jar) 这几个文件都放在同一个目录，然后切合到该目录执行以下命令

```bash
#编译生成class文件
docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp java:8-jdk-alpine javac SQLiteJDBC.java
#运行class文件
docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp java:8-jdk-alpine java -classpath ".:sqlite-jdbc-3.8.11.2.jar" SQLiteJDBC
```

`docker run --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp <java镜像名字> <java命令>`该命令意思是当前挂载当前路径到myapp目录，`--rm` 是一次性，用完即毁

   

