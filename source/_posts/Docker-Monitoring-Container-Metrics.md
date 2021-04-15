---
title: Docker监控容器指标
date: 2021-03-31 10:15:33
updated: 2021-04-15 11:00:15
categories: Docker
tags: [Docker,Cadvisor,prometheus]
---

在docker部署多个微服务后，发现宿主机内存不断的慢慢上涨，因此想知道是哪个微服务慢慢不断让内存上涨，因此想用一个监控软件，监控所有微服务的性能等指标

## 名词介绍

* [prometheus](https://prometheus.io/)：时间序列数据存储、查询、可视化、报警。（相当于Grafana+influxDB+其他的组合拳）
* [Cadvisor](https://github.com/google/cadvisor)：用于收集，聚合，处理和导出有关正在运行的容器的信息。
* [Grafana](https://grafana.com/grafana/)：指标图表分析展示平台，允许您查询，可视化，警报和了解指标。
* [influxDB](https://www.influxdata.com/)：时间序列存储数据库。(带时序的数据,一般用于物联网、日志、指标监控)
* [node-exporter](https://github.com/prometheus/node_exporter)：宿主机节点性能指标数据采集

## prometheus+cadvisor简单的性能指标采集展示框架

资源占用

* cadvisor:112M左右
* Prometheus:300M+(随时间流逝内存在上升)

### docker swarm模式部署

[官方部署文档](https://prometheus.io/docs/guides/cadvisor/)

prometheus的配置文件`/docker_data/v-monitor/prometheus/prometheus.yml`内容如下：

```yaml
scrape_configs:
- job_name: cadvisor
  scrape_interval: 5s
  static_configs:
  - targets:
    - cadvisor:8080
```

Swarm部署脚本

```yaml
version: '3.2'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
    - 9090:9090
    command:
    - --config.file=/etc/prometheus/prometheus.yml
    volumes:
    - /docker_data/v-monitor/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    depends_on:
    - cadvisor
  cadvisor:
    image: google/cadvisor:latest
    container_name: cadvisor
    ports:
    - 8080:8080
    volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:rw
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
```

### [prometheus容器指标](https://github.com/google/cadvisor/blob/master/docs/storage/prometheus.md#prometheus-container-metrics)

| 指标名称                     | 类型  | 含义                               |
| ---------------------------- | ----- | ---------------------------------- |
| container_memory_usage_bytes | gauge | 容器当前的内存使用量（单位：字节） |
| machine_memory_bytes         | gauge | 宿主机内存总量（单位：字节）       |

### 内存图表展示

[![ckwaAx.png](https://z3.ax1x.com/2021/03/31/ckwaAx.png)](https://imgtu.com/i/ckwaAx)

### 增加Grafana仪表板显示prometheus

[增加Grafana部署](https://grafana.com/docs/grafana/latest/installation/docker/)

```yaml
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
    - 3000:3000 
```

默认账号和密码是admin/admin

[官方配置手册GRAFANA SUPPORT FOR PROMETHEUS](https://prometheus.io/docs/visualization/grafana/)

1. 添加数据源：点击configuration->data sources->prometheus->在url输入pro服务的地址(http://prometheus:9090) 
2. 寻找合适的dashboard：去[grafana dashboard](https://grafana.com/grafana/dashboards?dataSource=prometheus&direction=desc&orderBy=downloads&category=docker)找一个适合自己的模版(我这里用[*Docker and system monitoring*](https://grafana.com/grafana/dashboards/893)的模版id为893)
3. 添加dashboard：点击dashboard->import->输入id添加模版(893)

### 增加[node-exporter](https://github.com/prometheus/node_exporter)宿主机节点数据采集

增加部署

```yaml
  node-exporter:
    image: prom/node-exporter:latest
    command:
      - '--path.rootfs=/host'
    pid: host
    volumes:
      - '/:/host:ro,rslave'    
    ports:
      - target: 9100
        published: 9100
        protocol: tcp
        mode: host
```

修改配置[prometheus.yml](/docker_data/v-monitor/prometheus/prometheus.yml)内容如下：

```yaml
scrape_configs:
- job_name: 'cadvisor' #不能随便修改名字，会造成数据的job name不一致查询时会查询出两组数据
  scrape_interval: 5s
  static_configs:
  - targets: ['localhost:9090','cadvisor:8080','node-exporter:9100']
```

### [QUERYING PROMETHEUS 语法](https://prometheus.io/docs/prometheus/latest/querying/basics/)

[中文文档](https://prometheus.fuckcloudnative.io/di-san-zhang-prometheus/di-4-jie-cha-xun/functions)

```sh
#node_filesystem_free_bytes代表查询的表名，{fstype="rootfs"}相当于查询条件，查询fstype是rootfs的所有数据,[1m]范围向量，一分钟内的数据
node_filesystem_free_bytes{fstype="rootfs"}[1m]
```

[![cEniNR.png](https://z3.ax1x.com/2021/04/01/cEniNR.png)](https://imgtu.com/i/cEniNR)

```sh
#name是容器名字

#容器名字容易统计死的容器，重启服务的时候，会有多个容器，但其实是一个服务，因此按服务名统计
sum(container_memory_rss{container_label_com_docker_swarm_service_name=~".+"}) by (container_label_com_docker_swarm_service_name)
#按服务名存在一个问题，因此可以通过image进行分组，但是存在后缀
sum(container_memory_rss{name=~".+"})by(image)
#可以去掉后缀,但是有的官方镜像后缀很难看
sum(label_replace(container_memory_rss{name=~".+"},"image_sub","$1","image", "(.*)(:)(.*)"))by(image_sub)
#因此最后采用label_replace方法，进行对原数据进行字段替换，
#label_replace(原数据,"新的字段名","取正则里面的那一部分","旧的字段名", "正则")，正则每一段都用()包裹，$1代表取第一个括号内容，2就代表第二个括号内容，用了括号才能用转义\\
label_replace(container_memory_rss{name=~".+"},"name","$1","name", "(.*)(\\.1\\.)(.*)")
#最终版本，旧的name和新的name要一致，因为有的正则匹配不到，旧的name的数据就会合为一体，就不会丢数据
sum(label_replace(container_memory_rss{name=~".+"},"name","$1","name", "(.*)(\\.1\\.)(.*)"))by(name)
#统计cpu，label_replace要在外面替换
sum(label_replace(rate(container_cpu_usage_seconds_total{name=~".+"}[$interval]),"name","$1","name", "(.*)(\\.1\\.)(.*)"))by (name) * 100
```

## cadvisor+influxDB+Grafana

待更新...



### 参考

[容器监控：cAdvisor](https://yunlzheng.gitbook.io/prometheus-book/part-ii-prometheus-jin-jie/exporter/commonly-eporter-usage/use-prometheus-monitor-container)

### 常见问题

1. 图表不显示数据,显示N/A，检查里面的查询语句，是否表改了名字，新版本好多表都加了`_bytes`后缀，找到升级后的表名替换旧的就可以了
2. 更新表的字段后显示`Only queries that return single series/table is supported`错误，检查右边的panel是否需要合并，不需要合并应该会选中一个图表类型

### 附录

完整的swarm部署文件

```yaml
version: '3.2'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
    - 14003:9090
    command:
    - --config.file=/etc/prometheus/prometheus.yml
    volumes:
    - /docker_data/v-monitor/prometheus/config:/etc/prometheus
    - /docker_data/v-monitor/prometheus/data:/prometheus
  cadvisor:
    image: google/cadvisor:latest
    ports:
    - 14004:8080
    volumes:
    - /:/rootfs:ro
    - /var/run:/var/run:rw
    - /sys:/sys:ro
    - /var/lib/docker/:/var/lib/docker:ro
  grafana:
    image: grafana/grafana:latest
    ports:
    - 14002:3000
    volumes:
    - /docker_data/v-monitor/grafana:/var/lib/grafana
  node-exporter:
    image: prom/node-exporter:latest
    command:
      - '--path.rootfs=/host'
    pid: host
    volumes:
      - '/:/host:ro,rslave'    
    ports:
      - target: 9100
        published: 9100
        protocol: tcp
        mode: host
```

[prometheus.yml](/docker_data/v-monitor/prometheus/prometheus.yml)

```yaml
scrape_configs:
- job_name: 'cadvisor' #不能随便修改名字，会造成数据的job name不一致查询时会查询出两组数据
  scrape_interval: 5s
  static_configs:
  - targets: ['localhost:9090','cadvisor:8080','node-exporter:9100']
```

