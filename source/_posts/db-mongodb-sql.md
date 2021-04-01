---
title: mongoDb常用应用场景
date: 2019-08-26 09:58:23
updated: 2021-03-19 11:13:47
categories: 数据库
tags: [mongoDB]
---

## 常用命令

```bash
# 密码登录验证
mongo 10.30.80.194:27017 -u admin  --authenticationDatabase=admin -p mima
#查看数据库列表
>show dbs
#切换数据库
>use admin
#查看当前数据库
>db
#查看所有表
>show tables
#验证密码
>db.auth("admin", "adminPass")
#查询表中所有数据
>db.表名.find()
#查看集群状态
>rs.status()
```

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

### 2. 正则匹配`$regex`

```shell
---data
  {"notice_key" : "[E00000003, 测试1]"}
---shell 且查询
db.getCollection("m_mq_log_record").find({"notice_key":{ $regex: /(?=.*测试1)(?=.*E00000003)/ }})
---java 且查询,`|`为或查询
query.addCriteria(Criteria.where("notice_key").regex("(?=.*测试1)(?=.*E00000003|.*E00000004|)"));
```

### 3. 聚合查询`aggregate`

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

group双层嵌套([$push](https://docs.mongodb.com/manual/reference/operator/aggregation/push/))-[Pivot Data](https://docs.mongodb.com/manual/reference/operator/aggregation/group/#pivot-data)

先group统计最内层，然后把group聚合的数组对象放到子对象那（利用 `subName: { $push: "$$ROOT" }`）

` $push: "$$ROOT"`是把聚合的对象放到一个字段subName里面

然后对统计好的再进行统计，如果要统计子对象数组里面的某个字段的数量，用`{ $sum: "$$ROOT.total" }`

```js
-- 先统计event_id
{ "$group": { "_id": { "event_id": "$event_id", "event_sub_type": "$event_sub_type" }, "total": { "$sum": "$num" }, sub: { $push: "$$ROOT" } } }
-- 在分组统计event_sub_type
{ "$group": { "_id": "$_id.event_sub_type", sub: { $push: "$$ROOT" },total: { $sum: "$$ROOT.total" } } }
```



##### `project`控制输出显示的结果

1为显示该字段

```js
"$project": {
            "_id": 1, 
             "customer_id": 1
}
```

##### `cond`类似case when

cond里面的if只支持一个条件，但是cond可以嵌套

Java: ConditionalOperators

```js
--如果$err_status=5 输出 1否则输出 0
"$cond": { "if": { "$eq": ["$err_status", "5"] }, "then": 1, "else": 0 }
-- 结合project可以统计错误信息等于5的数据条数
 "$project": {
            customer_id": 1
            , "fail_tatus": { "$cond": { "if": { "$eq": ["$err_msg", "5"] }, "then": 1, "else": 0 } }
        }
-- cond嵌套使用，"$gt": ["$record", 0] 可以用于判断对象是否为null，不为null继续cond，然后继续添加条件可以判断数组对象内的某个条件，达到1对多，子对象数组统计，判读子对象满足某个条件就设置为1，达到统计效果
{
                    "$cond": {
                        "if": { "$gt": ["$record", 0] }, "then":
                            {
                                "$cond": {
                                    "if": { "$eq": ["$record.is_opposite", false] }, "then":
                                       1, "else": 0
                                }
                            }, "else": 0
                    }
                }
```

##### `match`条件过滤

```

```

##### `unwind`

嵌入实体平铺，1个对象里面包含数组，平铺成一个对象对一个数组的内容，最终等于数组的条数

```js
"$unwind": "$term_info"
-- preserveNullAndEmptyArrays 为true时允许对象为null，不然平铺时如果对象为null时为null的这条数据就会消失
{ "$unwind": { "path": "$record", "preserveNullAndEmptyArrays": true } }
```

##### `lookup`

Java: LookupOperation

表关联左连接

```js
-- 表2为主集合
-- from 表1， localField 表1字段， foreignField 表2字段， as 新表表面
"$lookup": { "from": "b_terminfo", "localField": "devices_statuses.term_id", "foreignField": "term_id", "as": "term_info" }
-- 查询出的结果，表2-[表1数组]
```

##### `elemMatch` 内嵌数组，查询，其中数组里面的一个对象完全满足才会查出来

```js
"$elemMatch": {
        "term_id": "M59903"
        , "sync_status": "progressFail"
        , "err_msg": { "$ne": "5" }
    }}
```

对应java

```java
 Query query = new Query(Criteria.where("devices_statuses").elemMatch(
                    Criteria.where("term_id").is(termId)
                            .and("sync_status").is(Constants.OFFLINE_SYNC_DEVICE_PROGRESSFAIL)
                            .and("err_msg").ne(Constants.OFFLINE_SYNC_ERRORREASON_FAIL_FEATURE)
            ));
```

##### `facet`

多条语句组合一个结果,a，b，c各为独立的查询语句

```js
db.getCollection("b_company").aggregate([
    {
        "$facet": {
            "a": [
                { "$project": { Id: 1, "day": { "$substr": ["$time", 0, 10] } } }
                , { "$match": { day: "2020-07-09" } }
                , { "$group": { "_id": "$day", sum: { "$sum": 1 } } }
            ],
            "b": [
                { "$group": { "_id": null, total2: { "$sum": 1 } } }
            ],
            "c":[
                {"$lookup":{from:"b_user",localField:"Id",foreignField:"company_id",as:"user"}}    
               ,{"$unwind":"$user"}
               ,{ "$project": { Id: 1, "day": { "$substr": ["$user.user_login_time", 0, 10] } } }
               ,{ "$match": { day: "2021-02-05" } }
               ,{"$group":{"_id":"$Id",sum:{"$sum":1}}}
               ,{"$count":"total"}
            ]
        }
    }
])
```

对应java

```java
Aggregation aggregation = Aggregation.newAggregation(
                    Aggregation.facet()
                            .and(
                                    Aggregation.project("_id").and("time").substring(0, 10).as("day")
                                    , Aggregation.match(Criteria.where("day").is(nowDate))
                                    , Aggregation.count().as("count")
                            ).as("day")
                            .and(
                                    Aggregation.count().as("total")
                            ).as("total")
                            .and(
                                    Aggregation.lookup("b_user", "Id", "company_id", "user")
                                    , Aggregation.unwind("$user")
                                    , Aggregation.project("_id").and("user.user_login_time").substring(0, 10).as("day")
                                    , Aggregation.match(Criteria.where("day").is(nowDate))
                                    , Aggregation.group("_id")
                                    , Aggregation.count().as("total")
                            ).as("login")
            );
```

##### `$substr`

日期转换为天

```js
-- yyyy-mm-dd HH:mm:ss 转化成 yyyy-mm-dd
  { "$project": { Id: 1, "day": { "$substr": ["$time", 0, 10] } } }
--java
	Aggregation.project("_id").and("time").substring(0, 10).as("day")
```



### 最终示例

```js
db.getCollection("b_customer_info_device").aggregate([
    { "$unwind": "$devices_statuses" }
    , { "$lookup": { "from": "b_terminfo", "localField": "devices_statuses.term_id", "foreignField": "term_id", "as": "term_info" } }
    , { "$unwind": "$term_info" }
    , { "$match": {} }
    , {
        "$project": {
            "_id": 1, "customer_id": 1, "class_name": 1
            , "feature_fail": { "$cond": { "if": { "$eq": ["$devices_statuses.err_msg", "5"] }, "then": 1, "else": 0 } }
            , "total_fail": { "$cond": { "if": { "$eq": ["$devices_statuses.sync_status", "progressFail"] }, "then": 1, "else": 0 } }
        }
    }
    , {
        "$group": {
            "_id": { "_id": "$_id", "customer_id": "$customer_id", "class_name": "$class_name" }
            , "total_fail": { "$sum": "$total_fail" }
            , "feature_fail": { "$sum": "$feature_fail" }
        }
    }
    , {
        "$project": {
            "_id": 1, "customer_id": 1, "img_store_data": 1, "customer_name": 1, "class_name": 1
            , "feature_fail": { "$cond": { "if": { "$gt": ["$feature_fail", 0] }, "then": 1, "else": 0 } }
            , "total_fail": { "$cond": { "if": { "$gt": ["$total_fail", 0] }, "then": 1, "else": 0 } }
        }
    }

    , {
        "$group": {
            "_id": null
            , "total_customer": { "$sum": 1 }
            , "total_fail": { "$sum": "$total_fail" }
            , "feature_fail": { "$sum": "$feature_fail" }
        }
    }
]);
```

对应mongotemplate

```java
  ConditionalOperators.Cond condOperatorsFeature=ConditionalOperators.when(
                criteria.where("devices_statuses.err_msg").is(Constants.OFFLINE_SYNC_ERRORREASON_FAIL_FEATURE))
                .then(1)
                .otherwise(0);
        ConditionalOperators.Cond condOperatorsFail=ConditionalOperators.when(
                criteria.where("devices_statuses.sync_status").is(Constants.OFFLINE_SYNC_DEVICE_PROGRESSFAIL))
                .then(1)
                .otherwise(0);


        ConditionalOperators.Cond condOperatorsFeatureTotal=ConditionalOperators.when(
                criteria.where("feature_fail").gt(0))
                .then(1)
                .otherwise(0);
        ConditionalOperators.Cond condOperatorsFailTotal=ConditionalOperators.when(
                criteria.where("total_fail").gt(0))
                .then(1)
                .otherwise(0);

        Aggregation aggregation = Aggregation.newAggregation(
                Aggregation.unwind("$devices_statuses")
                ,LookupOperation.newLookup().from("b_terminfo")
                        .localField("devices_statuses.term_id")
                        .foreignField("term_id").as("term_info")
                ,Aggregation.unwind("$term_info")
                ,Aggregation.match(criteria)
                ,Aggregation.project("customer_id","class_name")
                        .and(condOperatorsFeature).as("feature_fail")
                        .and(condOperatorsFail).as("total_fail")
                ,Aggregation.group("customer_id","class_name")
                        .sum("total_fail").as("total_fail")
                        .sum("feature_fail").as("feature_fail")
                ,Aggregation.project()
                        .and(condOperatorsFeatureTotal).as("feature_fail")
                        .and(condOperatorsFailTotal).as("total_fail")
                ,Aggregation.group()
                        .count().as("total_customer")
                        .sum("total_fail").as("total_fail")
                        .sum("feature_fail").as("feature_fail")
        );
        AggregationResults<BasicDBObject> dBObjects=mongoTemplate.aggregate(aggregation,"b_customer_info_device",BasicDBObject.class);

        JSONArray countResult = JSON.parseObject(dBObjects.getRawResults().toJson()).getJSONArray("result");
        if(countResult!=null&&countResult.size()>0){
            JSONObject jobj = (JSONObject)countResult.get(0);
           return jobj;
        }
```

### 表关联子类统计

按类别统计每个事件的数量，输出结果如下

```
|-类型1
|--事件1
|----事件1记录1
|----事件1记录2
|----事件1记录n条
|--事件2
|-类型2
|--事件3
|----事件3记录1
```

```java
 String startTime = startDay + " 00:00:00";

            ConditionalOperators.Cond condCompany= addCompanyIdCriteriaInCond("record.company_id");

            //判断是否是当天
            ConditionalOperators.Cond condDay = ConditionalOperators.when(Criteria.where("record.trans_time").gte(startTime)
            ).then(condCompany!=null?condCompany:1).otherwise(0);

            //添加字表的判断是否是应答事件
            ConditionalOperators.Cond condOpposite = ConditionalOperators.when(Criteria.where("record.is_opposite").is(false)
            ).then(condDay).otherwise(0);

            //gt(0)是为了判断对象(是否有记录)是否为null，如果有对象就会大于0
            ConditionalOperators.Cond condOperators = ConditionalOperators.when(Criteria.where("record").gt(0)
            ).then(condOpposite).otherwise(0);

            Aggregation aggregation = Aggregation.newAggregation(
                    Aggregation.match(Criteria.where("event_type").is("device"))
                    , Aggregation.lookup("r_event_record", "event_id", "event_id", "record")
                    , Aggregation.unwind("$record", true)
                    , Aggregation.project("event_id", "event_name","event_sub_type").and(condOperators).as("num")
                    , Aggregation.group("event_id", "event_name","event_sub_type").sum("num").as("total")
                    , Aggregation.group("_id.event_sub_type").push("$$ROOT").as("sub").sum("$$ROOT.total").as("total")
            );

            AggregationResults<BasicDBObject> dBObjects = mongoTemplate.aggregate(aggregation, "b_event_info", BasicDBObject.class);
```

```js
db.getCollection("b_event_info").aggregate([
    { "$match": { "event_type": "device" } }
    , { "$lookup": { "from": "r_event_record", "localField": "event_id", "foreignField": "event_id", "as": "record" } }
    , { "$unwind": { "path": "$record", "preserveNullAndEmptyArrays": true } }

    , {
        "$project": {
            "event_id": 1, "event_name": 1, "num":
                {
                    "$cond": {
                        "if": { "$gt": ["$record", 0] }, "then":
                            {
                                "$cond": {
                                    "if": { "$eq": ["$record.is_opposite", false] }, "then":
                                        { "$cond": { "if": { "$gte": ["$record.trans_time", "2021-03-16 00:00:00"] }, "then": 1, "else": 0 } }, "else": 0
                                }
                            }, "else": 0
                    }
                }
            , "event_sub_type": 1
        }
    }
    , { "$group": { "_id": { "event_id": "$event_id", "event_sub_type": "$event_sub_type" }, "total": { "$sum": "$num" }, sub: { $push: "$$ROOT" } } }
    , { "$group": { "_id": "$_id.event_sub_type", sub: { $push: "$$ROOT" },total: { $sum: "$$ROOT.total" } } }
  --因为$addFields在mongotemplate找不到对应的语句，所以用上面的$group替代
//    ,{"$project": {"_id":1,"sub":1, total: { $sum: "$sub.total" }}}
//    , {
//        $addFields:
//            {
//                total: { $sum: "$books.total" }
//            }
//    }
])
```













