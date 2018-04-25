---
title: JavaEE之单元测试
date: 2017-04-01 02:01:00
updated: 2018-04-25 20:47:32categories: JavaEE
tags: [junit,grade,单元测试]
---
#### 创建工程

Gradle->[Java,Web]->[GroupId:com.xuan,Artifactld:projectName]->[Use auto-import,Creat dir.....lly]

#### 添加测试

选中要测试的->`ctrl+shift+t`

被测试代码

```java
public class JunitHello {
    public String printHello(){
        System.out.printf("hello junit");
        return "hello junit";
    }
}
```

测试代码(目录test/java下有效)

```java
public class JunitHelloTest {
    @Test
    public void printHello() throws Exception {
       JunitHello junitHello=new JunitHello();
        assertEquals(junitHello.printHello(),"hellojunit");
    }
}
```

测试结果

```
hello junit
org.junit.ComparisonFailure: 
Expected :hello junit
Actual   :hellojunit
 <Click to see difference>

	at com.xuan.test.JunitHelloTest.printHello(JunitHelloTest.java:14)
	
Process finished with exit code -1
```

###### 注意

自动导入了junit的包、测试代码只能在\test目录下才能使用，不然招不到junit的包，不需要添加JUnitGenerator V2.0自动生成测试模块插件