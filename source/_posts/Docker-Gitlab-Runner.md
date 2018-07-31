---
title: Docker-Gitlab-Runner
date: 2018-07-31 18:25:16
updated: 2018-07-31 18:31:30
categories: Docker
tags: [Docker,Gitlab,CI]
---

### 常见问题总结

1. 注册之后，运行时找不到runner,一直提示pending

   解决：在runner设置里勾选上`Run untagged jobs`

   - [x]  Indicates whether this runner can pick jobs without tags

2. 使用`docker`注册时，镜像用`docker:stable`在配置文件`config.toml`添加` volumes = ["/var/run/docker.sock:/var/run/docker.sock","/cache"]`

   ```toml
   concurrent = 1
   check_interval = 0
   
   [[runners]]
     name = "test"
     url = "http://gitlab/"
     token = "8db125c537f652e20349100517a4d6"
     executor = "docker"
     [runners.docker]
       tls_verify = false
       image = "docker:stable"
       privileged = false
       disable_cache = false
       volumes = ["/var/run/docker.sock:/var/run/docker.sock","/cache"]
       shm_size = 0
     [runners.cache]
   ```

   

