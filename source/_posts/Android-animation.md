---
title: android动画
date: 2016-12-13 17:13:46
updated: 2018-04-25 20:41:28categories: Android
tags: [动画,TranslateAnimation]
---
>* 平移动画 

`TranslateAnimation animation=new TranslateAnimation(float fromXDelta, float toXDelta, float fromYDelta, float toYDelta)`
fromXDelta 起点x
fromYDelta 起点y
toXDelta 终点x
toYDelta 终点y
以控件的中心为原点坐标，起点终点都是在原点坐标为基准

`animation.setDuration(2000);` 设置动画时间
`animation.setFillAfter(false);` 设置动画结束是否停留显示（false不显示），如果为true,不能通过隐藏控件让他消失
`rb_anmia.setAnimationListener()` 设置动画的监听（`onAnimationStart`,`onAnimationEnd`,`onAnimationRepeat`）
`view.startAnimation(animation);` 启动动画




