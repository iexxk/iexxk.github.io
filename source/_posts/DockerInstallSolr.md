---
title: Docker-install-solr
date: 2019-01-23 20:23:12
updated: 2019-02-18 18:12:40
categories: Docker
tags: [Docker,solr]
---



### solr清除数据

步骤：

1. 登录solr网页

2. 搜索对应的core

3. 点击Documents --> Document Type --> 选择XML类型 

4. 定格编写语句：

   ```
   <delete><query>*:*</query></delete>
   <commit/>
   ```

5. 最后点击Submit  Document

### 安装



`docker-compose.yml`

```dockerfile
  solr:
    image: solr:5.5.5
    restart: always
    ports:
      - 14093:8983
```

访问[ip:14093]()



常见问题

问题1： index已经锁定`Caused by: org.apache.solr.common.SolrException: Index locked for write for core XXX`

解决：

solr数据备份注意目录复制时权限

```bash
#删除这个文件
rm /data/soft/solr/data/index/write.lock
#以root权限进入容器执行
docker exec -it --user root <容器id> bash
cd /opt/solr/server/solr
chown -R solr:solr sure-core
```



