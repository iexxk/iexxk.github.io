---
title: JSP基础语法
date: 2017-03-06 11:47:27
updated: 2018-04-25 20:47:32categories: JavaEE
tags: [jsp,基础,入门,语法]
---
### 什么是jsp

是动态网页，可以嵌入java 代码 ，jsp 爷爷是servlet

### 基础语法

```jsp
<%-- page指令，可以配置session，errorPage，iserrorpage等等 --%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%-- 包含指令：用于设置公共的部分（eg：页头、也脚） --%>
<%@include file="/index.jsp"%>
<%!
    //  ！  定义在方法外面，可用做类的方法、属性
    void function() {
    }
%>
<%
    String aa = "xaa"; //java 代码
%>
<%=aa%>  <%-- 相当于out.print(aa); --%>
```
### jsp九大隐式对象

* **Reqeust**
* **Response**
* **Session**
* **Application**
* **Config**
* **Page**
* **Out**
* **Exception** (jsp独有)
* **pageContext** (jsp独有)

