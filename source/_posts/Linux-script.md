---
title: Linux-script
date: 2019-06-04 15:19:29
updated: 2019-06-04 16:16:20
categories: Linux
tags: [script]
---

##### 单行语法

```bash
cmd1 && cmd2 #cmd1正确执行cmd2，相反不执行
cmd1 || cmd2 #cmd1错误执行cmd2，相反不执行
```

##### 错误重定向不输出

```bash
cmd 1>/dev/null 2>&1 #错误不会打印
```

#### 实战

```bash
#用户bpf不存在则创建用户，且不输出错误日志,但异常还是存在所以可能会导致整个脚本终止
id bpf 1>/dev/null 2>&1 || useradd bpf -d /opt/bpf/
#方式2
if id bpf1 >/dev/null 2>&1; then echo 11; fi
#方式3（推荐），不会被推出，因为没有异常，经测试还是被退出
cat /etc/passwd | cut -f1 -d':' | grep -w "bpf" -c || useradd bpf -d /opt/bpf/
```

#### 优化

```xml
<! maven pom.xml & 符号报错，解决用<![CDATA[ cmd ]]> -->
<script><![CDATA[id bpf 1>/dev/null 2>&1 || useradd bpf -d /opt/bpf/]]></script>
```

