---
title: Mybatis 使用
date: 2017-12-14 16:26:28
updated: 2018-01-28 21:41:27
categories: JavaEE
tags: [java,Mybatis]
---

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