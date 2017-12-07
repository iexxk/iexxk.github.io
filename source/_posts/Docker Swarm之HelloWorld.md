---
title: Docker Swarm之HelloWorld
date: 2017-12-05 13:56:37
categories: docker集群
tags: [集群,Swarm,docker,nginx,overlay,ingress]
---
### 环境

| ID                        | Hostname(role)                | IP             | 端口（不包括必须的）     |
| ------------------------- | ----------------------------- | -------------- | -------------- |
| ywtryezli3s9hvhnmzgndi118 | xuanps(manager)               | 10.14.0.1:2377 | TCP14000-14020 |
| n8jomnk98nrog10tsspp3u38u | localhost.localdomain(worker) | 10.14.0.4      | TCP14000-14020 |
| kpbotld5edj55azexhbjfixai | xuan-ubuntu(worker)           | 192.168.123.2  |                |

镜像：[marshalw/hello-service](https://hub.docker.com/r/marshalw/hello-service/tags/)

创建服务`docker service create -p 3000:3000 --name hello-service marshalw/hello-service:0.1.0`

然后再三台主机都能访问下面任何一个地址

```
curl http://10.14.0.4:14000/hello/name
curl http://10.14.0.1:14000/hello/name
curl http://192.168.123.2:14000/hello/name
curl http://112.74.51.136:14000/hello/name
```





