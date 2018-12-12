---
title: viewGroup自定义控件
date: 2016-12-13 16:48:12
updated: 2018-01-28 21:41:27categories: Android
tags: [viewGroup,卫星菜单，测量]
---
## 自定义控件的基本使用
>* 创建一个控件类继承ViewGroup
>* 复写onlayout
>* 复写测量onMeasure

```java
public class ArcMenu extends ViewGroup {
    public ArcMenu(Context context, AttributeSet attrs) {
        super(context, attrs);
    }
	@Override
    protected void onLayout(boolean changed, int l, int t, int r, int b) {
	  int cent_x = getWidth() / 2; //viewgroup中心坐标
      int cent_y = getHeight() / 2; //viewgroup中心坐标
	  for (int i = 0; i < getChildCount(); i++) {
	  
         View childView = getChildAt(i);  //遍历子控件
         int childWidth = childView.getMeasuredWidth();  //获得子控件的宽度，需要先测量
         int childHeight = childView.getMeasuredHeight();
		 
			int cl = 0, ct = 0, cr = 0, cb = 0;		
		}
		 
		  childView.layout(cl, ct, cr, cb); //见下图
	}
	@Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        //测量所有子View的宽高
        measureChildren(widthMeasureSpec, heightMeasureSpec);
    }
}
```

`childView.layout(cl, ct, cr, cb)`
![viewGroup](http://ohdtoul5i.bkt.clouddn.com/viewgroup.png)

>* 在xml里面引用
```
 <com.xuan.hifusion.customcontrols.ArcMenu
                android:id="@+id/car_arcmenu"
                android:layout_width="match_parent"
                android:layout_height="match_parent"
                android:layout_weight="1"
                android:gravity="center">

                <ImageView
                    android:id="@+id/car_cent_line_iv"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:visibility="invisible"
                    app:srcCompat="@drawable/car_cent_line" />

                <ImageView
                    android:id="@+id/car_light_off_iv"
                    android:layout_width="wrap_content"
                    android:layout_height="wrap_content"
                    android:tag="右下"
                    android:visibility="invisible"
                    app:srcCompat="@drawable/car_light_off" />
 </com.xuan.hifusion.customcontrols.ArcMenu>
```
