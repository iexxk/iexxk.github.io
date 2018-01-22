---
title: linux脚本
date: 2017-12-29 17:25:52
categories: Linux
tags: [linux,脚本]
---
## shell基础知识

```bash
#文件名cp.sh
#!/bin/bash
exec cp "$@"
```

eg:

比如对于cp命令来说 cp src dist
那么\$1就是src \$2就是disc ,而$@就是所有的参数列表，src dist。

执行脚本`cp.sh src dist`=`exec cp src dist`

###### dockerfile中的应用

```dockerfile
#应用运行前执行的脚本
ENTRYPOINT ["/cp.sh","第二个脚本内容","....."]
#启动容器前执行的命令
CMD ["src", "dist", "第三个参数","......"]
```

等效于shell命令的 `/cp.sh src dist`=`exec cp src dist`

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