---
title: Java基础之抽象类
date: 2017-02-10 15:20:17
categories: Java
tags: [继承,抽象,abstract,父类]
---
# 抽象类
###### 思想
动物->抽象类，猴子->子类
###### 注意点：
1. 抽象类不能被实例化，实例化的工作应该交由它的子类来完成，它只需要有一个引用即可。
2. 抽象方法必须由子类来进行重写。
3. 只要包含一个抽象方法的类，该类必须要定义成抽象类。
4. 抽象类中可以包含具体的方法，当然也可以不包含抽象方法。
5. 子类中的抽象方法不能与父类的抽象方法同名。
6. abstract不能与final并列修饰同一个类。
7. abstract 不能与private、static、final或native并列修饰同一个方法。
###### 实例

子类:

```java
public class MainActivity extends baseActity {
    TextView textView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        textView = (TextView) findViewById(R.id.aa);
        super.initdata("s");
    }

    @Override
    public void send(String data) {
        textView.setText(data);
    }
}
```

抽象类:

```java
public abstract class baseActity extends AppCompatActivity {
    int i = 0;

    void initdata(String a) {
        send(a + i++);
    }
    
    public abstract void send(String data);
}
```

#### 参考

 [java提高篇（四）-----抽象类与接口](http://blog.csdn.net/chenssy/article/details/12858267)