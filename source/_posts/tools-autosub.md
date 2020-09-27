---
title: tools-autosub
date: 2020-09-19 21:42:41
updated: 2020-09-19 23:39:06
categories: Tools
tags: [autosub]
---

## AI字幕

参考[BingLingGroup](https://github.com/BingLingGroup)/**[autosub](https://github.com/BingLingGroup/autosub)**

### 安装

```bash
#一定要使用http代理，不能用socke5代理，错误详细信息见常见错误1
export all_proxy=http://127.0.0.1:58591
#一定要用pip3
#(废除有bug见错误2)pip3 install git+https://github.com/BingLingGroup/autosub.git@alpha ffmpeg-normalize langcodes
pip3 install git+https://github.com/BingLingGroup/autosub.git@dev ffmpeg-normalize langcodes
```

### 使用

```bash
#dcy1.wmv视频日语(ja-jp)生成中文(zh-cn)字幕
autosub -i dcy1.wmv  -S ja-jp -D zh-cn
#-o指定输出路径，不指定要卡住
autosub -i dcy1.wmv  -S ja-jp -D zh-cn -o /Users/xuanleung/Downloads/worldvideo/dcy1.zh-cn.srt
```



# 常见错误

### 错误1：

```bash
ERROR: Could not install packages due to an EnvironmentError: Missing dependencies for SOCKS support.
```

解决：原因是安装包不支持socks代理，两种解决方法，一是让它支持，二是采用http代理，这里用第二种方法解决，执行`export all_proxy=http://127.0.0.1:58591`

### 错误2：

```bash
    return value.encode(encoding or "ascii")
AttributeError: 'NoneType' object has no attribute 'encode'
```

解决：原因环境变量编码的问题，执行

```
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
```

上述还无法解决见[https://github.com/BingLingGroup/autosub/issues/127](https://github.com/BingLingGroup/autosub/issues/127)上面解决是在dev分支[2020.07.02](https://github.com/BingLingGroup/autosub/commit/d1133b37fcfc3ea03458063f73841dcbe732b483)提交的当时还没修复到alpha分支

```bash
#升级dev分支
pip3 install --upgrade git+https://github.com/BingLingGroup/autosub.git@dev
```



