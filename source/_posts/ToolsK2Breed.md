---
title: Tools-k2-breed
date: 2018-03-22 23:15:32
updated: 2018-12-12 10:47:58
categories: 工具
tags: [k2路有器,工具]
---

#### [斐讯K2 22.4.6.3 非telnet 页面直刷 Breed 详细方法（图文）](http://www.right.com.cn/forum/forum.php?mod=viewthread&tid=204435&highlight=k2%252B22.4.6.3)

1. 用网线连接电脑和路由器的lan口

2. 保持路由器与internet的连通(桥接，有线都可以)

3. 进入k2管理页面（p.to）

4. 进入网页调试模式(chrome按F12)，找到定时重启下拉05分的标签

5. 在05的标签右键编辑

6. 将“05”修改成为“05 | wget http://breed.hackpascal.net/breed-mt7620-phicomm-psg1208.bin”之后，鼠标移动到黑框外的空白处点击鼠标左键，结束编辑。

7. 回到页面重新选择05，05后面多了刚刚加的，然后保存。

8. 继续将“05”修改成“05 | mtd unlock Bootloader”，然后回到页面选择05保存。

9. 继续将“05”修改成“05 | mtd -r write breed-mt7620-phicomm-psg1208.bin Bootloader”，然后回到页面选择05保存，等待重启，如果未重启代表失败。

10. 拔除K2上Wan口的网线，路由器断电，持续按住路由器上的reset按钮，接通路由器电源，3秒后松开reset按钮。

11. 在浏览器地址栏输入“http://192.168.1.1”访问Breed Web。

    #### 注意：下次刷机只需进入brend ，步骤为

    1. 路由器断电，持续按住路由器上的reset按钮，接通路由器电源，3秒后松开reset按钮。
    2. 在浏览器地址栏输入“http://192.168.1.1”访问Breed Web。

    [RT-AC54U-GPIO-1-PSG1218-64M_3.4.3.9-099.trx](F:\xuan install.Back\K2.Back)  访问ip:http://192.168.123.1/ 管理账号：admin/admin wifi密码:1234567890

    高级设置-外部网络-外网连接类型pppoe拨号，用户名密码输入宽带账号密码，闪讯拨号插件选择重庆，其他默认，然后应用本页设置
    高级设置-系统管理-ntp服务器 分别填入红岩网校的ntp服务器202.202.43.120 202.202.43.131 手动设置时间 应用本页设置
    网络地图-点击地球的图标-重新连接 应该可以上网了

    参考http://www.tieba.com/p/5015549863

###### 方法2

[斐讯K2 V22.5.9.163官方固件定制版,集成breed,支持官版直刷【V1.4】](http://www.right.com.cn/forum/thread-208753-1-1.html)

直接手动升级`k2_163_v14_breed.bin`然后进入breed