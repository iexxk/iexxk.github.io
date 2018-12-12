---
title: JavaEE之数据库基础
date: 2017-06-20 13:14:28
updated: 2018-12-12 10:47:58categories: 数据库
tags: [基础,数据库,面试]
---

## 数据库

### 1. 交叉连接（cross join）

交叉连接（CROSS JOIN）：有两种，显式的和隐式的，不带ON子句，返回的是两表的乘积，也叫**笛卡尔积**。

例如：下面的语句1和语句2的结果是相同的。

语句1：**隐式的交叉连接**，没有CROSS JOIN。

```sql
SELECT O.ID, O.ORDER_NUMBER, C.ID, C.NAME
FROM ORDERS O , CUSTOMERS C
WHERE O.ID=1;
```

语句2：**显式的交叉连接，**使用CROSS JOIN。

```sql
SELECT O.ID,O.ORDER_NUMBER,C.ID,
C.NAME
FROM ORDERS O CROSS JOIN CUSTOMERS C
WHERE O.ID=1;
```

语句1和语句2的结果是相同的，查询结果如下：

`a`表：

| id   | name |
| ---- | ---- |
| 1    | 张三   |
| 2    | 李四   |
| 3    | 王五   |

`b`表：

| id   | job  | parent_id |
| ---- | ---- | --------- |
| 1    | java | 1         |
| 2    | php  | 2         |
| 3    | php  | 4         |

##### 1. 内连接(`INNER JOIN`)

内连接（INNER JOIN）：有两种，显式的和隐式的，返回连接表中符合连接条件和查询条件的数据行。（所谓的链接表就是数据库在做查询形成的中间表）。

###### 显式内连接

```mysql
SELECT a.*,b.* FROM a INNER JOIN b ON a.id=b.parent_id
//或者
SELECT a.*,b.* FROM a INNER JOIN b WHERE a.id=b.parent_id
```

###### 隐式内连接

```mysql
SELECT a.*,b.* FROM a,b WHERE a.id=b.parent_id  //只能用where
```

结果：

| id   | name | id1  | job  | parent_id |
| ---- | ---- | ---- | ---- | --------- |
| 1    | 张三   | 1    | java | 1         |
| 2    | 李四   | 2    | php  | 2         |

##### 2. 左连接(`LEFT JOIN`)

左向外联接的结果集包括  LEFT OUTER子句中指定的左表的所有行，而不仅仅是联接列所匹配的行。如果左表的某行在右表中没有匹配行，则在相关联的结果集行中右表的所有选择列表列均为空值。    

```mysql
SELECT a.*,b.* FROM a LEFT JOIN b ON a.id=b.parent_id
```

| id   | name | id1    | job    | parent_id |
| ---- | ---- | ------ | ------ | --------- |
| 1    | 张三   | 1      | java   | 1         |
| 2    | 李四   | 2      | php    | 2         |
| 3    | 王五   | `null` | `null` | `null`    |

##### 3. 右连接(`RIGHT JOIN`)

右向外联接是左向外联接的反向联接。将返回右表的所有行。如果右表的某行在左表中没有匹配行，则将为左表返回空值。    

```mysql
SELECT a.*,b.* FROM a RIGHT JOIN b ON a.id=b.parent_id
```

| id     | name   | id1  | job  | parent_id |
| ------ | ------ | ---- | ---- | --------- |
| 1      | 张三     | 1    | java | 1         |
| 2      | 李四     | 2    | php  | 2         |
| `null` | `null` | 3    | php  | 4         |

##### 4.完全连接（`FULL JOIN`,`UNION`）

完整外部联接返回左表和右表中的所有行。当某行在另一个表中没有匹配行时，则另一个表的选择列表列包含空值。如果表之间有匹配行，则整个结果集行包含基表的数据值。   

```mysql
SELECT a.*,b.* FROM a FULL JOIN b ON a.id=b.parent_id   //MYSQL不支持full join
//可以用union连接左连接和右连接代替full join
SELECT a.*,b.* FROM a LEFT JOIN b ON a.id=b.parent_id
UNION
SELECT a.*,b.* FROM a RIGHT JOIN b ON a.id=b.parent_id
```

| id     | name   | id1    | job    | parent_id |
| ------ | ------ | ------ | ------ | --------- |
| 1      | 张三     | 1      | java   | 1         |
| 2      | 李四     | 2      | php    | 2         |
| 3      | 王五     | `null` | `null` | `null`    |
| `null` | `null` | 3      | php    | 4         |

##### 5.交叉连接（`CROSS JOIN`）

```mysql
SELECT a.*,b.* FROM a CROSS JOIN b WHERE a.id=b.parent_id
SELECT a.*,b.* FROM a CROSS JOIN b ON a.id=b.parent_id
```

### **ON后面的条件（ON条件）和WHERE条件的区别：**

* ON条件：是过滤两个链接表笛卡尔积形成中间表的约束条件。
* WHERE条件：在有ON条件的SELECT语句中是过滤中间表的约束条件。在没有ON的单表查询中，是限制物理表或者中间查询结果返回记录的约束。在两表或多表连接中是限制连接形成最终中间表的返回结果的约束。

从这里可以看出，将WHERE条件移入ON后面是不恰当的。推荐的做法是：
ON只进行连接操作，WHERE只过滤中间表的记录。

## 总结

1. 查两表关联列相等的数据用内连接。
2. Col_L是Col_R的子集时用右外连接。
3. Col_R是Col_L的子集时用左外连接。
4. Col_R和Col_L彼此有交集但彼此互不为子集时候用全外。
5. 求差操作的时候用联合查询。

多个表查询的时候，这些不同的连接类型可以写到一块。例如：

```mysql
SELECT T1.C1,T2.CX,T3.CY

FROM TAB1 T1

       INNER JOIN TAB2 T2 ON (T1.C1=T2.C2)

       INNER JOIN TAB3 T3 ON (T1.C1=T2.C3)

       LEFT OUTER JOIN TAB4 ON(T2.C2=T3.C3);

WHERE T1.X >T3.Y;
```

上面这个SQL查询是多表连接的一个示范。

#### 参考

[深入理解MySQL的外连接、内连接、交叉连接](http://www.shuchengxian.com/article/168.html)

[Java就业企业面试问题-数据库（强烈推荐）](http://bbs.itheima.com/thread-329953-1-1.html?srx)