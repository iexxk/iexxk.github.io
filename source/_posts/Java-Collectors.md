---
title: Java8 list分组
date: 2018-09-15 18:52:01
updated: 2018-09-15 18:52:01
categories: Java
tags: [Java8,Collectors]
---

## 实战按月分类list数据

数据源：

```json
{
    "2018年08月":[
        {
            "createTime":"2018-08-15 15:51:16"
        },
        {
            "createTime":"2018-08-15 15:51:15"
        }
    ],
    "2018年09月":[
        {
            "createTime":"2018-09-15 15:51:16"
        },
        {
            "createTime":"2018-09-15 15:51:15"
        }
    ]
}   
```

代码：

```java
//-----------------实体类-----------------
public class ThematicMap extends BaseBean {
    ....
    public String getMonth(){
        Date createTime= this.getCreateTime(); //获取basebean的时间
        SimpleDateFormat format1 = new SimpleDateFormat("yyyy年MM月");
        return format1.format(createTime.getTime());
    }
}
//--------------------------------------

List<ThematicMap> thematicMapList = thematicMapMapper.listForPage(params);
//getMonth方法获取数据，
Map<String,List<ThematicMap>> stringListMap=thematicMapList.stream().collect(Collectors.groupingBy(ThematicMap::getMonth,LinkedHashMap::new,Collectors.toList()));
```



`Collectors.groupingBy(Function<? super T, ? extends K> classifier,
​                                  Supplier<M> mapFactory,
​                                  Collector<? super T, A, D> downstream)`有三个参数

如果不考虑顺序一个参数即可`thematicMapList.stream().collect(Collectors.groupingBy(ThematicMap::getMonth));`

第二个参数是指定容器：默认值是`HashMap::new`,但是它会导致乱序，因此使用`LinkedHashMap`

最终数据结构

```json
{
    "2018年08月":[
        {
            "createTime":"2018-08-15 15:51:16"
        },
        {
            "createTime":"2018-08-15 15:51:15"
        }
    ],
    "2018年09月":[
        {
            "createTime":"2018-09-15 15:51:16"
        },
        {
            "createTime":"2018-09-15 15:51:15"
        }
    ]
}       
```





###### 参考

[Collectors.groupingBy分组后的排序问题](https://www.cnblogs.com/zhshlimi/p/9070543.html)