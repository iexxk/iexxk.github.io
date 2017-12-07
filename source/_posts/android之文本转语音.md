---
title: android之文本转语音
date: 2016-09-06 13:29:28
categories: Android
tags: [android组件,TextToSpeech]
---
# android 系统自带了文本转语音的功能
一般手机都有Pico TTS功能，但是没有中文语言包
解决方案： 安装google 语音装文本tts服务或者讯飞tts等兼容系统接口的TTs
### 文字转语音的代码比较少
```java
TextToSpeech mTts;
mTts=new TextToSpeech(this, new TextToSpeech.OnInitListener() {
          @Override
          public void onInit(int status) {
              // status can be either TextToSpeech.SUCCESS or TextToSpeech.ERROR.
              if (status == TextToSpeech.SUCCESS) {
                  // Set preferred language to US english.
                  // Note that a language may not be available, and the result will indicate this.
                  int result = mTts.setLanguage(Locale.CHINA);
                  // Try this someday for some interesting results.
                  // int result mTts.setLanguage(Locale.FRANCE);
                  if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                      // Lanuage data is missing or the language is not supported.
                      Log.e(TAG, "Language is not available.");
                      Intent installIntent = new Intent();
                      installIntent.setAction(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA);
                      startActivity(installIntent);
                  } else {
                      // Check the documentation for other possible result codes.
                      // For example, the language may be available for the locale,
                      // but not for the specified country and variant.
                      // The TTS engine has been successfully initialized.
                      // Allow the user to press the button for the app to speak again.
                      Log.i(TAG,"初始化成功");
                      mTts.speak("初始化成功",TextToSpeech.QUEUE_FLUSH,null);
                  }
              } else {
                  // Initialization failed.
                  Log.e(TAG, "Could not initialize TextToSpeech.");
              }
          }
      });
```
注意销毁 `TextToSpeech`
```java
    @Override
    protected void onDestroy() {
        super.onDestroy();
        // 关闭TextToSpeech对象
        if (mTts != null) {
            mTts.shutdown();
        }
    }
```

### 问题
在使用nubia手机时，发现手机没有这项（TTs）设置,安装了其它TTs却不能开启。
解决：打算用第三方sdk,但是查了一下讯飞的离线文字转语音却发现是收费的，只能说nubia的系统太坑了。