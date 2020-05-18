---
title: Linux-Script-Shell
date: 2020-03-25 11:07:16
updated: 2020-03-26 17:07:34
categories: Linux
tags: [Linux,shell,script]
---

### 配置修改脚本

测试文件a.conf

```properties
sex=boy
age=8
url=http://www.baidu.com
    "systemUrl": "http://10.254.197.9:9304",
```

常用脚本命令

```shell
#查看包含sex的行
cat a.conf | grep sex
#替换sex=boy为sex=girl,-i为写入文件
sed -i "s/sex=boy/sex=girl/" a.conf
# 替换sex的值,\S用于匹配除单个空格符之外的所有字符,输出age=8
sed -i "s/age=\S*/age=9/" a.conf 
# 注释sex开头的配置，&代表任意字符
sed -i  's/^sex/;&/' a.conf 
# 取消注释
sed -i 's/^;\(sex\)/\1/' a.conf 
# 在age配置后加一行;this is age
sed -i '/age/a\;this is age' a.conf
# 在age配置前加一行;this is age
sed -i '/age/i\;this is age' a.conf
# 删除所有匹配;this is age的行
sed -i '/;this is age/d'  a.conf
# 修改url,如果url里面有空格会失败，因为S匹配非空格
sed -i "s/url=\S*/url=http:\/\/www.baidu.com/" a.conf 
# 替换ip
sed -i "s/10.254.197.9/127.0.0.1/" a.conf
# 匹配行头，然后替换整行,适用于包含空格的格式  '/^行头/c\整行替换的值' 加反斜杠\是为了区分内容可省略
sed -i '/^url/c\url = 2' a.conf
```

