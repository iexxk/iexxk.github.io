---
title: JS-快速入门
date: 2017-03-06 11:47:27
updated: 2018-04-25 20:47:32categories: JavaEE
tags: [js,基础,入门,语法]
---
### 快速入门

1. JavaScript代码可以直接嵌在网页的任何地方，通常放到`<head>`中

2. 由`<script>...</script>`包裹代码

3. 引入文件`<script src="/src/js/xx.js"></script>`

4. `alert('hello world');`对话框

5. `console.log(var类型);` 调试输出打印: 浏览器->右键->检查->Console

6. 严格**区分大小写**

7. `==`自动转换数据类型再比较（缺陷），`===`先比较类型，在比较数据（比较完善）*注：NaN(`0/0;//NaN`)是个特殊的Number，`NaN===NaN;//false`  应该用`isNaN(NaN)`*

8. 数组 `var arr=[1,2,3.14,"helll",null,true];//可以是任意类型`

9. 对象

   ```javascript
   var person={
     name:'xx',
     age:20,
     skill:['js','java','c'],
     hasCar: true,
     zipcode: null
   };//类似json字符串
   person.name; //值为'xx'
   person.tags[0];//值为'js'
   console.log(person); //调试打印出对象
   person.book='hello'; //新增一个book属性
   delete.person.book;//删除book属性
   'name' in person;// 返回true，判断person是否拥有name属性
   person.hasOwnProperty('name'); //true判断一个属性是否是person自身拥有的，而不是继承得到的
   ```

10. 全局变量`i=10;//i是全局变量`  会造成混乱这是一缺陷，弥补缺陷方法加 `'use strict';//需要浏览器支持，如果用了i=10;，将出现ReferenceError错误`

11. 转义字符串 `'I\'m \"ok\"!; //字符串内容I'm "ok"!  `

12. 多行字符串```   `这是一个多行字符串`;//替代了\n ```

13. 模板字符串

    ```javascript
    var name="xx";
    var age=20;
    var message='你好,${name},年龄${age}'; //模板字符串法，需要浏览器支持
    var message='你好,'+name+',年龄'+age; //两者等效
    ```

14. 字符串操作

    ````javascript
    var s='hello world!';
    s.length; //字符串长度
    s[0];//'h'
    s[5];//' '
    s[11];//'!' 
    s[0]='x';//'h' 只可读（赋值是不成功的）
    s=s.toUpperCase();//'HELLO WORLD!' 转换为大写
    s=s.toLowerCase();//转换为小写
    s.indexOf('wo');//返回它的位置6，如果没有wo则返回-1
    s.substring(0,5);//从0开始到5结束（不包括5），'hello'
    s.substring(7);//从7开始到结束 'orld!'
    ````

15. 数组

    ```javascript
    var arr=[1,'a',2];
    arr.length; //3
    arr.length=2; //[1,'2']
    arr.length=4; //[1,'2',undefined,undefined]
    arr[2]=3;//[1,'2',3,undefined]
    arr[4]=6;//[1,'2',3,undefined,6]
    arr.slice(0,3); //等效于substring
    var arrCopy= arr.slice(); //从头到尾复制数组
    var arr=[1,2];
    arr.push('a','b'); //返回长度4
    arr;//[1,2,'a','b']
    arr.pop(); //返回'b'
    arr;//[1,2,'a']
    arr.unshift('A'); //返回长度4
    arr;//['A',1,2,'a']
    arr.sort(); //默认规则（0-9，A-Z,a-z）排序
    arr;//[1,2,A,a]
    arr.shift(); //'1'
    arr;//[2,A,'a'] 
    arr.reverse();
    arr;//['a',A,2] 反转
    //从索引1开始删除2个元素，然后再添加2个元素
    arr.splice(1,2,'b','c');//返回[A,2]
    arr;//[a,b,c]
    var arr2=[1,2,3];
    var added=arr2.concat(arr); //连接
    added;//[1,2,3,a,b,c]
    arr2;//[1,2,3]
    arr;//[a,b,c]
    var arr = ['A', 'B', 'C'];
    arr.concat(1, 2, [3, 4]); //返回['A', 'B', 'C', 1, 2, 3, 4]
    arr.join('-');//'A-B-C'
    var arr=[[1,2,3],[4,5,6],'-']; //多维数组把数组看成一个元素
    arr[1][2];//6
    ```

16. 循环`for (var ? in ?){}`

    ```javascript
    var o={
      name:'xx',
      age:20,
      city:'cq'
    };
    //可以把一个对象的所有属性依次循环出来
    for(var key in o){
      alert(key); //'name','age','city'
    }
    var a=['A','B','C'];
    //由于Array也是对象，而它的每个元素的索引被视为对象的属性
    for(var i in a){
      alert(i); //'0','1','2'
      alert(a[i]); //'A','B','C'
    }
    ```

17. Map是一组键值对的结构，具有极快的查找速度。

    ```javascript
    var m=new Map([['oo',100],['xx',99],['qq',21]]);
    m.get('oo');//100
    var mm=new Map(); //空Map
    mm.set('aa',12); //添加键值对
    mm.has('ss'); //是否存在key 'ss',不存在false
    mm.get('aa'); //获取key 'aa'的值12
    mm.delete('aa'); //删除'aa'键值对
    ```

18. Set:`Set`和`Map`类似，也是一组key的集合，但不存储value。

    ```javascript
    var s1=new Set([1,2,3,3]); //重复key字动过滤
    ```

19. iterable `Array`、`Map`和`Set`都属于`iterable`类型。

    ```javascript
    var a=['A','B','C'];
    for(var x of a){ //遍历Array，Set，Map都可以
      alert(x);  //'A','B','C'
    }
    a.name='hello';
    for(var x in a){
      alert(x);  //'0','1','2','name'
    }
    //for ... in循环将把name包括在内，但Array的length属性却不包括在内。
    //for ... of循环则完全修复了这些问题，它只循环集合本身的元素。
    a.forEach(function (element,index,array)){
      //element: 指向当前元素的值
      //index：指向当前索引(可省略)
      //array：指向array对象本身(可省略)
    }
    var s = new Set(['A', 'B', 'C']);
    s.forEach(function (element, sameElement, set) {
        alert(element);
    });
    var m = new Map([[1, 'x'], [2, 'y'], [3, 'z']]);
    m.forEach(function (value, key, map) {
        alert(value);
    });
    ```

    ​