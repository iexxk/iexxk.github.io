---
title: hexo博客添加自定义模板
date: 2018-01-30 00:07:03
updated: 2018-12-12 10:47:58
categories: script
tags: [script,nodejs,hexo]
---

### 需求

每次新建文章时都要新建文件然后复制文章头，或者复制其他文件，很麻烦，因此弄一个命令直接生产一个文件带模板

### 脚本详解

前面几篇介绍过关于nodejs文件系统了这里就不介绍了，主要解释下脚本如何传参数

`process.argv[2]`第一个参数，为什么是2,因为1是脚本文件本身所以第一个参数就是2，第二个参数就是3，依次叠加

关于文章默认创建时间以及更新时间都是以当前时间为准

#### 命令使用

```sh
filename <参数1> <参数2> <参数4>
#参数1 文件名也是标题名
#参数2 分类，也就是类别
#参数3 标签，多个用英文逗号分离
#当一个参数都没默认会创建一个空标题文件名为newfile.md的文件标签和分类默认也为空
```

eg: 假设脚本文件名字为new执行`new 标题 java java,nodejs`会生成一个`标题.md文件`内容如下

```markdown
---
title: 标题
date: 2018-01-30 00:07:03
updated: 2018-01-30 00:23:06
categories: java
tags: [java,nodejs]
---
```

##### 额外注意

**如果脚本放的目录就是文章生产的目录，因此放入hexo时记得设置`.gitignore`不要让这个文件也被上传编译了**

###### 脚本内容

```javascript
#!/usr/bin/env node
/*
通过改模板快速创建文章
*/

/*
---
title: WSL使用ssh
date: 2017-11-22 22:12:28
updated: 2018-01-30 00:23:06
categories: WSL
tags: [ssh,ubuntu,sshd]
---
*/
console.log("开始创建文章");
//取第一个参数，因为1被脚本自己本身占用，所以这里是2
var title=process.argv[2]?process.argv[2]:"";  //标题也是文件名
var categories=process.argv[3]?process.argv[3]:"";  //分类
var tags=process.argv[4]?process.argv[4]:"";  //标签 英文逗号分离
var filename=process.argv[2]?process.argv[2]:"newfile";

var fs = require("fs"); //请求文件系统
var template=[];
template.push('---'+'\r');
template.push('title: '+title+'\r');
template.push('date: '+getFormatDate(Date.now())+'\r');
template.push('updated: '+getFormatDate(Date.now())+'\r');
template.push('categories: '+categories+'\r');
template.push('tags: ['+tags+']'+'\r');
template.push('---'+'\r');
var result=template.join('');
fs.writeFile(filename+'.md', result, 'utf8',function(err) { //写入新的文件内容
				if (err) return console.log("写文件错误：",err);
				console.log("创建"+title+".md文件成功：",result);
			});
			
			
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



