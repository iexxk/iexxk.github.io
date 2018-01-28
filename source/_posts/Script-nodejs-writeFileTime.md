---
title: 批量写入文件的修改时间
date: 2018-01-28 22:05:33
updated: 2018-01-28 22:05:33
categories: script
tags: [script,npm,nodejs,file]
---

### 环境

系统：wsl

环境：nodejs

##### 步骤

1. 创建脚本
2. 编写脚本内容
3. 修改脚本为执行文件`chmod +x scriptfilename`

#### 需求描述

批量把文档的修改时间写入该文档的指定字段位置

###### eg：添加hexo 文章的修改时间

##### 脚本内容解读

file文件系统的主要方法解释

```javascript
var fs = require("fs"); //请求文件系统
fs.readdir("./",function(err,files){}); //读取./也就是当前目录的所有文件
fs.readFile(file, 'utf8',function(err, data) {}); //读取"file"文件内容data
fs.stat(file,function(err, stats) {}); //读取文件信息，创建时间等
fs.writeFile(file, result, 'utf8',function(err) {}); //写入file文件内容result,会覆盖原来的
datastring.replace(/正则表达式:/g,"新的内容")；//正则替换/正则内容/g，datastring数据源
```

文件信息stats返回的是json信息格式如下

```json
Stats {
  dev: 12,
  mode: 33279,
  nlink: 1,
  uid: 0,
  gid: 0,
  rdev: 0,
  blksize: 512,
  ino: 4785074604307105,
  size: 1297,
  blocks: 8,
  atimeMs: 1517144361661.3943,
  mtimeMs: 1517146617920.6301,
  ctimeMs: 1517146647324.5525,
  birthtimeMs: 1517146647324.5525, 
  atime: 2018-01-28T12:59:21.661Z, //访问时间
  mtime: 2018-01-28T13:36:57.921Z, //修改时间
  ctime: 2018-01-28T13:37:27.325Z, //创建时间
  birthtime: 2018-01-28T13:37:27.325Z }
```

批量读取脚本路径的当前目录的所有文件，通过判段文件名是否包含`.md`防止改了不必要的文件

```
console.log('文件创建时间读取并写入文件指定字段demo');
var fs = require("fs"); //请求文件系统
var file = "./txt"; //设置读取和写入的文件，当前目录下的test文件

fs.readdir("./",function(err,files){
	var len=files.length;
	var file=null;
	for(var i=0;i<len;i++){
		file=files[i];
		console.log("读取文件：",file);
		if(file.indexOf(".md")>-1){
			console.log("处理文件：",file);
			writeFileTime(file,fs);
		}
	}
});
```

单文件读取并写入修改时间

```javascript
/*
file:读取时间的文件以及写入内容的文件
fs: 文件系统
*/
function writeFileTime(file,fs){
	fs.readFile(file, 'utf8',function(err, data) { //读取文件内容
		if (err) return console.log("读取文件内容错误：",err);
		console.log("文件"+file+"的内容：",data);
		fs.stat(file,function(err, stats) { //读取文件信息，创建时间等
		   if (err) return console.log("读取文件信息错误：",err);
			console.log("文件"+file+"的信息：",stats);  //打印文件的信息
			console.log("创建时间是：",stats.mtime);
			console.log("格式化",getFormatDate(stats.mtime));
			var result = data.replace(/categories:/g, "updated: "+getFormatDate(stats.mtime)+"\r"+"categories:");//data:替换为date:2018.....
			console.log("修改后文件内容为：",result);
			fs.writeFile(file, result, 'utf8',function(err) { //写入新的文件内容
				if (err) return console.log("写文件错误：",err);
			});
		});
	});
}
```

时间格式化方法

```javascript
/*
 timeStr:时间，格式可为："September 16,2016 14:15:05、
 "September 16,2016"、"2016/09/16 14:15:05"、"2016/09/16"、
 '2014-04-23T18:55:49'和毫秒
 dateSeparator：年、月、日之间的分隔符，默认为"-"，
 timeSeparator：时、分、秒之间的分隔符，默认为":"
 */
function getFormatDate(timeStr, dateSeparator, timeSeparator) {
    dateSeparator = dateSeparator ? dateSeparator : "-";
    timeSeparator = timeSeparator ? timeSeparator : ":";
    var date = new Date(timeStr),
            year = date.getFullYear(),// 获取完整的年份(4位,1970)
            month = date.getMonth(),// 获取月份(0-11,0代表1月,用的时候记得加上1)
            day = date.getDate(),// 获取日(1-31)
            hour = date.getHours(),// 获取小时数(0-23)
            minute = date.getMinutes(),// 获取分钟数(0-59)
            seconds = date.getSeconds(),// 获取秒数(0-59)
            Y = year + dateSeparator,
            M = ((month + 1) > 9 ? (month + 1) : ('0' + (month + 1))) + dateSeparator,
            D = (day > 9 ? day : ('0' + day)) + ' ',
            h = (hour > 9 ? hour : ('0' + hour)) + timeSeparator,
            m = (minute > 9 ? minute : ('0' + minute)) + timeSeparator,
            s = (seconds > 9 ? seconds : ('0' + seconds)),
            formatDate = Y + M + D + h + m + s;
    return formatDate;
}
```





### 最终脚本内容

```javascript
#!/usr/bin/env node
/*
批量添加修改时间
用于bolg初始化修改时间
*/

console.log('文件创建时间读取并写入文件指定字段demo');
var fs = require("fs"); //请求文件系统
var file = "./txt"; //设置读取和写入的文件，当前目录下的test文件

fs.readdir("./",function(err,files){
	var len=files.length;
	var file=null;
	for(var i=0;i<len;i++){
		file=files[i];
		console.log("读取文件：",file);
		if(file.indexOf(".md")>-1){
			console.log("处理文件：",file);
			writeFileTime(file,fs);
		}
	}
});
/*
file:读取时间的文件以及写入内容的文件
fs: 文件系统
*/
function writeFileTime(file,fs){
	fs.readFile(file, 'utf8',function(err, data) { //读取文件内容
		if (err) return console.log("读取文件内容错误：",err);
		console.log("文件"+file+"的内容：",data);
		fs.stat(file,function(err, stats) { //读取文件信息，创建时间等
		   if (err) return console.log("读取文件信息错误：",err);
			console.log("文件"+file+"的信息：",stats);  //打印文件的信息
			console.log("创建时间是：",stats.mtime);
			console.log("格式化",getFormatDate(stats.mtime));
			var result = data.replace(/categories:/g, "updated: "+getFormatDate(stats.mtime)+"\r"+"categories:");//data:替换为date:2018.....
			console.log("修改后文件内容为：",result);
			fs.writeFile(file, result, 'utf8',function(err) { //写入新的文件内容
				if (err) return console.log("写文件错误：",err);
			});
		});
	});
}

/*
 timeStr:时间，格式可为："September 16,2016 14:15:05、
 "September 16,2016"、"2016/09/16 14:15:05"、"2016/09/16"、
 '2014-04-23T18:55:49'和毫秒
 dateSeparator：年、月、日之间的分隔符，默认为"-"，
 timeSeparator：时、分、秒之间的分隔符，默认为":"
 */
function getFormatDate(timeStr, dateSeparator, timeSeparator) {
    dateSeparator = dateSeparator ? dateSeparator : "-";
    timeSeparator = timeSeparator ? timeSeparator : ":";
    var date = new Date(timeStr),
            year = date.getFullYear(),// 获取完整的年份(4位,1970)
            month = date.getMonth(),// 获取月份(0-11,0代表1月,用的时候记得加上1)
            day = date.getDate(),// 获取日(1-31)
            hour = date.getHours(),// 获取小时数(0-23)
            minute = date.getMinutes(),// 获取分钟数(0-59)
            seconds = date.getSeconds(),// 获取秒数(0-59)
            Y = year + dateSeparator,
            M = ((month + 1) > 9 ? (month + 1) : ('0' + (month + 1))) + dateSeparator,
            D = (day > 9 ? day : ('0' + day)) + ' ',
            h = (hour > 9 ? hour : ('0' + hour)) + timeSeparator,
            m = (minute > 9 ? minute : ('0' + minute)) + timeSeparator,
            s = (seconds > 9 ? seconds : ('0' + seconds)),
            formatDate = Y + M + D + h + m + s;
    return formatDate;
}

```

