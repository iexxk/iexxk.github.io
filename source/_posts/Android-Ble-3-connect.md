---
title: Ble蓝牙开发之三连接
date: 2016-08-24 17:31:57
categories: Android
tags: [Ble,连接]
---
# 蓝牙连接

### BluetoothGattCallback 回调
```java
android.bluetooth.BluetoothGattCallback BluetoothGattCallback = new BluetoothGattCallback() {
 //连接状态
 @Override
 public void onConnectionStateChange(BluetoothGatt gatt, int status, int newState)
 
 //遍历Services和characteristic
 @Override
 public void onServicesDiscovered(BluetoothGatt gatt, int status)
 
 //接收的数据改变时
 @Override
 public void onCharacteristicChanged(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic)
 
 //信号强度
 @Override
 public void onReadRemoteRssi(BluetoothGatt gatt, int rssi, int status)
 
 //写descriptor时的回调，status=0写成功
 @Override
 public void onDescriptorWrite(BluetoothGatt gatt, BluetoothGattDescriptor descriptor, int status)
 
 //写Characteristic时的回调，status=0写成功
 @Override
 public void onCharacteristicWrite(BluetoothGatt gatt, BluetoothGattCharacteristic characteristic, int status)
 
}
```
### 连接
```java
private BluetoothGatt mBluetoothGatt;
//连接服务 ，第二个参数设为true为自动连接，false不自动连接
mBluetoothGatt = mBluetoothDevice().connectGatt(context, true,BluetoothGattCallback);  
```

### 找到需要的characteristic，descriptor
在onServicesDiscovered回调里遍历所有Services，Characteristics
```java
//获得服务
 List<BluetoothGattService> serviceList = mBluetoothGatt.getServices();
//遍历服务
   for (BluetoothGattService gattService : serviceList) {
   //获得Characteristics
    List<BluetoothGattCharacteristic> characteristicList = gattService.getCharacteristics();
	    //遍历Characteristics
        for (BluetoothGattCharacteristic characteristic : characteristicList) {
					//判断存储自己需要的characteristic
		}
   }
```
### 读写UUID
如何找到读写的UUID号，可以用蓝牙助手，或者查看外围蓝牙设备文档
或者从权限判断。