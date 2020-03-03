---
title: SpringBoot-BugFix
date: 2020-01-09 09:56:45
updated: 2020-01-09 11:31:11
categories: SpringBoot
tags: [SpringBoot]
---

## SpringBoot 遇到问题总结

### request.getInputStream() 为null问题解决

#### 知识总结

request.getInputStream();  request.getReader();  和request.getParameter("key");

这三个函数中任何一个方法执行一次后（可正常读取body数据），之后再执行就无效了。读取之后游标就向后面移动了

#### 问题描述

1. 使用postman请求没有任何问题，都能读取到
2. 升级springboot 2.2.0以上版本，也不会有任何问题，能读取到

#### 问题分析

1. 在control使用`request.getInputStream()`时获取不到数据流，标记数据被读，断点看`req->request->inputStream->ib->state` 如果state=2代表该输入流已读，再次读取就会为null，state=0代码未读
2. postman能读取，是因为设置了请求头`Content-Type`所以不存在读取不了，因此也和后面那个过滤器进入的条件有关，所以带请求头的并不会进入过滤器
3. springboot 2.2.0以上可以读取，估计是修复该问题
4. springboot 2.2.0以下版本到底是哪里读取了InputStream，最后找到了一个过滤器`HiddenHttpMethodFilter`,里面断点，的确进去了，并用了`request.getParameter`方法

#### 问题解决

升级，或者添加配置禁用`HiddenHttpMethodFilter`过滤器，代码如下

```java
@Configuration
public class ConfigurationData {
	@Bean
	public HttpPutFormContentFilter httpPutFormContentFilter() {
		return new HttpPutFormContentFilter();
	}
	@Bean
	public FilterRegistrationBean disableSpringBootHttpPutFormContentFilter(HttpPutFormContentFilter filter) {
		FilterRegistrationBean filterRegistrationBean = new FilterRegistrationBean();
		filterRegistrationBean.setFilter(filter);
		filterRegistrationBean.setEnabled(false);
		return filterRegistrationBean;
	}
	@Bean
	public HiddenHttpMethodFilter hiddenHttpMethodFilter() {
		return new HiddenHttpMethodFilter();
	}
	@Bean
	public FilterRegistrationBean disableSpringBootHiddenHttpMethodFilter(HiddenHttpMethodFilter filter) {
		FilterRegistrationBean filterRegistrationBean = new FilterRegistrationBean();
		filterRegistrationBean.setFilter(filter);
		filterRegistrationBean.setEnabled(false);
		return filterRegistrationBean;
	}
}
```

#### 测试源码

1. 测试接口接收类

   ```java
   @RestController
   @RequestMapping(value = "/xmbankaccess")
   public class XmBankAccessControl {
       private final Logger logger = LoggerFactory.getLogger(getClass());
     
       @RequestMapping(value = "/facecompare")
       public void facecompare(HttpServletRequest req, HttpServletResponse rsp) throws IOException {
           logger.info("begin");
           byte[] reqByte = readReqData(req);
           String str = new String(reqByte);
           logger.info(str);
       }
     
       private byte[] readReqData(HttpServletRequest request) throws IOException {
           BufferedInputStream bis = null;
           byte[] reqBuff = null;
           try {
               bis = new BufferedInputStream(request.getInputStream());
               byte[] buff = new byte[1024];
               int len = 0;
               int count = 0;
               ByteArrayOutputStream baos = new ByteArrayOutputStream();
               while ((len = bis.read(buff, 0, buff.length)) != -1) {
                   baos.write(buff, 0, len);
                   count += len;
               }
               baos.close();
               reqBuff = new byte[count];
               System.arraycopy(baos.toByteArray(), 0, reqBuff, 0, count);
   
           } catch (IOException e) {
               logger.error("读请求信息异常：", e);
           } finally {
               if (bis != null) {
                   bis.close();
                   bis = null;
               }
           }
           return reqBuff;
       }
   }
   ```

2. 测试请求类

   ```java
   public class AddFaceTest {
   
       private static final Logger log = LoggerFactory.getLogger("aaa");
   
       public static void main(String[] args) throws IOException, InterruptedException {
           sendMsgHttp("aaaa".getBytes());
       }
   
       public static byte[] sendMsgHttp(Object paramObj) {
           // 日志-开始处理
           if (log.isInfoEnabled()) {
               log.info("HTTP通讯处理开始。。。");
           }
           // 参数初始化
           byte[] inData = null;
           byte[] outData = null;
           URL url = null;
           URLConnection conn = null;
           // 读取输入的数据
           if ((paramObj instanceof byte[])) {
               inData = (byte[]) paramObj;
           } else {
               log.error("数据错误：输入的参数必须是byte[]或CompositeData类型的数据");
               return null;
           }
           OutputStream os = null;
           BufferedInputStream is = null;
           try {
               // 建立连接
   //			url = new URL("http://127.0.0.1:8080/xmbankaccess/facecompare");
               url = new URL("http://127.0.0.1:9980/xmbankaccess/facecompare");
               conn = url.openConnection();
               conn.setConnectTimeout(6000);
               conn.setReadTimeout(6000);
               conn.setDoOutput(true);
               if (log.isInfoEnabled()) {
                   log.info("URL连接已打开。。。");
               }
               // 发送请求数据
               os = conn.getOutputStream();
               if (log.isDebugEnabled()) {
                   log.debug("向Servlet发送的请求数据为：" + new String(inData, "UTF-8"));
               }
               os.write(inData);
               os.flush();
               // 读取响应数据
               is = new BufferedInputStream(conn.getInputStream());
               int availableSize = 0;
               byte[] buffer = new byte[8192];
               ByteArrayOutputStream baos = new ByteArrayOutputStream();
               while ((availableSize = is.read(buffer)) != -1) {
                   baos.write(buffer, 0, availableSize);
               }
               outData = baos.toByteArray();
               baos.close();
           } catch (Exception e) {
               log.error("通讯发生异常：", e);
           } finally {
               try {
                   if (null != os) {
                       os.close();
                   }
                   if (null != is) {
                       is.close();
                   }
               } catch (IOException e) {
                   log.error(e.getMessage());
               }
           }
           // 判断响应的内容是否为空，空则直接返回
           if (outData == null) {
               outData = "aa".getBytes();
           }
           return outData;
       }
   }
   ```

   #### 参考

   [SpringMVC 中 request.getInputStream() 为空解惑]([https://emacsist.github.io/2017/12/04/springmvc-%E4%B8%AD-request.getinputstream-%E4%B8%BA%E7%A9%BA%E8%A7%A3%E6%83%91/](https://emacsist.github.io/2017/12/04/springmvc-中-request.getinputstream-为空解惑/))

