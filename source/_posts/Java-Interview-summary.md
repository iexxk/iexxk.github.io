---
title: Java面试总结
date: 2018-04-08 17:19:08
updated: 2018-04-08 23:55:10
categories: Java
tags: [面试,java]
---

## 面试百问

1. Http2.0与http1.0

   * 性能大幅提升
   * 多路复用
   * header压缩

2. 重写equals为何要重写hashcode

   hashcode:是jdk根据对象的地址或者字符串或者数字算出来的int类型的数值。

   实战：向`HashSet`添加对象，自动去除重复的对象

   原理：`HashSet` 的 `add` 方法判断两个对象是否“相同”

   ```mermaid
   graph LR
   q[hashset.add对象]-->a{调用对象内hashCode判断}
   a-->|相等|b{调用对象内equlas判断}
   a-->|不相等|c[添加到集合hashset]
   b-->|相等|d[不添加对象到hashset]
   b-->|不相等|c
   ```

   举例测试：

   ```Java
   HashSet<Xy> xys=new HashSet<>();
   xys.add(new Xy(1,2));
   xys.add(new Xy(2,2));
   xys.add(new Xy(2,2));
   System.out.print(xys.toString()); //输出[{2,2}, {1,2}]
    System.out.print(new Xy(1,2).equals(new Xy(1,2))); //输出true
   ```

   对象类的实现必须覆写`equals`和`hashCode`

   ```java
   public class Xy {
       private int x;
       private int y;
       Xy(int x, int y){
           this.x=x;
           this.y=y;
       }
       @Override
       public int hashCode() {
           return Objects.hash(x,y); //生成hashcode，只要保证不同的值生成不同的hashcode即可
       }
       @Override
       public boolean equals(Object obj) {
           System.out.print("2");
           if (!(obj instanceof Xy)){
               return false;
           }
           Xy test= (Xy) obj;
           return (test.x == x) && (y == test.y);
       }
       @Override
       public String toString() {
           return "{"+x+","+y+"}";
       }
   }
   ```

3. java对象的生命周期

   1. 创建阶段(created) `分配存储空间->构造对象->static初始化(超类到子类)->变量构造方法初始化(超到子类)`
   2. 应用阶段(InUse)`至少被一个强引用持有（Object object=new Object();）`
   3. 不可见阶段(Invisible)`不在被任何强引用持有(但是可能被jvm持有),超出对象作用域(方法内定义了变量,方法外该变量就是不可见,编译报错)`
   4. 不可达阶段(Unreachable)`不在被任何强引用持有`
   5. 收集阶段(collected)`已经被垃圾回收器发现,会调用finazlie方法,所以一般不要重写,会影响垃圾回收`
   6. 终结阶段(Finalized)`对象执行完finazlie仍处于不可达，则进入该阶段等待垃圾回收`
   7. 对象空间重写分配阶段(Deallocated)`垃圾已经回收，空间处于再分配状态`

4. java创建对象的几种方式

   ```java
   User user = new User(); //new方式
   User user = User.class.newInstance(); //反射方式1.newInstance,无参的构造对象
   Constructor<User> constructor = User.class.getConstructor();
   User user = constructor.newInstance(); //反射方式2.Constructor 有参构造对象
   //public class CloneTest implements Cloneable{} //clone需要实现该接口
   CloneTest copyClone = (CloneTest) cloneTest.clone(); //clone浅克隆，深克隆(含内部自定义对象)
   public class Test implements Serializable//反序列化,文件反序列化为对象
   ```

5. 反射invoke

   ```java
   //正常的调用
   Xy xy = new Xy();
   xy.setX(5);
   System.out.println("xy x:" + xy.getX());
   //使用反射调用
   try {
       Class xy2 = Class.forName("com.example.demo.Xy"); //找到class
       Method setxMethod = xy2.getMethod("setX", int.class); //获得set方法
       Object xyObj = xy2.newInstance();//必须有不带参的构造(不然运行InstantiationException)
       setxMethod.invoke(xyObj, 5);  //调用set方法
       Method getXMethod = xy2.getMethod("getX"); //获得get方法
       System.out.println("xy x:" + getXMethod.invoke(xyObj)); //调用get方法
   } catch (Exception e) {
       e.printStackTrace();
   }
   ```

6. ​

