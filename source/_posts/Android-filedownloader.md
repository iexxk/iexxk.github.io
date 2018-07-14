---
title: Android-filedownloader
date: 2018-07-13 15:50:35
updated: 2018-07-13 16:39:01
categories: Android
tags: [Android,filedownloader]
---

#### 安卓文件离线断点下载

GitHub：[lingochamp/FileDownloader](https://github.com/lingochamp/FileDownloader)

添加依赖`implementation 'com.liulishuo.filedownloader:library:1.7.4'`

`Application`里添加初始化

```java
FileDownloader.setupOnApplicationOnCreate(this)
    .connectionCreator(new FileDownloadUrlConnection
    .Creator(
        new FileDownloadUrlConnection.Configuration()
        .connectTimeout(15_000) // set connection timeout.
        .readTimeout(15_000) // set read timeout.
	)
).commit();
```

单次弹窗下载进度条

```java
AlertDialog.Builder builder = new AlertDialog.Builder(context);
builder.setTitle("是否需要下载离线地图？");
builder.setMessage(f.getAbsolutePath() + " 没有找到离线地图文件");
builder.setCancelable(true);
final ProgressDialog dialog22 = new ProgressDialog(this);
dialog22.setTitle("正在下载离线地图");
dialog22.setCancelable(false);
builder.setPositiveButton("下载(文件>500M)", new DialogInterface.OnClickListener() {
    @Override
    public void onClick(final DialogInterface dialog, int which) {
        FileDownloader.getImpl().create(Config.KJMAPDOWNLOAD)
            .setAutoRetryTimes(100)
            .setPath(f.getAbsolutePath(),true)
            .setListener(new FileDownloadLargeFileListener() {
                @Override
                protected void pending(BaseDownloadTask task, long soFarBytes, long totalBytes) {
                    dialog22.show();
                }
                @Override
                protected void progress(BaseDownloadTask task, long soFarBytes, long totalBytes) {
                    dialog22.setMessage( "重试"+task.getRetryingTimes()+"次,下载速度：" + task.getSpeed() + "kb/s,百分比：" + soFarBytes / 1048576 + "/" + totalBytes / 1048576 + "M");
                }
                @Override
                protected void completed(BaseDownloadTask task) {
                    Toast.makeText(LineActivity.this, "下载成功，请重新打开该页面", Toast.LENGTH_LONG).show();
                    String oldFileUrl=task.getPath()+"/"+task.getFilename();
                    Log.i("oldFileUrl",oldFileUrl);
                    File oldName=new File(oldFileUrl);
                    File newName=new File(f.getAbsolutePath()+"/"+Config.KJMAPDOWNLOADFILENAME);
                    if (oldName.renameTo(newName)){
                        Log.i("LineActivity","重命名成功");
                    }else {
                        Log.e("LineActivity","重命名失败");
                    }
                    dialog22.dismiss();
                }
                @Override
                protected void paused(BaseDownloadTask task, long soFarBytes, long totalBytes) {
                }
                @Override
                protected void error(BaseDownloadTask task, Throwable e) {
                    Toast.makeText(LineActivity.this, "下载失败", Toast.LENGTH_LONG).show();
                    dialog22.dismiss();
                }
                @Override
                protected void warn(BaseDownloadTask task) {
                }
            }).start();
        dialog.dismiss();
    }
});
builder.setNegativeButton("取消", new DialogInterface.OnClickListener() {
    @Override
    public void onClick(DialogInterface dialog, int which) {
        dialog.dismiss();
    }
});
AlertDialog dialog = builder.create();
dialog.show();
```

### 注意事项

1. `getAbsolutePath()`获取文件路径，末尾没有`/` 如果获取文件地址需要手动拼接`/`
2. ` .setPath(f.getAbsolutePath(),true)`这个必须设置，后面需要指定该路径是文件还是目录，如果要设置文件名，需要设置为false，然后路径拼接文件名,如果是路径模式，下载完成后需要手动重命名，否则没有文件后缀
3. 该下载会自动接着上次未完成的下载，需要重新下载，可以去下载目录删除未完成的文件即可
4. 文件大小可以能大于1g用`FileDownloadLargeFileListener`