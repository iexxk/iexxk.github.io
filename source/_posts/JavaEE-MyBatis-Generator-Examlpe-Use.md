---
title: Mybatis Generator Example使用
date: 2017-12-14 16:26:28
updated: 2017-12-14 16:27:33categories: JavaEE
tags: [java,Mybatis]
---

## [Mybatis Generator Example](http://www.mybatis.org/generator/generatedobjects/exampleClassUsage.html)

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



