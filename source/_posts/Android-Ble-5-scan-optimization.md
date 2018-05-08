---
title: Ble蓝牙开发之五扫描与连接速度优化
date: 2016-08-30 09:06:44
updated: 2018-04-25 20:47:32categories: Android
tags: [Ble,优化]
---
# 扫描模式

### ScanSettings的属性与方法
```java
ScanSettings settings = new ScanSettings.Builder()
      //设置扫描模式（SCAN_MODE_LOW_LATENCY扫描优先，SCAN_MODE_LOW_POWER省电优先，SCAN_MODE_BALANCED平衡模式,SCAN_MODE_OPPORTUNISTIC安卓6.0里面才用的模式）
                .setScanMode(ScanSettings.SCAN_MODE_OPPORTUNISTIC)
        //设置扫描的时间，设置了这一项，将扫描5秒，然后在onBatchScanResults里面回调
                .setReportDelay(5000)
            //android 6.0可用
                .setMatchMode(1)
            //android 6.0可用
                .setCallbackType(1)
            //android 6.0可用
                .setNumOfMatches(1)
                .build();
```