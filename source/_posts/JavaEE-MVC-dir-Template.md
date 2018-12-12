---
title: JavaEE之MVC目录结构
date: 2017-03-17 10:20:28
updated: 2018-12-12 10:47:58categories: JavaEE
tags: [JavaEE,环境搭建,MVC]
---

## mvc目录结构

模块内分mvc层，mvc层内分模块

eg：下面介绍以功能模块（model）进行mvc分层,类的命名以`功能模块名字Dao.java`命名

###### `dao`层

ModelDao.java文件结构如下

```java
package com.xuan.goods.model.dao;

import org.apache.commons.dbutils.QueryRunner;
import org.apache.commons.dbutils.handlers.BeanHandler;
import cn.itcast.jdbc.TxQueryRunner;
import com.xuan.goods.model.domain.Model;
/***
*模块持久层， 操作数据库
*/
public class ModelDao{
 private QueryRunner qr=new TxQueryRunner();
  /**
  *抛出异常
  */
 public Model findByName(String name)throws SQLException{
  String sql="select result from model where name=?";  //数据库语句
   //？的值为第三个name参数值，多个问号依次像后面增加参数
  return qr.query(sql, new BeanHandler<Model>(Model.class),name); 
 }
}
```

###### `domain`层

Model.java文件结构如下

```java
package com.xuan.goods.model.domain;
/**
*实体层
*/
public class Model{
  	//对应数据库
private String uid;//主键
private String name;//名字
public String getUid() {
	return uid;
}
public void setUid(String uid) {
	this.uid = uid;
}
/**
*get方法可以在jsp页面里直接用标签引用获得值，${model.name}
*/
public String getName() {
	return name;
}
public void setName(String name) {
	this.name = name;
}  
}
```



###### `service`层

ModelService.java文件结构如下

```java
package com.xuan.goods.user.service;
/***
*业务逻辑层
*/
public class ModelService{
  private ModelDao modelDao=new ModelDao(); //连接数据库操作层
  /**
  *业务逻辑
  */
  public Model findModel(String name) throw ModelException{
   Model model=modelDao.findByName(name);
    if (model=null){
      //将错误转换为自定义异常ModelException自定义异常类只需要extends Exception这个类 
      throw new ModelException("未找到模块！");
    }
    try{
       return model;
    }catch(SQLException e){
      throw new RuntimeException(e);//转换异常，并传递异常
    }
  }
}
```

###### `web`层

servlet 包下ModelServlet.java文件结构如下

```java
package com.xuan.goods.model.web.servlet;
/***
*页面显示层
*/
public class ModelServlet extends BaseServlet{
  private ModelService modelService=new ModelService(); //连接业务逻辑层
  public string findName(HttpServletRequest req, HttpServletResponse resp)
			throws ServletException, IOException {
		String name = req.getParameter("name"); // 获取名
		Model model = modelService.findModel(name);// 通过service得到结果
    	req.setAttribute("model", model); // 保存成功信息，转发到msg.jsp显示,jsp页面里直接用标签引用获得值，${model.name}
		return "f:/jsps/msg.jsp"; // 转发到页面
}
```

### 代码见`goods`项目

