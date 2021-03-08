---
title: docker 配置 tls 安全远程连接
date: 2021-03-08 15:49:29
updated: 2021-03-08 16:20:58
categories: docker
tags: [docker]
---

## 说明

官方设置[Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/)

tls(https)安全连接是通过证书进行验证，因为连接协议是https，所以连接的时候端口变成了**2376**

阿里云开放端口: 2376

```bash
#服务端需要的文件
 "tlscacert": "/docker_data/cert/ca.pem",
 "tlscert": "/docker_data/cert/server-cert.pem",
 "tlskey": "/docker_data/cert/server-key.pem",
#客户端需要的文件
--tlscacert=/docker_data/cert/ca.pem 
--tlscert=/docker_data/cert/cert.pem 
--tlskey=/docker_data/cert/key.pem
```



### 生成证书

```bash
mkdir /docker_data/cert/
cd /docker_data/cert/
#生成ca证书ca-key.pem
openssl genrsa -aes256 -out ca-key.pem 4096
>Enter pass phrase for ca-key.pem: 设置密码
>Verifying - Enter pass phrase for ca-key.pem: 输入刚刚设置的密码

#根据ca-key.pem创建ca公钥ca.pem
openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
>Enter pass phrase for ca-key.pem:输入刚刚设置的密码
>Country Name (2 letter code) [XX]:CN
>State or Province Name (full name) []:guangzhou
>Locality Name (eg, city) [Default City]:guangzhou
>Organization Name (eg, company) [Default Company Ltd]:nantian
>Organizational Unit Name (eg, section) []:chanpingsanbu
>Common Name (eg, your name or your server's hostname) []:192.168.0.76(这个host似乎可以随便输入)
>Email Address []:
#生成服务key
openssl genrsa -out server-key.pem 4096

openssl req -subj "/CN=192.168.0.76" -sha256 -new -key server-key.pem -out server.csr

#这里在这个ip列表里面的ip，才能访问，例如通过阿里云外网ip进行访问，需要加入阿里云的外网ip，DNS似乎也已随便输入
echo subjectAltName = DNS:192.168.0.76,IP:192.168.0.76,IP:127.0.0.1,IP:47.119.116.142 >> extfile.cnf
echo extendedKeyUsage = serverAuth >> extfile.cnf

openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out server-cert.pem -extfile extfile.cnf

openssl genrsa -out key.pem 4096
openssl req -subj '/CN=client' -new -key key.pem -out client.csr
echo extendedKeyUsage = clientAuth > extfile-client.cnf
openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out cert.pem -extfile extfile-client.cnf 
```

修改`vim /etc/docker/daemon.json`文件

```json
{
    "registry-mirrors": ["https://registry.docker-cn.com"],
    "hosts": ["unix:///var/run/docker.sock", "tcp://192.168.0.76:2376"],
    "tls": true,
    "tlscacert": "/docker_data/cert/ca.pem",
    "tlscert": "/docker_data/cert/server-cert.pem",
    "tlskey": "/docker_data/cert/server-key.pem",
    "tlsverify": true
}
```

配置完成后重启docker

```bash
systemctl daemon-reload
systemctl restart docker.service
```



### 测试

```bash
#服务端测试
docker --tlsverify --tlscacert=ca.pem --tlscert=cert.pem --tlskey=key.pem -H=47.119.116.142:2376 version

#客户端测试,需要先从服务器拷贝这三个文件
curl https://47.119.116.142:2376/images/json --cert cert.pem --key key.pem --cacert ca.pem
```



#### portioner 连接



#### idea客户端连接方式

拷贝`ca.pem 、cert.pem、key.pem `三个文件到cert目录，然后idea指向cert目录，url用`https://ip:2376`

[![6lVZGV.png](https://s3.ax1x.com/2021/03/08/6lVZGV.png)](https://imgtu.com/i/6lVZGV)