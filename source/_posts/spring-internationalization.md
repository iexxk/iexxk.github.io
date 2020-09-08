---
title: spring 国际化
date: 2020-09-01 10:34:53
updated: 2020-09-08 11:44:07
categories: Spring
tags: [spring]
---

## 国际化配置

spring自带，所以不需要添加任何依赖

1. 在`resources`目录添加

   ```properties
   #创建message.properties文件并添加
   user.name=userName
   ----------------------------
   #创建message_en.properties文件并添加
   user.name=user name
   ---------------------------
   #创建message_zh.properties文件并添加
   user.name=用户名
   ```

2. spring配置文件添加配置`spring.messages.basename=message`其中message为国际化的文件，就是上面添加的文件名，如果有文件夹包裹，从`resources`带上文件相对路径

3. 添加测试类,关键类`MessageSource`是读取国际化文件

   ```java
   import org.slf4j.Logger;
   import org.slf4j.LoggerFactory;
   import org.springframework.beans.factory.annotation.Autowired;
   import org.springframework.context.MessageSource;
   import org.springframework.context.i18n.LocaleContextHolder;
   import org.springframework.web.bind.annotation.RequestMapping;
   import org.springframework.web.bind.annotation.RestController;
   
   @RestController
   @RequestMapping(value = "/test")
   public class TestControl {
   
       private final Logger logger = LoggerFactory.getLogger(getClass());
   
       @Autowired
       MessageSource messageSource;
   
       @RequestMapping(value = "/glob")
       public String glob() {
           String userNmae = messageSource.getMessage("user.name", null, LocaleContextHolder.getLocale());
           logger.info("glob :" + userNmae);
           return userNmae;
       }
   }
   ```

4. 测试，使用postman请求该接口，然后请求`headers`里面添加`Accept-Language:ch`或`Accept-Language:en`就能返回对应的翻译了

### 常见问题

1. 出现`No message found under code 'user.name' for locale 'ch'.`错误

   解决：在配置文件`application.properties`配置`#spring.messages.basename=<你的国际化文件>`，或者检查国际化文件是否存在和配置的文件是否匹配

