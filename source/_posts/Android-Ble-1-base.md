---
title: Ble蓝牙开发之一认识
date: 2016-08-18 16:49:00
updated: 2018-01-28 21:41:27categories: Android
tags: [Ble,基础]
---

# 初步认识
>* Ble蓝牙是指低功耗蓝牙，在android4.3(api 18)以上理论都是兼容的

# Ble两种角色
>* 中心设备
>* 外围设备

## 关系
中心设备扮演扫描的角色，寻找外围设备的广播消息。

# Ble 名词解释
>* ScanResult 扫描蓝牙设备的结果（api21才有）
>* BluetoothDevice 蓝牙设备
>* BluetoothGatt作为中央来使用和处理数据

# Ble三大部分
>* Service 服务（系统服务、用户服务....）
>* Characteristic 特征
>* Descriptor ：用于描述characteristic的信息或属性

## 共同点：都拥有不同的UUID

## 关系: 
>* 一个ble设备有多个Service
>* 一个Service有多个Characteristic
>* 一个Characteristic包含一个value和多个Descriptor
>* 一个Descriptor包含一个value
>* 一个value存储的最大数据长度为20byte,大于20byte自动分包

## Characteristic权限
READ、WRITE、NOTIFY、WRITE_NO_RESPONSE是否有读，写，通知的权限

# 开发流程
1. 外围设备开机
2. 使能中心设备蓝牙
3. 添加蓝牙权限
4. 扫描外围设备（discover）
5. 连接外围设备（connect）
6. 扫描外围设备的服务和特征 （discover）
7. 获取数据（读取外围设备的数据）
  7.1 Service->Characteristic-getValue()
  7.2 Service->Characteristic-getDescriptor-getValue()
8. 写入数据（向外围设备发送数据）
  8.1 BluetoothGatt.writeCharacteristic(Characteristic.setValue("写入的数据"))
  8.2 BluetoothGatt.writeDescriptor(Descriptor.setValue("写入的数据"))
9. 订阅通知（接收外围设备广播的数据）
  9.1 Service->Characteristic-getDescriptor->BluetoothGatt.writeDescriptor(Descriptor.setValue("特点的值"))
10. 断开连接（disconnect）


