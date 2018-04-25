---
title: Ble蓝牙开发之四读写数据
date: 2016-08-25 08:48:44
updated: 2018-04-25 20:47:32categories: Android
tags: [Ble,读写]
---
# 写数据（发送数据）
前提找到可写的characteristic，在onServicesDiscovered回调里查找
```java
 characteristic_W.setValue("string或者byte[]等");
  //写成功issucceed返回true
  boolean issucceed= mBluetoothGatt.writeCharacteristic(characteristic_W)
```

写完之后onCharacteristicWrite回调返回写的消息
```java
 @Override
 public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status)
```
### 其它的写同理
写的对应关系如下：
     写的操作      --->     对应的回调
writeCharacteristic--->onCharacteristicWrite
writeDescriptor    --->onDescriptorWrite

# 接收数据（使能通知）
```java
//characteristic_R接收数据的uuid
//使能characteristic_R的通知
mBluetoothGatt.setCharacteristicNotification(characteristic_R, true);
//未知，测试发现不能改
String UUIDDes = "00002902-0000-1000-8000-00805f9b34fb";
//从接收里获取descriptor
BluetoothGattDescriptor descriptor = characteristic_R.getDescriptor(UUID.fromString(UUIDDes)); 
//写数据到descriptor
descriptor.setValue(BluetoothGattDescriptor.ENABLE_NOTIFICATION_VALUE);
//发送给底层
mBluetoothGatt.writeDescriptor(descriptor);
```
使能接收数据每步都有状态返回，注意做好状态的判断，以确定是那一步失败
设置成功后，onDescriptorWrite会有回调消息
然后在onCharacteristicChanged的回调里旧可以接收到外围蓝牙设备发送的广播消息了
### 注意
向外围蓝牙设备写（发送）消息，_同一时间只能写一次_，最好是在在上次写完成之后才开始第二次

# 断开连接
```java
mBluetoothGatt.disconnect();
```