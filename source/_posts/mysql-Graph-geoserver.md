---
title: mysql-Graph-geoserver
date: 2018-10-11 11:35:07
updated: 2018-10-12 23:02:46
categories: 杂谈
tags: [mysql,geometry,geoserver]
---

## geoserver绘制形状

#### 绘制矩形图形(`POLYGON`)

注意事项：第一个点和最后一个点必须相同，因此矩形至少是5个点

![](http://ohdtoul5i.bkt.clouddn.com/%255CUsers%255Cxuan%255CAppData%255CRoaming%255CTypora%255Ctypora-user-images%255C1539238451033.png)

```mysql
--添加面
SET @g = 'POLYGON((114.34845 25.48141, 114.34845 25.28141, 114.51599 25.28141, 114.51599 25.48141, 114.34845 25.48141))';
INSERT INTO test(shape) VALUES (ST_PolygonFromText(@g));
--添加点
SET @g = ST_GeomFromText('POINT(114.44845 25.38141)'); INSERT INTO test(shape) VALUES (@g);
```

表结构：

| 名    | 类型     |
| ----- | -------- |
| id    | int      |
| shape | geometry |
| name  | varchar  |

### 常见语句
```MYSQL

-- 插入
SET @g = ST_GeomFromText('POINT(109.49097 19.06798)',1);
 INSERT INTO infcamer(shape) VALUES (@g);
-- 更新 
UPDATE `功能分区面` set SHAPE=ST_PolygonFromText(@g,1) WHERE OGR_FID=1; 
-- 查询坐标是否正确设置
SELECT * FROM infcamer WHERE ST_Contains(SHAPE, ST_GeomFromText( 'POINT(109.49097 19.06798)',0))
-- 查询空间坐标相关设置
SELECT * FROM spatial_ref_sys LIMIT 0, 50;
-- geoserver数据库
GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]
-- test数据库
GEOGCS["GCS_WGS_1984",DATUM["WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]

GEOGCS["GCS_WGS_1984",DATUM["WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433],METADATA["World",-180.0,-90.0,180.0,90.0,0.0,0.0174532925199433,0.0,1262]]
```

### 镂空面

数据格式为

`POLYGON((a a, b b,a a),(c c,d d, c c)) `

### 常见问题

1. 点坐标查询提示`[Err] 3033 - Binary geometry function st_contains given two geometries of different srids: 0 and 1, which should have been identical.`

   **分析**：由于插入时的**srid**不一致，用`SELECT * FROM infcamer WHERE ST_Contains(SHAPE, ST_GeomFromText( 'POINT(109.49097 19.06798)'))`查询时没有指定**srid**，所以报错提示有不同的srid

   **解决1**：查询时指定**srid**例如：`SELECT * FROM infcamer WHERE ST_Contains(SHAPE, ST_GeomFromText( 'POINT(109.49097 19.06798)',0))`

   **解决2**：插入时指定**srid**,指定的**srid**最好和原有记录的**srid**一致，这样就不会存在`different srids: 0 and 1`，例如：`SET @g = ST_GeomFromText('POINT(109.49097 19.06798)',0);
    INSERT INTO infcamer(shape) VALUES (@g);`

2. 在`Navicat`客户端看不到完整数据，最好导出看




### 参考

[Mysql官方文档](https://dev.mysql.com/doc/refman/5.7/en/populating-spatial-columns.html)

[Mysql的空间扩展](http://www.mysqlab.net/docs/view/refman-5.1-zh/chapter/spatial-extensions-in-mysql.html)  较全，值得一看

[mysql ogr2ogr error](https://bugs.mysql.com/bug.php?id=79282)