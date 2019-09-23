---
title: mongoDb常用应用场景
date: 2019-08-26 09:58:23
updated: 2019-09-19 14:15:43
categories: 数据库
tags: [mongoDB]
---

##  常用场景

### 1. 批量更新`updateMany`

更新对象A中包含list<对象B中设备id为a1>，且对象B中的状态为0的所有数据,把状态更新为1

##### 数据结构

```json
{ 
    "_id" : ObjectId("5d566377e831932f076cecfe"), 
    "name" : "222", 
    "devices_statuses" : [
        {
            "device_id" : "a1", 
            "status" : "0"
        }
    ], 
    "_class" : "com.xxx.bean.CustomerInfoDevice"
}
```

####`updateMany`更新多条

与`findAndModify`区别 `findAndModify`更新单条，sort排序的首条

mongo对应的js查询脚步

```js
db.b_customer_info_device.updateMany({"devices_statuses.status":"0","devices_statuses.device_id":"a1"},{$pull:{"devices_statuses":{term_id:"D00010"}}});
```

springboot对应写法

```java
Query query = new Query(Criteria.where("devices_statuses.device_id").is(termId).and("devices_statuses.status").in("0");
Update update = new Update();
//更新删除，删除devices_statuses数组对象中termId=？的，pull为从数组移出
//update.pull("devices_statuses", Query.query(Criteria.where("term_id").is(termId)));
//更新状态为1                        
update.set("devices_statuses.$.sync_status", "1");
mongoTemplate.updateMulti(query, update, CustomerInfoDevice.class);
```



### 2. 聚合查询`aggregate`

##### 数据结构

```json
{
  {
   _id: ObjectId(7df78ad8902c)
   name: '张三', 
	 user: "san"
   code: '0'
  },
  {
   _id: ObjectId(7df78ad8902c)
   name: '李四', 
	 user: "si"
   code: '1'
  },
  {
   _id: ObjectId(7df78ad8902c)
   name: '张三', 
	 user: "san"
   code: '1'
  }
}
```

##### [group](https://docs.mongodb.com/manual/reference/operator/aggregation/group/)

按`_id`里面的字段进行分组统计，这里按`code`字段进行分组

 `_id:null` 统计所有

`_id:"$code"`按code字段进行统计



```js
db.getCollection("m_user").aggregate([
{
	"$group":{
	    _id:"$code"
	    ,recordNum:{'$sum': 1}
	    }
}
]);

```

执行结果

```json
{ 
    "_id" : "0", 
    "recordNum" : 1.0
}
// ----------------------------------------------
{ 
    "_id" : "1", 
    "recordNum" : 2.0
}
```









