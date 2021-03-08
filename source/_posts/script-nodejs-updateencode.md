---
title: Script-nodejs-updateEncode
date: 2018-05-03 23:18:30
updated: 2018-12-12 10:47:58
categories: script
tags: [script,nodejs,file]
---



有bugbug。。。。。。。。



```js
/*
批量修改文件编码
*/
console.log("开始修改文件编码");
var fs= require("fs");
//---------同步----------------
var files =fs.readdirSync("./");
files.forEach(function (filename){
  var stats=fs.statSync(filename);
  console.log(filename+"文件状态",stats);
  //if(stats.isDirectory()) filename +='/';
  //process.
});
//----------异步------------------
fs.readdir("./",function(err,files){
  var len=files.length;
  var file=null;
  for(var i=0;i<len;i++){
    file=files[i];
    console.log("读取文件",file);
    var stats=fs.stat(file);
    console.log("文件状态",stats);
  }
})
```



```Js
#!/usr/bin/env node
/*
批量修改文件编码
*/
console.log("开始修改文件编码");
var fs = require("fs");
var jschardet = require("jschardet");
var path = "node_modules/jschardet";
readDir(path);
/*
修改文件编码
*/
function readDir(dirPath) {
    console.log("目录:",dirPath);
    var files = fs.readdirSync(dirPath);
    files.forEach(function(file) {
        var filepath = dirPath +"/"+file;
        var stats = fs.statSync(filepath);
        //console.log(filename+"文件状态",stats);
        if (stats.isFile()) {
            var buff = fs.readFileSync(file);
            var info = jschardet.detect(buff);
            console.log(filename + "文件编码", info);
        } else if (stats.isDirectory()) {
            console.log("目录" + filepath);
            readDir(filepath);
        }
    });
}

```

