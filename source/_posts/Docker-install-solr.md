---
title: Docker-install-solr
date: 2019-01-23 20:23:12
updated: 2019-01-23 20:29:21
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

