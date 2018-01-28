---
title: 数据库MySQL之查询
date: 2017-06-27 20:14:28
updated: 2017-06-27 21:50:39categories: 数据库
tags: [基础,数据库,面试]
---

## 查询（SELECT）

###### 查询employee_id为1，2，3的结果

```mysql
#多条件查询
SELECT * FROM employee WHERE employee.employee_id =1 OR employee.employee_id=2 OR employee.employee_id=3
#范围（1~3）查询
SELECT * FROM employee WHERE employee.employee_id BETWEEN 1 and 3
#半开范围查询
SELECT * FROM employee WHERE employee.employee_id<=3
```

