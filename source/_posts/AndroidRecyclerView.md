---
title: Android-RecyclerView
date: 2018-05-09 11:26:38
updated: 2018-12-12 10:47:58
categories: Android
tags: [RecyclerView,Android]
---

### RecyclerView 基本使用

1. 添加依赖v7包依赖，版本号和`compileSdkVersion`一致，不然报错

   ```groovy
   implementation 'com.android.support:appcompat-v7:25.0.0'
   implementation 'com.android.support:recyclerview-v7:25.0.0'
   ```

2. 在layout里添加`RecyclerView`布局的引用

   ```xml
   <android.support.v7.widget.RecyclerView
       android:id="@+id/recyView1"
       android:layout_width="wrap_content"
       android:layout_height="wrap_content"
   />
   ```

3. 添加一个item的布局

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <android.support.constraint.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
       xmlns:app="http://schemas.android.com/apk/res-auto"
       android:layout_width="match_parent"
       android:layout_height="match_parent">

       <TextView
           android:id="@+id/recyNumberPhone"
           android:layout_width="wrap_content"
           android:layout_height="wrap_content"
           android:text="TextView"
           app:layout_constraintStart_toStartOf="parent"
           app:layout_constraintTop_toTopOf="parent" />

       <TextView
           android:id="@+id/recyNumberName"
           android:layout_width="wrap_content"
           android:layout_height="wrap_content"
           android:text="TextView"
           app:layout_constraintEnd_toEndOf="parent"
           app:layout_constraintTop_toTopOf="parent" />
   </android.support.constraint.ConstraintLayout>
   ```

4. 创建适配器`RecyNumberAdapter`继承` RecyclerView.Adapter`

   ```java
   public class RecyNumberAdapter extends RecyclerView.Adapter<RecyNumberAdapter.NumberHolder>{
       private Context context; //上下文
       private List<Map<String,String>> mDatas;  //数据源
     
       public RecyNumberAdapter(Context context,List<Map<String,String>> mDatas){
           //构造方法传入数据
           this.context=context;
           this.mDatas=mDatas;
       }

       @Override
       public NumberHolder onCreateViewHolder(ViewGroup parent, int viewType) {
           // 填充布局item
           View view = LayoutInflater.from(context).inflate(R.layout.recy_number, null);
           NumberHolder holder = new NumberHolder(view);
           return holder;
       }

       @Override
       public void onBindViewHolder(final NumberHolder holder, final int position) {
           //绑定view
     holder.recyNumberName.setText(String.valueOf(mDatas.get(position).get("name"))); //用户名
     holder.recyNumberPhone.setText(String.valueOf(mDatas.get(position).get("id"))); //电话号码  
       }

       @Override
       public int getItemCount() {
           return mDatas.size(); //数据长度
       }
       //类部类
       class  NumberHolder extends RecyclerView.ViewHolder{
           //获取item子布局的控件
           private TextView recyNumberPhone;
           private TextView recyNumberName;
           public NumberHolder(View view){
               super(view);
               recyNumberPhone=view.findViewById(R.id.recyNumberPhone);
               recyNumberName=view.findViewById(R.id.recyNumberName);
           }
       }
   }
   ```

5. 调用测试

   ```java
   RecyclerView recyNumberView=findViewById(R.id.personalNumber);
   // 设置布局管理器有横向，表格等等
   GridLayoutManager gridLayoutManager=new GridLayoutManager(this,4);
   recyNumberView.setLayoutManager(gridLayoutManager);
   //测试数据
   List<Map<String,String>> datas=new ArrayList<>();
   Map<String,String> map=new HashMap<>();
   map.put("id","13432861290");
   map.put("name","张三");
   datas.add(map);
   //设置适配器
   recyNumberView.setAdapter(new RecyNumberAdapter(this,datas));
   ```

6. 添加点击事件，在`RecyNumberAdapter`里添加

   ```java
   private OnItemClickListener mItemClickListener;
   //item的回调接口
   public interface OnItemClickListener {
   	void onItemClick(View view, int Position);
   }
   //定义一个设置点击监听器的方法
   public void setOnItemClickListener(OnItemClickListener itemClickListener) {
   	this.mItemClickListener = itemClickListener;
   }
   //在覆写的onBindViewHolder方法中添加
     //如果设置了回调，则设置点击事件
   if (mItemClickListener != null) {
       holder.itemView.setOnClickListener(new View.OnClickListener() {
           @Override
           public void onClick(View v) {
               mItemClickListener.onItemClick(holder.itemView, position);
           }
       });
   }
   ```

7. 调用的时候只需要`recyNumberAdapter.setOnItemClickListener`即可

