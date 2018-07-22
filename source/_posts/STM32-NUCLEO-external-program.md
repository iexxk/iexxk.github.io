---
title: STM32-NUCLEO-external-program
date: 2018-07-22 10:45:12
updated: 2018-07-22 10:45:12
categories: STM32
tags: [STM32,NUCLEO]
---

## NUCLEO板子对外部stm32进行编程下载

### 环境

1. NUCLEO-F401RE板子
2. stm32f103rb核心板（源地）
3. 软件环境见[STM32-Dev-Mac](https://blog.iexxk.com/2018/06/18/STM32-Dev-Mac/)

### [步骤](https://jingyan.baidu.com/article/9989c746e54ee7f648ecfe9c.html)

1. 硬件连线,[拔掉NUCLEO板子上的CN2两个跳线帽](https://www.st.com/content/ccc/resource/technical/document/user_manual/98/2e/fa/4b/e0/82/43/b7/DM00105823.pdf/files/DM00105823.pdf/jcr:content/translations/en.DM00105823.pdf)，然后连接CN4到编程的目标板(stm32f103rb核心板)，电源不连单独供电，连接图如下

   | NUCLEO     | 从上(SWD)到下(CN4) | 目标板 | 描述           |
   | ---------- | ------------------ | ------ | -------------- |
   | VDD_TARGET | 1                  |        | vdd电源        |
   | SWCLK      | 2                  | SWDCLK | 时钟           |
   | GND        | 3                  | GND    | 地             |
   | SWDIO      | 4                  | SWDIO  | 数据输入/输出  |
   | NRST       | 5                  |        | 目标MCU的RESET |
   | SWO        | 6                  |        | 保留           |

   ![](http://ohdtoul5i.bkt.clouddn.com/DSC_0592.JPG)

2. 打开STM32CubeMX软件，新建个工程，这里直接选STM32F103RBTx的NUCLEO套版，这里直接在这个套版上基础修改

3. 设置led输出引脚：在pinout引脚设置界面去掉PA5，修改PC13为`GPIO_Output`输出，并打上`LED`用户标签

   ![](http://ohdtoul5i.bkt.clouddn.com/QQ20180722-105903.png)

4. 修改时钟引脚设置，由于自己的板子用的高速时钟(HSE)和低速时钟(LSE)都用的外部时钟，所以这里切换时钟模式都为外部(Crystal)

   ![QQ20180722-110145](/Users/xuanleung/Downloads/QQ20180722-110145.png)

   ![QQ20180722-105957](/Users/xuanleung/nustore/xuanfong1.github.io/source/_posts/image/src_dir/QQ20180722-105957.png)

5. 修改时钟配置，修改晶振频率和自己板子一致，并且换成外部，然后设置倍数，如果倍数设置高于频率，会提示红报错，选择可用最高倍数即可，该板子只能选`X9`

   ![QQ20180722-110120](/Users/xuanleung/nustore/xuanfong1.github.io/source/_posts/image/src_dir/QQ20180722-110120.png)

6. 最后生成makerfile类型工程

7. 修改`Makefile`文件，`C_SOURCES`去重,`BINPATH`设置路径`/usr/local/bin/`

8. 在`main.c`添加led流水灯代码,引脚的名称注意用刚刚设置的标签名字

   ```c
     /* USER CODE END WHILE */
   
     /* USER CODE BEGIN 3 */
       HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_RESET);
       HAL_Delay(500);
       HAL_GPIO_WritePin(LED_GPIO_Port, LED_Pin, GPIO_PIN_SET);
       HAL_Delay(1000);
   ```

9. 编译`make`下载`st-flash write ./build/<项目名>.bin 0x8000000`

###使用CLion进行项目编译运行

1. `build->OpenOCD Support->board config file`:`st_nucleo_f103rb.cfg`
2. 编译运行手动按reset

注意：使用openocd时，NRST一定要连！

但是：没有线引出来无法连接，所以运行时立马手动按reset键也可以成功。



### 参考

[ STM32Cube工具学习笔记（一）Cube配置](https://blog.csdn.net/JiaLiang_825/article/details/78875328)

[Nucleo-64板载ST-LINK/ V2-1调试器 之对外界编程](http://www.stmcu.org/module/forum/thread-609184-1-1.html)

[在Windows上配置Eclipse中配置STM32的开发调试环境](https://zhuanlan.zhihu.com/p/35758891)