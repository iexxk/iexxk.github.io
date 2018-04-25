---
title: Android-WebView
date: 2018-04-24 13:35:30
updated: 2018-04-24 13:35:30
categories: Android
tags: [Android,WebView]
---

将一个html H5网页打包成一个apk

1. 在`MainActivity`初始化一个`webview`,启用JavaScript脚步，然后设置自定义`Webviewclient`,接着就是设置些缓存等，这些非必须，最后终哟啊的一个方法就是加载`webview.loadUrl`这里添加你的h5链接，如果是本地，直接是路径就可以了，最后设置`setContentView(webview);`,里面还加了`webview`返回是网页的返回，到返回完了，在返回就是退出应用提示`dialog`

   ```java
   public class MainActivity extends AppCompatActivity {
       private WebView webview;
       @Override
       protected void onCreate(Bundle savedInstanceState) {
           super.onCreate(savedInstanceState);

           //实例化WebView对象
           webview = new WebView(this);
           //设置WebView属性，能够执行Javascript脚本
           webview.getSettings().setJavaScriptEnabled(true);
           //重写WebViewClient
           webview.setWebViewClient(new WebViewClientDiy(this));  
           //额外的设置，缓存等
           webview.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
           webview.getSettings().setJavaScriptEnabled(true);
           webview.getSettings().setDomStorageEnabled(true);
           webview.getSettings().setAppCacheMaxSize(1024 * 1024 * 8);
           String appCachePath = this.getApplicationContext().getCacheDir()
                   .getAbsolutePath();
           webview.getSettings().setAppCachePath(appCachePath);
           webview.getSettings().setAllowFileAccess(true);
           webview.getSettings().setAppCacheEnabled(true);


           //加载需要显示的网页
           //webview.loadUrl("file:///android_asset/index.html");//显示本地网页
           webview.loadUrl("http://dev.clothes.yaokexing.com/mobile/welcome");//显示远程网页
           //设置Web视图
           setContentView(webview);
       }

       @Override//设置回退
       public boolean onKeyDown(int keyCode, KeyEvent event) {
           if ((keyCode == KeyEvent.KEYCODE_BACK) && webview.canGoBack()) {
               webview.goBack(); //goBack()表示返回WebView的上一页面
               return true;
           } else {
               AlertDialog exitDialog = new AlertDialog.Builder(this).create();
               exitDialog.setTitle("系统提示");
               exitDialog.setMessage("你确定要退出吗");
               exitDialog.setButton(DialogInterface.BUTTON_POSITIVE, "确定", new DialogInterface.OnClickListener() {
                   @Override
                   public void onClick(DialogInterface dialog, int which) {
                       finish();
                   }
               });
               exitDialog.setButton(DialogInterface.BUTTON_NEGATIVE, "取消", new DialogInterface.OnClickListener() {
                   @Override
                   public void onClick(DialogInterface dialog, int which) {
                       Toast.makeText(MainActivity.this, "欢迎回来", Toast.LENGTH_SHORT).show();
                   }
               });
               //onKeyListener用于设置监听手机back键的操作
               exitDialog.setOnKeyListener(new DialogInterface.OnKeyListener() {
                   @Override
                   public boolean onKey(DialogInterface dialog, int keyCode, KeyEvent event) {
                       if (keyCode == KeyEvent.KEYCODE_BACK) {
                           return true;// false时dialog会消失
                       }
                       return true;
                   }
               });
               exitDialog.show();
           }
           return super.onKeyDown(keyCode, event);  //退出程序
       }
   ```

2. 自定义`WebViewClient`类,里面主要覆写`shouldOverrideUrlLoading`这个方法，因存在老版本和新版本，所以把判断是否用webview加载独立方法出来，一些第三方登录需要用系统的浏览器，所以这里就起到作用了

   ```java
   public class WebViewClientDiy extends WebViewClient {
       Context context;
       public WebViewClientDiy(Context context) {
           this.context=context;
       }

       @SuppressWarnings("deprecation")
       @Override
       public boolean shouldOverrideUrlLoading(WebView view, String url) {
           final Uri uri = Uri.parse(url);  //老版本
           return handleUri(uri,view);
       }

       @TargetApi(Build.VERSION_CODES.N)
       @Override
       public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
           final Uri uri = request.getUrl();  //新版本
           return handleUri(uri,view);
       }

       private boolean handleUri(final Uri uri,WebView view) {
           Log.i("测试", "Uri =" + uri);
           if (uri.toString().contains("weixin://wap/pay?")){
               Intent intent = new Intent();
               intent.setAction(Intent.ACTION_VIEW);
               intent.setData(Uri.parse(uri.toString()));
               context.startActivity(intent);   //系统默认加载方法
               return true;
           }
           view.loadUrl(uri.toString());  //调用webview的加载方法
               return true;
       }
   }
   ```

3. 在`AndroidMainfest.xml`添加网络权限`<uses-permission android:name="android.permission.INTERNET"/>`,到此基本就可以用了

4. 现在做一些优化关闭标题栏，修改`AndroidMainfest.xml`的them为自定义样式`android:theme="@style/AppTheme.NoActionBar">`

   改样式需要在`styles.xml`添加如下内容

   ```Xml
       <style name="AppTheme.NoActionBar" parent="Theme.AppCompat.Light.DarkActionBar">
           <item name="windowActionBar">false</item>
           <item name="windowNoTitle">true</item>
           <item name="android:windowFullscreen">false</item>
       </style>
   ```

   ​





