---
title: Docker集群之安装Kubernetes
date: 2017-09-14 10:07:37
categories: docker集群
tags: [集群,k8s,docker,kubectl,Minikube]
---
# kubectl安装

[kubectl](https://github.com/GoogleCloudPlatform/kubernetes) 是 Kubernetes 自带的客户端，可以用它来直接操作 Kubernetes。

###### 官方文档：[Install and Set Up kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### window平台（需要bash on ubuntu环境）

```powershell
#切换bash on Ubuntu命令
bash
#下载kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/windows/amd64/kubectl.exe
#退出bash
exit
#查看版本
.\kubectl.exe version
```

### Linux平台

```shell
#下载kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
#添加权限
chmod +x ./kubectl
#设置全局命令（环境变量）
sudo mv ./kubectl /usr/local/bin/kubectl
#检查安装成功与否
kubectl version
```

# Minikube安装

###### 官方文档[kubernetes/minikube](https://github.com/kubernetes/minikube/releases)

[virtualBox](https://www.virtualbox.org/wiki/Linux_Downloads)

### Linux

```shell
#安装配置minikube
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.22.1/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
#查看版本
minikube version
#下载virtualbox
wget http://download.virtualbox.org/virtualbox/5.1.26/VirtualBox-5.1-5.1.26_117224_el7-1.x86_64.rpm

```

### Windos

```powershell
#安装配置minikube
curl -Lo minikube.exe https://storage.googleapis.com/minikube/releases/v0.22.1/minikube-windows-amd64.exe
#查看版本
./minikube.exe version
```

### 。。。。。放弃，转用swarm ,已卸载相关下载文件

弃坑理由：安装负杂，需要安装虚拟机，对环境要求高，学习成本高，swarm和Kubernetes对dockers的差距越来越小

