---
title: Docker-install-mongo
date: 2019-01-23 21:37:49
updated: 2019-01-23 21:37:49
categories: Docker
tags: [Docker,mongo]
---



```dockerfile
  mongo:
    image: mongo
    restart: always
    ports:
      - 14017:27017
  #  environment:
  #    MONGO_INITDB_ROOT_USERNAME: root
  #    MONGO_INITDB_ROOT_PASSWORD: example
    volumes:
      - /dockerdata/v-yinfu/mongo/configdb:/data/configdb
      - /dockerdata/v-yinfu/mongo/db:/data/db   
```

