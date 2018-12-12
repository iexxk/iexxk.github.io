---
title: JavaEE-MyBatis
date: 2018-10-16 16:33:07
updated: 2018-12-12 10:47:58
categories: JavaEE
tags: [JavaEE,MyBatis]
---

## mybatis使用基础

```xml
<mapper namespace="com.willson.service.mapper.infrared.InfraredPictureMapper">
  <resultMap id="BaseResultMap" type="com.willson.facade.pojo.infrared.InfraredPicture">
    <id column="r_id" />
    <result column="id" jdbcType="BIGINT" property="id" />
    <association property="resource" javaType="com.willson.facade.pojo.sys.Resource" columnPrefix="r_" >
      <id column="id" property="id" jdbcType="BIGINT"/>
      <result column="name" property="name" jdbcType="VARCHAR"/>
    </association>
    <collection property="soil" ofType="com.willson.facade.pojo.plot.Soil" columnPrefix="s_">
      <id column="id" property="id" jdbcType="BIGINT"/>
      <result column="plot_num" jdbcType="VARCHAR" property="plotNum" />
    </collection>
  </resultMap>
    
  <sql id="Base_Column_List">
    t.id,
    r.id r_id
  </sql>    
```

解释：

`<id column="r_id" />` 一般主键id，如果id存在相同（例如一对多时）,id相同的就只会显示一个,因此在多一对多是，关联字段也要加别名

` <association  >` 对应实体类object ,一对一

`<collection >`对应list< Object > ,一对多