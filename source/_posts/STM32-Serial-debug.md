---
title: STM32-Serial-debug
date: 2018-07-29 11:14:20
updated: 2018-07-29 11:14:20
categories: STM32
tags: [STM32,NUCLEO,mbed]
---

## mac stm32串口调试

### 方式一（使用mbed os但是不是集成板子，需要更改很多配置）

1. [mbed](https://os.mbed.com/compiler/#nav:/Nucleo_printf/main.cpp;)是一个在线编辑编译代码的工具,上面有很多源码下载里面项目[ST/Nucleo_printf](https://os.mbed.com/teams/ST/code/Nucleo_printf/),点击编译，下载bin文件
2. 将下载的bin文件写入开发板，执行`st-flash write Nucleo_printf_NUCLEO_F401RE.bin 0x8000000`
3. 打开**CLion**软件在插件管理界面添加[Serial Port Monitor](https://bitbucket.org/dmitry_cherkas/intellij-serial-monitor)
4. 然后在左下角**Serial Monitor**点击设置，选择**usbmodem**，设置波特率**9600**，就可以看到打印的hello world

### 方式二（Cubemx）：使用hal库函数进行串口输出

串口发送(在main函数添加)：

```c
//把"hello world"的内容通过uart2发送出去，长度是11，timeout的时间是最大值0xffff
HAL_UART_Transmit(&huart2, "hello world", 11,0xFFFF);
```







### 参考

[STM32L0 HAL库 UART 串口读写功能](https://www.cnblogs.com/Mysterious/p/4804188.html)

[【STM32CubeMX】HAL库中断方式UART串口通信](https://blog.csdn.net/cayloon/article/details/79196942)