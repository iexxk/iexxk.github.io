---
title: github博客之更新完善
date: 2017-12-07 18:16:37
updated: 2018-04-25 20:47:32categories: 杂谈
tags: [github,hexo,Travis,WSL]
---

### wsl安装[nodejs8.x](https://nodejs.org/en/download/)

```shell
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install nodejs
```

### wsl安装[hexo-cli](https://hexo.io/zh-cn/docs/)

```shell
cd /mnt/f/
sudo npm install -g hexo-cli
hexo --version #1.0.4
hexo init hexo && cd hexo
hexo new hello #创建新文章
hexo g #生产静态页面
hexo s #启动本地测试服务
```

### hexo安装next主题

```shell
git clone https://github.com/iissnan/hexo-theme-next themes/next
#复制next主题到hexo\themes目录下，修改配置文件_config.yml中的theme为next
hexo clean
hexo g && hexo s
```



### hexo引入[gitment](https://github.com/imsun/gitment)评论

参考：[Gitment：使用 GitHub Issues 搭建评论系统](https://imsun.net/posts/gitment-introduction/)

简介：[Gitment](https://github.com/imsun/gitment) 是作者实现的一款基于 GitHub Issues 的评论系统。

`hexo\themes\next\_config.yml`

```properties
  #菜单
  tags: /tags/ || tags
  updated: 2018-04-25 20:47:32categories: /categories/ || th
  #样式
  scheme: Pisces
  #评论
  gitment:
  enable: true
  mint: true # RECOMMEND, A mint on Gitment, to support count, language and proxy_gateway
  count: true # Show comments count in post meta area
  lazy: false # Comments lazy loading with a button
  cleanly: false # Hide 'Powered by ...' on footer, and more
  language: # Force language, or auto switch by theme
  github_user: xuanfong1 # MUST HAVE, Your Github ID
  github_repo: hexo # MUST HAVE, The repo you use to store Gitment comments
  client_id: ff47a05197bc142b8dc0 # MUST HAVE, Github client id for the Gitment
  client_secret: b52d05ee5566230edfcf653efab9fd9fce6756c8 # EITHER this or proxy_gateway, Github access secret token for the Gitment
  proxy_gateway: # Address of api proxy, See: https://github.com/aimingoo/intersect
  redirect_protocol: # Protocol of redirect_uri with force_redirect_protocol when mint enabled
```



### [Hexo配置](https://hexo.io/docs/deployment.html)和[next主题配置](http://theme-next.iissnan.com/theme-settings.html#fonts-customization)