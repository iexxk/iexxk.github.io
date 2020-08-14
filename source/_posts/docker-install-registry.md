---
title: Docker安装Registry
date: 2018-01-24 16:17:37
updated: 2018-12-12 10:47:58
categories: Docker
tags: [集群,Swarm,Docker,registry]
---
### [Registry](https://hub.docker.com/_/registry/)官网

### 本地仓库安装无绑定oss

1. [htpasswd](http://www.awesometool.org/Generate/Htpasswd)网页生成密码保存到`./auth/htpasswd`，加密方式选中**bcrypt**，或者执行命令生成`htpasswd -Bbn test 123456 > auth/htpasswd`

2. 编辑`vim docker-compose.yml`

   ```properties
   registry:
     restart: always
     image: "registry:2.6.2"
     ports:
       - 14005:5000
     environment:
       - REGISTRY_AUTH=htpasswd #授权模式
       - REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm
       - REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd #密码的地址
     volumes:
       - ./auth:/auth #密码存储的挂载卷
       - ./data:/var/lib/registry #本地仓库挂载的卷
   ```

3. 启动容器`docker-compose up`

4. 创建镜像`docker tag <镜像名字> 127.0.0.1:14005<镜像名字>`

5. 登陆仓库`docker login 127.0.0.1:14005`输入账号密码或者`docker login -u admin -p 123456 127.0.0.1:14005`

6. 上传镜像`docker push 127.0.0.1:14005<镜像名字>` 或者拉取镜像`docker pull 127.0.0.1:14005<镜像名字>`

### 绑定oss

1. 修改上面的第6步骤

   ```properties
   registry:
     restart: always
     image: "registry:2.6.2"
     ports:
       - 14005:5000
     environment:
       - REGISTRY_AUTH=htpasswd
       - REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm
       - REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd
       - REGISTRY_STORAGE=oss #必填
       - REGISTRY_STORAGE_OSS_ACCESSKEYID=你的阿里云ACCESSKEYID，带oss权限 #必填
       - REGISTRY_STORAGE_OSS_ACCESSKEYSECRET=你的阿里云ACCESSKEYSECRET，带oss权限 #必填
       - REGISTRY_STORAGE_OSS_REGION=节点区域（oss-cn-hangzhou） #必填
       - REGISTRY_STORAGE_OSS_BUCKET=buket的名字（t-docker-registry） #必填
       - REGISTRY_STORAGE_OSS_ENDPOINT=t-docker-registry.oss-cn-hangzhou.aliyuncs.com #非必填
     volumes:
       - ./auth:/auth
   ```

2. 如果报如下错误

   ##### 参考[Private registry push fail: server gave HTTP response to HTTPS client](https://github.com/docker/distribution/issues/1874)

   ```shell
   Error response from daemon: received unexpected HTTP status: 503 Service Unavailable
   #或者
   Error response from daemon: login attempt to http://127.0.0.1:14005/v2/ failed with status: 503 Service Unavailable
   #或者
   Error response from daemon: Get https://112.74.51.136:14005/v2/: http: server gave HTTP response to HTTPS client
   ```

   设置`vim /etc/docker/daemon.json`

   ```json
   {
     //这句是仓库加速地址，以前的
     "registry-mirrors": ["your aliyun 加速地址"],
     //添加这句,只有通过这个ip访问才不报错，如果有其他ip访问，也要加进来，不然就不用那个ip访问
     "insecure-registries":["112.74.51.136:14005"]
   }
   ```

   然后`sudo systemctl daemon-reload`重启`systemctl restart docker`

   ###### 幻觉：失败了一次，重启又可以了？

### docker registry 证书配置 

部署配置

```
  registry:
    restart: always
    image: "registry:2.6.2"
    ports:
      - 14005:5000
    environment:
      - REGISTRY_AUTH=htpasswd #授权模式
      - REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm
      - REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd #密码的地址
      - REGISTRY_HTTP_TLS_KEY=/certs/domain.key
      - REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt
    volumes:
      - /dockerdata/v-registry/auth:/auth #密码存储的挂载卷
      - /dockerdata/v-registry/registry:/var/lib/registry #本地仓库挂载的卷
      - /dockerdata/v-registry/certs:/certs #https
```

 在`/dockerdata/v-registry/`生成证书,注意在hostname设置时，不要忽略www

```bash
[root@environment-test1 v-registry]# sudo mkdir -p certs && sudo openssl req -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key -x509 -days 365 -out certs/domain.crt
Generating a 4096 bit RSA private key
...........................................................++
..++
writing new private key to 'certs/domain.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:CN
State or Province Name (full name) []:
Locality Name (eg, city) [Default City]:
Organization Name (eg, company) [Default Company Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server's hostname) []:www.3sreform.com
Email Address []:
```

再各个使用仓库的宿主机创建目录`mkdir -p /etc/docker/certs.d/www.3sreform.com:14005 `

然后把生成的证书放到该目录下并改名为`ca.crt`

最后重启docker

`sudo systemctl daemon-reload`和`sudo systemctl restart docker`

最后用`docker login www.3sreform.com:14005 -u admin -p <密码>`测试

最后push是，镜像开头必须是`www.3sreform.com`



#### 参考

[Docker搭建registry 私人仓库](https://www.jianshu.com/p/55ee4b6a72b6)