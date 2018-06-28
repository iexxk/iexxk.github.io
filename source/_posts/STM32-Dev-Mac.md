---
title: STM32-Dev-Mac
date: 2018-06-18 18:53:17
updated: 2018-06-24 13:58:01
categories: STM32
tags: [STM32,Mac,CLion]
typora-copy-images-to: ./image/src_dir
---

# stm32开发环境搭建(mac)

环境工具

* CLion
* [STM32CubeMX](http://www.st.com/zh/development-tools/stm32cubemx.html) 记录见：[mac系统安装STM32CubeMX](https://jingyan.baidu.com/article/6c67b1d64cd97e2787bb1eb1.html)
* [Segger](https://www.segger.com/downloads/jlink/#Ozone) 下载 Ozone - The J-Link Debugger
* 安装编译器：arm-gcc-none-eabi-gcc `brew cask install gcc-arm-embedded`
* 安装stlink`brew install stlink`
* 安装openocd 执行`brew install openocd`



## 运行测试第一个跑马灯

#### 环境准备

* mac os系统

* 开发板`NUCLEO-F401RE` 其中mcu型号`stm32f401RETx`

* 安装项目初始化软件[STM32CubeMX](http://www.st.com/zh/development-tools/stm32cubemx.html) 步骤见[mac系统安装STM32CubeMX](https://jingyan.baidu.com/article/6c67b1d64cd97e2787bb1eb1.html)

* 安装编译器`arm-gcc-none-eabi-gcc` 执行`brew cask install gcc-arm-embedded`

* 安装stlink下载器`brew install stlink`

* 开发板`NUCLEO-F401RE`跳线如图

  ![QQ20180624-125246](/Users/xuanleung/nustore/xuanfong1.github.io/source/_posts/image/src_dir/QQ20180624-125246.png)

#### 项目搭建步骤：

1. 初始化项目工程见[STM32CubeMX使用之初始化项目](https://jingyan.baidu.com/article/f0e83a2571981922e59101cb.html)

2. 进入生成的工作目录执行`make`

3. 提示错误`/bin/sh: /arm-none-eabi-gcc: No such file or directory`解决，修改`Makefile`

   ```makefile
   # BINPATH是指arm-none-eabi-gcc的路径，可以通过执行which arm-none-eabi-gcc得到路径
   BINPATH = /usr/local/bin/
   ```

4. 提示错误

   ```verilog
   build/main.o: In function `main':
   /Users/xuanleung/IdeaProjects/f401demo/Src/main.c:75: multiple definition of `main'
   ```

   解决修改`Makefile`,删除里面重复的，#标注为有重复，删除即可

   ```makefile
   C_SOURCES =  \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr_ex.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_cortex.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma_ex.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ramfunc.c \
   #Src/stm32f4xx_it.c \
   Src/stm32f4xx_it.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ex.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma.c \
   /Src/system_stm32f4xx.c \
   #Src/stm32f4xx_hal_msp.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_uart.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc_ex.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc.c \
   #Src/main.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim_ex.c \
   Src/stm32f4xx_hal_msp.c \
   Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_gpio.c \
   Src/main.c 
   ```

5. 再重新执行`make`，得到编译成功的文件了

   ```verilog
   /usr/local/bin//arm-none-eabi-size build/f401demo.elf
      text	   data	    bss	    dec	    hex	filename
      5460	     20	   1636	   7116	   1bcc	build/f401demo.elf
   /usr/local/bin//arm-none-eabi-objcopy -O ihex build/f401demo.elf build/f401demo.hex
   /usr/local/bin//arm-none-eabi-objcopy -O binary -S build/f401demo.elf build/f401demo.bin
   ```

6. 下载bin文件到开发板`NUCLEO-F401RE` ,执行`st-flash write ./build/xxxxx.bin 0x8000000`,如果下载失败重启单片机和检查跳线帽

7. 修改src下面的`main.c`添加跑马灯代码

   ```c
   while (1)
   {
       /* USER CODE END WHILE */
   
       /* USER CODE BEGIN 3 */
       HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_RESET);
       HAL_Delay(500);
       HAL_GPIO_WritePin(LD2_GPIO_Port, LD2_Pin, GPIO_PIN_SET);
       HAL_Delay(500);
   }
   ```

8. 重新编译`make`和下载`st-flash write ./build/f401demo.bin 0x8000000` 

9. 下载完成后ld2就会闪烁

## 使用CLion进行项目编译运行

1. 使用STM32CubeMX重新初始化项目，选择`SW4STM32`
2. 



#### 参考

[macOS 下用 Clion和OpenOCD开发 STM32(st-link和STM32CubeMX)](https://www.jianshu.com/p/ed7203324ac6)

[CLion for embedded development](https://blog.jetbrains.com/clion/2016/06/clion-for-embedded-development/)

[CLion for Embedded Development Part II](https://blog.jetbrains.com/clion/2017/12/clion-for-embedded-development-part-ii/)

http://blog.meekdai.com/MacOS-Eclipse-ARM-GCC-STM32.html

[STM32 Nucleo-64 boards文档](https://www.st.com/content/ccc/resource/technical/document/user_manual/98/2e/fa/4b/e0/82/43/b7/DM00105823.pdf/files/DM00105823.pdf/jcr:content/translations/en.DM00105823.pdf)

[Nucleo-64板载ST-LINK/ V2-1调试器 之对外界编程](http://www.stmcu.org/module/forum/thread-609184-1-1.html)