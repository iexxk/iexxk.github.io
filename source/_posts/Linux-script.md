---
title: linux脚本
date: 2017-12-29 17:25:52
categories: Linux
tags: [linux,脚本]
---
#### centos7开机脚本

1. 新建开机脚本`vim /root/Dropbox/save/bootstartscript.sh`

   ```sh
   #添加开机启动脚本
   #开机启动dropbox
   dropbox start -d
   ```

2. 添加开机脚本到启动文件`vim /etc/rc.d/rc.local`

   ```sh
   #开机启动脚本
   bash /root/Dropbox/save/bootstartscript.sh
   ```

3. 设置启动脚本生效` chmod +x /etc/rc.d/rc.local `