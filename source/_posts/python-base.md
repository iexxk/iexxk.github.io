---
title: python-base
date: 2020-09-24 14:12:20
updated: 2020-09-24 15:15:04
categories: python
tags: [python]
---

## python使用数据库

### python与mongodb

```python
import pymongo
#连接数据库
fund = pymongo.MongoClient('mongodb://ip.cn:14011/')["db_name"]
#条件查询数据，0代表不返回该字段，1代表返回该字段,sort第二个参数1升序，-1降序
result = fund["tb_name"].find({"name": "1"}, {"_id": 0, "name": 1}).sort("name",-1)
```



