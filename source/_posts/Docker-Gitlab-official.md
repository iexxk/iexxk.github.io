---
title: Docker-Gitlab-official
date: 2018-07-27 13:43:28
updated: 2020-05-18 14:19:15
categories: Docker
tags: [Docker,Gitlab]
---

### 官方版gitlab安装使用

[官网教程](https://docs.gitlab.com/omnibus/docker/)

`docker-statck.yml`文件

```yaml
version: "3.6"
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    ports:
      - "14020:22"
      - "14018:80"
#https      - "14019:443"
    volumes:
      - /dockerdata/v-gitlab-ce/data:/var/opt/gitlab
      - /dockerdata/v-gitlab-ce/logs:/var/log/gitlab
      - /dockerdata/v-gitlab-ce/config:/etc/gitlab
    environment:
      GITLAB_OMNIBUS_CONFIG: "from_file('/omnibus_config.rb')"
    configs:
      - source: gitlab_rb
        target: /omnibus_config.rb
    secrets:
      - gitlab_root_password
  gitlab-runner:
    image: gitlab/gitlab-runner:alpine
    deploy:
      mode: replicated
      replicas: 1
configs:
  gitlab_rb:
    external: true
secrets:
  gitlab_root_password:
    external: true
```

portainer->config->name: `gitlab_rb`

```yaml
external_url 'http://192.168.1.230:14018/'
#这里必须设置监听为80，因为是监听容器内的端口
nginx['listen_port'] = 80
#这里要设置ssh端口，不然ssh不能使用
gitlab_rails['gitlab_shell_ssh_port'] = 14020
gitlab_rails['initial_root_password'] = File.read('/run/secrets/gitlab_root_password')
gitlab_rails['time_zone'] = 'Asia/Shanghai'
#cron时间表达式每天三点
gitlab_rails['backup_cron'] = '0 0 3 * * ?'
# 默认备份目录/var/opt/gitlab/backups
# gitlab_rails['backup_path'] = '/var/opt/gitlab/backups'
# limit backup lifetime to 7 days - 604800 seconds
gitlab_rails['backup_keep_time'] = 604800

# ----优化内存配置-------------
#数据库缓存大小
postgresql['shared_buffers'] = "256MB"
#数据库并发
postgresql['max_worker_processes'] = 6
#进程数
unicorn['worker_processes'] = 2
#
unicorn['worker_memory_limit_min'] = "200 * 1 << 20"
unicorn['worker_memory_limit_max'] = "300 * 1 << 20"
#减少并发
sidekiq['concurrency'] = 10



```

portainer->secrets->name: `gitlab_root_password`

```yaml
MySuperSecretAndSecurePass0rd!
```

登陆时用户名为`root`，密码为`gitlab_root_password`的内容

### 备份

```sh
docker exec -t <your container name> gitlab-rake gitlab:backup:create
```

### 恢复

`1550500433_2019_02_18_11.6.2_gitlab_backup.tar`文件名分析

`11.6.2`gitlab版本号，备份还原版本号要一致

`1550500433_2019_02_18_11.6.2`备份文件编号

```bash
# 移动到目录/var/opt/gitlab/backups并修改权限
chmod 777 1550500433_2019_02_18_11.6.2_gitlab_backup.tar
#进入容器执行
gitlab-rake gitlab:backup:restore BACKUP=1550500433_2019_02_18_11.6.2
#同意几个yes
```

### 重置管理员密码

进入容器执行

```bash
gitlab-rails console production
#进入console,查询用户1的用户名，@符号后面为用户名
irb(main):004:0> user = User.where(id:1).first
=> #<User id:1 @root>
#重置密码为xxxx
irb(main):005:0> user.password = 'xxxx'
=> "xxxx"
#保存设置
irb(main):006:0> user.save!
Enqueued ActionMailer::DeliveryJob (Job ID: efc41db4-43bb-4f0f-83ca-7481611c2ff4) to Sidekiq(mailers) with arguments: "DeviseMailer", "password_change", "deliver_now", #<GlobalID:0x00007fea66e486f0 @uri=#<URI::GID gid://gitlab/User/1>>
=> true
```

到此用root用户登录即可

## 定时备份

```bash
docker exec -t $(docker ps | grep "gitlab_mygitlab" | awk '{ print $1 }') gitlab-backup create
#对于GitLab 12.1和更早版本，请使用
docker exec -t $(docker ps | grep "gitlab_mygitlab" | awk '{ print $1 }')  gitlab-rake gitlab:backup:create
## 添加定时任务
crontab -e
# i进行编辑，esc然后:wq
0  4  *  *  *  docker exec -t $(docker ps | grep "gitlab_mygitlab" | awk '{ print $1 }') gitlab-backup create
## 然后查看
crontab -l
```



### centos7 crontab 定时任务

```bash
# （查看状态）
systemctl status crond
# （设为开机启动）
systemctl enable crond
# （启动crond服务）
systemctl start crond
#添加定时任务
crontab -e
#查看定时任务
crontab -l
#删除当前用户的定时任务
crontab -r
```

备份会有如下警告：

因为配置文件和密码文件需要自己手动备份，为了数据安全

```bash
Warning: Your gitlab.rb and gitlab-secrets.json files contain sensitive data
and are not included in this backup. You will need these files to restore a backup.
Please back them up manually.
```





### 额外

1. 进入容器可以执行命令`gitlab-rake gitlab:env:info`更多命令见rake
2. 备份文件`repositories`中`xxx.bundle`可以用git命令解压`git clone xxx.bundle xxx`,详情见`git bundle`打包

## 参考

[gitlab.rb配置文件](https://gitlab.com/gitlab-org/omnibus-gitlab/blob/master/files/gitlab-config-template/gitlab.rb.template)

