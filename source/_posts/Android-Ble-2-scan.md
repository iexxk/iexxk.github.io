---
title: Ble蓝牙开发之二搜索
date: 2016-08-24 16:35:45
categories: Android
tags: [Ble,搜索]
---
# 添加权限
```xml
	<!-- 低功耗蓝牙权限 -->
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
	<!-- 是否只允许BLE蓝牙 -->
    <uses-feature
        android:name="android.hardware.bluetooth_le"
        android:required="false" />
```

# 蓝牙初始化
检测是否支持蓝牙，返回true支持
```
getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)
```
打开蓝牙
```java
//获取蓝牙
 final BluetoothManager bluetoothManager =(BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
       mBluetoothAdapter = bluetoothManager.getAdapter();
    // 2.Enable Bluetooth 检测用户是否打开蓝牙并提示用户打开
	   if (mBluetoothAdapter == null || !mBluetoothAdapter.isEnabled()) {	
			Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
			startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);
	    }
```
# 搜索蓝牙
Ble蓝牙搜索功能在 android5.1(api 21)时发生了变化，有过滤，有扫描设置等很不错的功能
### api 21：
可以配置过滤器，设置搜索模式

```java
startScan(List<ScanFilter> filters, ScanSettings settings, ScanCallback callback)
stopScan(ScanCallback callback)
```

三个回调，如果不关闭搜索onScanResult一直回返回结果
要进入onBatchScanResults回调，必须设置搜索时间setReportDelay(5000)，时间到了一起返回

```java
@Override
public void onScanResult(int callbackType, ScanResult result)
 @Override
public void onBatchScanResults(List<ScanResult> results)
  @Override
public void onScanFailed(int errorCode) 
```

### api 18：

```java
startLeScan(BluetoothAdapter.LeScanCallback callback)
stopLeScan(BluetoothAdapter.LeScanCallback callback)
```

一个回调
```java
  @Override
  public void onLeScan(BluetoothDevice bluetoothDevice, int rssi, byte[] bytes)
```
# 注意

不管是新api搜索，还是旧的都要注意停止搜索，还有最好做好兼容，两种搜索都写,版本判断
```
  if(Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP)
```