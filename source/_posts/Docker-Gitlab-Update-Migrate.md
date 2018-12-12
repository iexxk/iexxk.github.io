---
title: Docker-Gitlab-Update-Migrate
date: 2018-07-26 08:20:44
updated: 2018-07-26 08:20:44
categories: Docker
tags: [Docker,Gitlab]
---

### gitlab 升级迁移

#### 方式一：挂在卷复制迁移（镜像版本相同）

直接复制所有挂在卷，但是有可能出现问题1

#### 方式二：备份打包迁移

注意：`docker-compose.yml`里面的镜像版本要和之前的版本一致

更多rake命令具体看官网

1. gitlab停止运行，并删除挂掉的容器（未成功，因为存在问题1）

   ```sh
   #创建备份
   docker-compose run --rm gitlab app:rake gitlab:backup:create
   #恢复备份
   docker-compose run --rm gitlab app:rake gitlab:backup:restore
   ```

2. gitlab运行的情况

   ```sh
   #查看环境信息
   docker-compose exec --user git gitlab bundle exec rake gitlab:env:info RAILS_ENV=production
   #创建备份（采用）
   docker-compose exec --user git gitlab bundle exec rake gitlab:backup:create RAILS_ENV=production
   #查看备份
   docker-compose exec --user git gitlab bundle exec rake gitlab:backup:restore RAILS_ENV=production
   #恢复备份
   docker-compose exec --user git gitlab bundle exec rake gitlab:backup:restore BACKUP=1532580339_2018_07_26_10.7.3 RAILS_ENV=production
   ```

#### 方式四

进入gitlab容器执行

```sh
#恢复
/sbin/entrypoint.sh app:rake gitlab:backup:restore
#备份
/sbin/entrypoint.sh app:rake gitlab:backup:create
```



```bash
Starting the gitlab container
Enter the gitlab's bash shell
Execute /sbin/entrypoint.sh app:rake gitlab:backup:restore to restore a backup
When restore finish, just restart gitlab container, and all is done.
For backup procedure, simply execute /sbin/entrypoint.sh app:rake gitlab:backup:create command when you're in gitlab container's shell.
```

### 问题

1. 迁移时，重启时,报500错误,日志提示

   ```verilog
   2018-07-26 05:53:41,648 INFO spawned: 'sidekiq' with pid 1066,
   2018-07-26 05:53:42,649 INFO success: sidekiq entered RUNNING state, process has stayed up for > than 1 seconds (startsecs),
   2018-07-26 05:53:50,996 INFO exited: sidekiq (exit status 1; not expected),
   2018-07-26 05:53:51,998 INFO spawned: 'sidekiq' with pid 1075,
   2018-07-26 05:53:52,999 INFO success: sidekiq entered RUNNING state, process has stayed up for > than 1 seconds (startsecs),
   ```

   具体原因进入容器`cat /var/log/gitlab/gitlab/production.log`查看日志，内容如下

   ```verilog
   Redis::CommandError (DENIED Redis is running in protected mode because protected mode is enabled, no bind address was specified, no authentication password is requested to clients. In this mode connections are only accepted from the loopback interface. If you want to connect from external computers to Redis you may adopt one of the following solutions: 1) Just disable protected mode sending the command 'CONFIG SET protected-mode no' from the loopback interface by connecting to Redis from the same host the server is running, however MAKE SURE Redis is not publicly accessible from internet if you do so. Use CONFIG REWRITE to make this change permanent. 2) Alternatively you can just disable the protected mode by editing the Redis configuration file, and setting the protected mode option to 'no', and then restarting the server. 3) If you started the server manually just for testing, restart it with the '--protected-mode no' option. 4) Setup a bind address or an authentication password. NOTE: You only need to do one of the abovethings in order for the server to start accepting connections from the outside.):
     lib/gitlab/middleware/multipart.rb:95:in `call'
     lib/gitlab/request_profiler/middleware.rb:14:in `call'
     lib/gitlab/middleware/go.rb:17:in `call'
     lib/gitlab/etag_caching/middleware.rb:11:in `call'
     lib/gitlab/middleware/read_only/controller.rb:28:in `call'
     lib/gitlab/middleware/read_only.rb:16:in `call'
     lib/gitlab/request_context.rb:18:in `call'
     lib/gitlab/metrics/requests_rack_middleware.rb:27:in `call'
     lib/gitlab/middleware/release_env.rb:10:in `call'
     config.ru:23:in `block (2 levels) in <main>'
     config.ru:31:in `<main>'
   ```

   解决：从日志可以看出是安全原因，因此进入redis容器执行`redis-cli`然后执行命令`CONFIG SET protected-mode no`到此就可以了，这样更改下次重启又会失效，如果要永久生效，多执行一条`CONFIG REWRITE`,但是删除死掉的容器会失效

2. redis版本过高，初始化时用低版本，`latest`如果时最新的存在权限问题也就是问题1

   解决，重新用指定版本号`3.0.6`的docker-compose启动，然后redis容器挂在卷下的`dump.rdb`单独复制进去，如果存在权限问题，把旧的删了，重新复制进去，然后在redis容器`/var/lib/redis/`执行`chown redis:redis -R dump.rdb`

### 总结数据升级麻烦



### 参考

[GitLab升级失败恢复](https://hearrain.com/gitlab-sheng-ji-shi-bai-hui-fu)

[sameersbn/gitlab官方Rake Tasks](https://hub.docker.com/r/sameersbn/gitlab/#creating-backups)

https://github.com/sameersbn/docker-gitlab/issues/1655