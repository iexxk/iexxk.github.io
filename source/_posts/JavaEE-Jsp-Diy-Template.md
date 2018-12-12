---
title: jsp自定义模板（解决样式改变问题）
date: 2017-06-09 21:14:28
updated: 2018-12-12 10:47:58categories: JavaEE
tags: [idea,jsp,DOCTYPE]
---

### html转jsp页面样式发生改变

jsp页面DOCTYPE声明不对或者没有声明

修改idea jsp模板

`file->settings->Editor->File and Code Templates->Other->jsp files`

```jsp
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<%--不加这个样式会发生改变--%>
<!DOCTYPE html>
<html>
  <head>
    <title>#[[$Title$]]#</title>
  </head>
  <body>
  #[[$END$]]#
  </body>
</html>
```

idea默认jsp模板没有设置DOCTYPE

web2.5默认<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">

3.0默认<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

html5默认<!DOCTYPE html>

## 参考：

### [html转jsp页面样式发生改变](http://blog.csdn.net/qq_27039233/article/details/54092450)

