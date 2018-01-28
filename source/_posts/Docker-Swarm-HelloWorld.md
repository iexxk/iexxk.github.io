---
title: Docker Swarm之HelloWorld
date: 2017-12-05 13:56:37
updated: 2017-12-13 12:06:35categories: Docker
tags: [集群,Swarm,Docker,nginx,overlay,ingress]
---
### 服务发现

服务发现组件记录了（大规模）分布式系统中所有服务的信息，人们或者其它服务可以据此找到这些服务。 DNS 就是一个简单的例子。当然，复杂系统的服务发现组件要提供更多的功能，例如，服务元数据存储、健康监控、多种查询和实时更新等。

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





