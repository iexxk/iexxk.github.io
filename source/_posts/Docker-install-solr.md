---
title: Docker-install-solr
date: 2019-01-23 20:23:12
updated: 2019-01-29 10:54:37
categories: Docker
tags: [Docker,solr]
---



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



