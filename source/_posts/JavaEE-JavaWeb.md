---
title: JavaEE之java web基础概念
date: 2017-06-19 22:14:28
updated: 2018-01-28 21:41:27categories: JavaEE
tags: [基础,java,面试]
---

## Java Web基础

### 1 Ajax

AJAX = Asynchronous JavaScript and XML（异步的 JavaScript 和 XML）。

AJAX 是与服务器交换数据并更新部分网页的艺术(新方法)，在不重新加载整个页面的情况下。

```javascript
$.ajax({url:"/jquery/test1.txt",async:false}); //jQuery.ajax([settings])使用方法
```

### 2 cookie和session

Cookie是会话技术,将用户的信息保存到浏览器的对象.

Session也是会话技术,将Session的信息保存到服务器的对象.Session是基于Cookie的 利用Cookie向浏览器回写JSessionID.

### 3 网站大量登陆访问session过多

session默认保存在内存中，内存资源宝贵，session数据量大导致内存利用率高

* 解决方案：
  1. 设置session超时时间
  2. 将session中的数据序列化到硬盘中
  3. 不使用session，使用cookie（此方法存在安全性问题）

### 4  Jsp九大内置对象

* Page：指的是JSP被翻译成Servlet的对象的引用.
* pageContext：对象可以用来获得其他8个内置对象,还可以作为JSP的域范围对象使用.pageContext中存的值是当前的页面的作用范围》
* request：代表的是请求对象,可以用于获得客户机的信息,也可以作为域对象来使用，使用request保存的数据在一次请求范围内有效。
* Session代表的是一次会话，可以用于保存用户的私有的信息,也可以作为域对象使用，使用session保存的数据在一次会话范围有效
* Application：代表整个应用范围,使用这个对象保存的数据在整个web应用中都有效。
* Response：是响应对象,代表的是从服务器向浏览器响应数据.
* Out：out对象被封装为JSPWriter接口，是用于向页面输出内容的对象
* Config：指的是ServletConfig用于JSP翻译成Servlet后 获得Servlet的配置的对象.
* Exception：在页面中设置isErrorPage=”true”，即可使用，是Throwable的引用.用来获得页面的错误信息。

#### 参考

[Java就业企业面试问题-Java Web（强烈推荐）](http://bbs.itheima.com/thread-329949-1-1.html)



