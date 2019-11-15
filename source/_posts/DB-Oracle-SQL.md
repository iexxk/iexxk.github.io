---
title: oracle常用sql总结
date: 2019-10-23 10:03:20
updated: 2019-11-14 16:24:57
categories: 数据库
tags: [oracle,sql]
---

### 语法

#### 1. `SUM(<需要求和的字段,字段必须是数字类型>)`和`count(<需要统计条数的字段>)`

sum注意区分count，一个是根据字段里面的值求和，一个是根据条数求数据总条数

```sql
-- 对所有用户的年龄进行累加求和
select  SUM(u.AGE) from t_user u ;
```

#### 2. `CASE WHEN <条件> THEN <满足条件的结果> ELSE <不满足条件的结果> END`

`CASE <条件字段> WHEN <值1> THEN <满足条件=值1的结果> WHEN <值2> THEN <满足条件=值2的结果>    ... ELSE <不满足所有条件的结果> END`

```sql
--eg:查询年龄大于18的flag输出成年人，否则未成年人
select CASE WHEN u.age>18 THEN '成年人' ELSE '未成年人' END as flag from t_user u;
--eg:多条件组合查询年龄大于18且是男的的flag输出男成年人，否则未成年人
select CASE WHEN u.age>18 and u.sex='男' THEN '男成年人' ELSE '未成年人' END as flag from t_user u;
--按条件统计总数，sum是求和，输出只能是1 ELSE 0，因为要进行累加
--统计大于18的总人数
select sum(CASE WHEN u.age>18 THEN 1 ELSE 0 END) as total from t_user u;
--多条件switch实现,将boy替换成男，girl替换成女，其他输出人妖
select CASE u.sex
    WHEN 'boy' THEN '男'
    WHEN 'girl' THEN '女'
    ELSE '人妖' END  from t_user u;
```

#### 3. `DECODE(<条件字段>,<值1>,<满足条件=值1的结果>,<值2>,<满足条件=值2的结果>,....,<都不满足>)`

```sql
--将boy替换成男，girl替换成女，其他输出人妖，等效于case when
select DECODE(u.SEX,'boy','男','girl','女','人妖') from t_user u;
```

#### 4. `NVL(<需要判断的字段>,<如果判断的字段为null输出的结果>)`

```sql
--数据为null的会替换成人妖
select nvl(u.SEX,'人妖') from t_user u;
--没有年龄的设置为0,方便统计空数据
select sum(nvl(u.age,0)) from t_user u;
```

#### 5.  `group by <分组的字段1，字段2...>`分组统计

select后面的字段=分组的字段+统计求和等字段，原理分组过后，查询不能查一个组有多个不同结果的字段，如果是相同的结果加入group by 字段1，字段2

```sql
--按年龄分组统计各个年龄的总数
select u.AGE,count(u.SEX) from T_USER u group by u.AGE;
--按年龄性别进行分组统计,统计年龄相同且性别相同的个数
select u.AGE,u.SEX,count(*) from T_USER u group by u.AGE,u.SEX
```

#### 5. `order by <排序字段> <desc/asc>` asc升序，desc降序

```sql
--按时间升序
select * from  T_USER order by "creat_time" asc
```

#### 6. `to_char(sysdate, 'yyyy-MM-dd')`格式化日期

```sql
--sysdate获取当前日期，to_char格式化为天
select to_char(sysdate, 'yyyy-MM-dd') from DUAL;
--按天分组统计
select sum(1),to_char(u."creat_time",'YYYY-MM-DD') as day from t_user u group by to_char(u."creat_time",'YYYY-MM-DD');
--按月分组统计，按年等其他日期类似
select sum(1),to_char(u."creat_time",'YYYY-MM') as day from t_user u group by to_char(u."creat_time",'YYYY-MM');
--查询7天前的数据，其他天类似
select * from T_USER u where to_char(u."creat_time",'yyyy-MM-dd')>to_char(sysdate-7, 'yyyy-MM-dd')
--统计查询前7天的数据，当天没有统计为0，按时间降序
select t_date.day, NVl(t_data.total, 0)
from (select TO_CHAR(trunc(sysdate + 1 - ROWNUM), 'yyyy-MM-dd') day from DUAL connect by ROWNUM <= 7) t_date
         left join (select to_char(u."creat_time", 'yyyy-MM-dd') as day, count(1) as total
                    from T_USER u
                    group by to_char(u."creat_time", 'yyyy-MM-dd')) t_data
                   on t_data.day = t_date.day
order by t_date.day asc;
```

#### 7. round(<小数>,<保留小数点后位数>)

```sql
--保留小数点后2位，输出33.33
select round( 1/3*100 ,2) from dual;
```

#### 8. `left join` 左连接

以左边为主，右边有就连接，没有就null

```sql
select * from T_USER l left join T_USER r on l.AGE=r.FLAG;
```

#### 9. `substr(<需要裁剪的字符串>,<开始位置>, <结束位置>)`

```sql
-- 输出2019
select substr('2019-01-02',1, 4) from DUAL;
```

#### 10. `connect by`

其他用法，获取树形数据(也就是父子关系)见google

`rownum`数据库关键字，行数

```sql
--生成1-10的序列
select rownum from dual connect by rownum<=10;
--生成7天的日期
select TO_CHAR(trunc(sysdate+1-ROWNUM),'yyyy-MM-dd') dd from DUAL connect by  ROWNUM <= 7
```

#### 11. `union <all>` 两个结果集合并

有all 全连接，不去重，没有all 去重

```sql
-- 输出1-4-1-4
select rownum from dual connect by rownum<=4
union all
select rownum from dual connect by rownum<=4;
-- 输出1-4
select rownum from dual connect by rownum<=4
union 
select rownum from dual connect by rownum<=4;
```

#### 12. ROLLUP 分组汇总

ROLLUP汇总分组排列在最后一条数据，但是数据头为null，可以通过null判断取别名为总数

```sql
SELECT nvl(CASE
               WHEN sex = 'boy' THEN '男'
               WHEN sex = 'girl' THEN '女'
               ELSE '人妖'
               END, '总数') AS type,
       count(1)           as num
from t_user
GROUP BY
    ROLLUP
    ( CASE
          WHEN sex = 'boy' THEN '男'
          WHEN sex = 'girl' THEN '女'
          ELSE '人妖'
          END);
```

#### 13. `||`字符连接符

用于单位，用于多条数据拼接

```sql
select 'sex是'||u.SEX||',年龄是'||u.AGE as detail from T_USER u;
--------输出结果------
--sex是boy,年龄是1
--sex是girl,年龄是2
```



#### 示例数据

```sql
create table T_USER
(
	AGE NUMBER,
	FLAG VARCHAR2(10),
	SEX VARCHAR2(4),
	"creat_time" DATE
)
INSERT INTO SYSTEM.T_USER (AGE, FLAG, SEX, "creat_time") VALUES (1, '2', 'boy', TO_DATE('2019-10-23 03:14:11', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO SYSTEM.T_USER (AGE, FLAG, SEX, "creat_time") VALUES (2, '4', 'girl', TO_DATE('2019-10-24 03:14:14', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO SYSTEM.T_USER (AGE, FLAG, SEX, "creat_time") VALUES (3, '6', 'ff', TO_DATE('2019-10-26 03:14:19', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO SYSTEM.T_USER (AGE, FLAG, SEX, "creat_time") VALUES (3, '2', null, TO_DATE('2019-10-23 03:14:23', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO SYSTEM.T_USER (AGE, FLAG, SEX, "creat_time") VALUES (null, '2', null, TO_DATE('2019-10-23 03:14:25', 'YYYY-MM-DD HH24:MI:SS'));
```



