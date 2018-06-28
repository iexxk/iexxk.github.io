---
title: Mybatis 使用
date: 2017-12-14 16:26:28
updated: 2018-03-30 13:56:16
categories: JavaEE
tags: [java,Mybatis]
typora-copy-images-to: image\src_dir
---

## 自动生成代码

### maven形式

1. 在`pom.xml`添加依赖

   ```xml
   <dependencies>
   	...
       <!--Mybatis Mapper代码生成用-->
       <dependency>
           <groupId>org.mybatis.generator</groupId>
           <artifactId>mybatis-generator-core</artifactId>
           <version>1.3.6</version>
       </dependency>
       ...
   </dependencies>
   ```

2. 在`pom.xml`添加插件

   ```xml
   <plugins>
       <!--mybatis生成代码插件-->
       <plugin>
           <groupId>org.mybatis.generator</groupId>
           <artifactId>mybatis-generator-maven-plugin</artifactId>
           <version>1.3.6</version>
           <!--指定配置文件路径-->
           <configuration>
           <overwrite>true</overwrite>
           <configurationFile>path/generactorConfig.xml</configurationFile>
           </configuration>
       </plugin>
   </plugins>
   ```

3. 配置`generactorConfig.xml`文件,改配置来源[Mybatis系列—Mybatis插件使用（自动生成Mapper，分页）](https://juejin.im/entry/5aabc4036fb9a028e11fb726)

   ```xml
   <?xml version="1.0" encoding="UTF-8" ?>
   <!DOCTYPE generatorConfiguration PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN" "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd" >
   <generatorConfiguration>
       <!-- 指定oracle/mysql的驱动包的路径 千万别放中文路径下 -->
       <classPathEntry location="C://Users//Administrator//.DataGrip2018.1//config//jdbc-drivers//MySQL Connector//J//5.1.46//mysql-connector-java-5.1.46.jar"/>
       <!-- 配置数据源和生成的代码所存放的位置 -->
       <context id="testTable" targetRuntime="MyBatis3Simple">
           <!--设置生成的Java文件的编码格式-->
           <property name="javaFileEncoding" value="UTF-8"></property>
           <!--格式化java代码-->
           <property name="javaFormatter" value="org.mybatis.generator.api.dom.DefaultJavaFormatter"></property>
           <!--格式化xml代码-->
           <property name="xmlFormatter" value="org.mybatis.generator.api.dom.DefaultXmlFormatter"></property>
           <!--javaBean 实现序列化接口-->
           <plugin type="org.mybatis.generator.plugins.SerializablePlugin"></plugin>
           <!--javaBean生成toString() 方法-->
           <plugin type="org.mybatis.generator.plugins.ToStringPlugin" />
           <commentGenerator>
               <!--生成代码时，是否生成注释  true：不  false：是-->
               <property name="suppressAllComments" value="true"></property>
           </commentGenerator>
           <!--数据库配置-->
           <jdbcConnection driverClass="com.mysql.jdbc.Driver" connectionURL="jdbc:mysql://192.168.204.182:3306/manage?useUnicode=true&amp;characterEncoding=UTF-8&amp;zeroDateTimeBehavior=convertToNull&amp;serverTimezone=UTC" userId="root" password="lfadmin"></jdbcConnection>
           <!--
               java类型处理器
                 用于处理DB中的类型到Java中的类型，默认使用JavaTypeResolverDefaultImpl；
                  注意一点，默认会先尝试使用Integer，Long，Short等来对应DECIMAL和 NUMERIC数据类型；
              -->
           <javaTypeResolver type="org.mybatis.generator.internal.types.JavaTypeResolverDefaultImpl">
               <property name="forceBigDecimals" value="false"></property>
           </javaTypeResolver>
   
           <!--生成实体-->
           <javaModelGenerator targetPackage="com.willson.facade.pojo.plot" targetProject="../facade/src/main/java">
               <property name="enableSubPackages" value="true"/>
           </javaModelGenerator>
           <!--生成mapper.xml文件-->
           <sqlMapGenerator targetPackage="plot"  targetProject="src/main/resources/mapper">
               <property name="enableSubPackages" value="true"></property>
           </sqlMapGenerator>
           <!--生成dao接口-->
           <javaClientGenerator type="XMLMAPPER" targetPackage="com.willson.service.mapper.plot" targetProject="src/main/java">
               <property name="enableSubPackages" value="true"></property>
           </javaClientGenerator>
           <!--为哪些表生成代码 tableName=表名字  domainObjectName 生成实体类名字-->
           <table tableName="tb_plot_herbaceous_plant" domainObjectName="herbaceousPlant" />
   
       </context>
   </generatorConfiguration>
   ```

4. 最后在右侧`maven projects->plugins->mybatis-generator:generate`运行就会生成了

   ![](http://ohdtoul5i.bkt.clouddn.com/1530182957362.png)

##注解式

基本格式,接口加`@Mapper`

```Java
package com.xhzg.xhzg.mapper;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Select;
@Mapper
public interface UserMapper {
    @Select("select * from user where username=#{username}")
    User loadUserByUsername(String username);
}

```

### 常用注解

```java
    @Select("select * from user where username=#{username}") //查询语
```

#### 实现插入数据后返回自增id：

```Java
    @Insert("INSERT INTO picturedetail(userid,detail) VALUES(#{userid}, #{detail})")
    @Options(useGeneratedKeys = true, keyProperty = "picturedetailid")
    int insertPictureDetail(PictureDetail pictureDetail);
```

`Options(useGeneratedKeys = true, keyProperty = "自增id")`用于返回自增id，返回后id读取直接从传入的

`PictureDetail`类里获取即可，不是通过返回值接收

#### 实现where if 查询语句

通过` @SelectProvider(type`实现

```java
    @SelectProvider(type = Provider.class,method = "queryPaperByParam")
    List<Paper> selectPaper(Paper paper);
```

查询provider类

```java
public class Provider {
    private final String TBL_PAPER = "paper"; //表名
	//查询方法，和注解里的名字要一致
    public String queryPaperByParam(Paper paper) {
        SQL sql = new SQL().SELECT("*").FROM(TBL_PAPER);

        if (!StringUtils.isEmpty(paper.getPapername())) {
            sql.WHERE("papername LIKE '%"+paper.getPapername()+"%'");
        }
        if (paper.getPaperid()!=0) {
            sql.WHERE("paperid = #{paperid}");
        }
        return sql.toString();
    }
}
```

---

## xml式

### [Mybatis Generator Example](http://www.mybatis.org/generator/generatedobjects/exampleClassUsage.html)

### 1.OR条件的使用

```sql
--?=keyword
select * from TBL_TEST WHERE ( NAME like ? ) or( SEX like ? ) and Class='1班';
```

等效于

```java
 TblTestExample example = new TblTestExample();
        if (!StringUtil.isEmpty(keyword)) {
            keyword="%"+keyword+"%"; //必须加，不然查不到
            example.or().andNameLike(keyword); //根据关键字查找
            example.or().andSexLike(keyword);//必须分开写，不然不是or
        }    
		example.createCriteria().andClassEqualTo("1班"); //限定会员单位
        }
        List<TblTest> testList = testMapper.selectByExample(example);
```



#### 问题

1. `Mapper method 'com.xxx' has an unsupported return type: class com.xxx.User`问题原因是mapper 中insert只能返回int，因此修改返回类型即可

2. `nested exception is org.apache.ibatis.builder.BuilderException: Error invoking SqlProvider method (com.xhzg.xhzg.mapper.Provider.queryflowerByParam). Cannot invoke a method that holds named argument(@Param) using a specifying parameterObject. In this case, please specify a 'java.util.Map' object.`错误解决：指定@param

   ```java
   //provider知道@param  
   public String queryflowerByParam(@Param("classid") int classid) {}
   @SelectProvider(type = Provider.class,method = "queryflowerByParam")
   List<FlowerInfoEntiy> selectFlowerinfo(@Param("classid") int classid);
   ```

   ​