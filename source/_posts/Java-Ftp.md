---
title: Java-Ftp
date: 2018-07-14 14:08:35
updated: 2018-12-12 10:47:58
categories: Java
tags: [Java,Ftp]
---

#### 问题：

##### 问题1： 文件损坏

```java
//该格式会转码导致部分数据丢失
ftp.setFileType(FTP.ASCII_FILE_TYPE);  
//该格式不会丢失数据
ftp.setFileType(FTP.BINARY_FILE_TYPE);
```

##### 问题2：上传失败

发现在虚拟机运行代码时发现通过FTP上传文件总是失败返回`500 Illegal PORT command`

查资料所得发现FTP工作协议分：参考[FTP时显示500 Illegal PORT command的解决](https://blog.csdn.net/jsd2honey/article/details/76572410)

* 主动模式：服务器向客户端敲门，然后客户端开门(端口) 
* 被动模式：客户端向服务器敲门，然后服务器开门(端口) 

从上面分析就知道，主动模式肯定不行的，虚拟机里的服务开放端口，然后告诉服务器，但是服务器并不能访问虚拟机的端口，他只能访问虚拟机宿主机的端口，因此导致了本地可以运行，但是放到虚拟机却上传失败了

##### 解决

然后在代码里添加`ftp.enterLocalPassiveMode();`设置为被动模式，记得上传下载都要设置。

不设置默认为主动模式`enterLocalActiveMode()`

##### 附代码

pom.xml添加ftp依赖

```xml
<dependency>
    <groupId>commons-net</groupId>
    <artifactId>commons-net</artifactId>
    <version>3.5</version>
</dependency>
```

ftp工具类：

```java
/**
 * ftp上传下载工具类
 */
public class FtpUtil {
    /**
     * Description: 向FTP服务器上传文件
     *
     * @param host     FTP服务器hostname
     * @param port     FTP服务器端口
     * @param username FTP登录账号
     * @param password FTP登录密码
     * @param basePath FTP服务器基础目录
     * @param filePath FTP服务器文件存放路径。例如分日期存放：/2015/01/01。文件的路径为basePath+filePath
     * @param filename 上传到FTP服务器上的文件名
     * @param input    输入流
     * @return 成功返回true，否则返回false
     */
    public static boolean uploadFile(String host, int port, String username, String password, String basePath,
                                     String filePath, String filename, InputStream input) throws IOException {
        boolean result = false;
        FTPClient ftp = new FTPClient();
        try {
            int reply;
            ftp.connect(host, port);// 连接FTP服务器
            // 如果采用默认端口，可以使用ftp.connect(host)的方式直接连接FTP服务器
            ftp.login(username, password);// 登录
            reply = ftp.getReplyCode();
            if (!FTPReply.isPositiveCompletion(reply)) {
                ftp.disconnect();
                return result;
            }
            ftp.enterLocalPassiveMode();  //设置被动模式
            //切换到上传目录
            if (!ftp.changeWorkingDirectory(basePath + filePath)) {
                //如果目录不存在创建目录
                String[] dirs = filePath.split("/");
                String tempPath = basePath;
                for (String dir : dirs) {
                    if (null == dir || "".equals(dir)) continue;
                    tempPath += "/" + dir;
                    if (!ftp.changeWorkingDirectory(tempPath)) {
                        if (!ftp.makeDirectory(tempPath)) {
                            return result;
                        } else {
                            ftp.changeWorkingDirectory(tempPath);
                        }
                    }
                }
            }
            //设置上传文件的类型为二进制类型
            ftp.setFileType(FTP.BINARY_FILE_TYPE);

            //上传文件
            if (!ftp.storeFile(filename, input)) {
                return result;
            }
            input.close();
            ftp.logout();
            result = true;
        } catch (IOException e) {
           // e.printStackTrace();
           throw e;
        } finally {
            if (ftp.isConnected()) {
                try {
                    ftp.disconnect();
                } catch (IOException ioe) {
                }
            }
        }
        return result;
    }

    /**
     * Description: 从FTP服务器下载文件
     *
     * @param host       FTP服务器hostname
     * @param port       FTP服务器端口
     * @param username   FTP登录账号
     * @param password   FTP登录密码
     * @param remotePath FTP服务器上的相对路径
     * @param fileName   要下载的文件名
     * @param localPath  下载后保存到本地的路径
     * @return
     */
    public static boolean downloadFile(String host, int port, String username, String password, String remotePath,
                                       String fileName, String localPath) {
        boolean result = false;
        FTPClient ftp = new FTPClient();
        try {
            int reply;
            ftp.connect(host, port);
            // 如果采用默认端口，可以使用ftp.connect(host)的方式直接连接FTP服务器
            ftp.login(username, password);// 登录
            reply = ftp.getReplyCode();
            if (!FTPReply.isPositiveCompletion(reply)) {
                ftp.disconnect();
                return result;
            }
            ftp.enterLocalPassiveMode();  //设置被动模式
            ftp.changeWorkingDirectory(remotePath);// 转移到FTP服务器目录
            FTPFile[] fs = ftp.listFiles();
            for (FTPFile ff : fs) {
                if (ff.getName().equals(fileName)) {
                    File localFile = new File(localPath + "/" + ff.getName());
                    OutputStream is = new FileOutputStream(localFile);
                    ftp.retrieveFile(ff.getName(), is);
                    is.close();
                }
            }

            ftp.logout();
            result = true;
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (ftp.isConnected()) {
                try {
                    ftp.disconnect();
                } catch (IOException ioe) {
                }
            }
        }
        return result;
    }

    /**
     * 删除FTP上指定路径的文件
     *
     * @param host
     * @param port
     * @param username
     * @param password
     * @param ftpDirAndFileName
     * @return
     */
    public static boolean deleteFile(String host, int port, String username, String password, String ftpDirAndFileName) {
        FTPClient ftp = new FTPClient();
        try {
            int reply;
            ftp.connect(host, port);
            // 如果采用默认端口，可以使用ftp.connect(host)的方式直接连接FTP服务器
            ftp.login(username, password);// 登录
            reply = ftp.getReplyCode();
            if (!FTPReply.isPositiveCompletion(reply)) {
                ftp.disconnect();
                return false;
            }
            boolean hasDelete = ftp.deleteFile(ftpDirAndFileName);

            ftp.logout();
            return hasDelete;
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (ftp.isConnected()) {
                try {
                    ftp.disconnect();
                } catch (IOException ioe) {
                }
            }
        }

        return false;
    }
}
```



##### 问题3：docker部署，无权限问题

原因：由于使用ftp登陆时默认跟目录`/`其实时用户ftp home目录，因此设置home目录因该是挂载卷的子目录，不然同级回提示没权限，如果新配置记得删除passwd的文件或删除，不然配置修改无效

正确的配置文件如下

```yaml
  ftpd-server:
    restart: on-failure
    image: stilliard/pure-ftpd:hardened
    volumes:
      - /dockerdata/v-manager-test-ygl/ftpdata:/home/ftpusers
      - /dockerdata/v-manager-test-ygl/ftpconfig:/etc/pure-ftpd/passwd
    ports:
       - "14821:21"
       - "30000-30009:30000-30009"
    environment:
      PUBLICHOST: "192.168.1.230"
      FTP_USER_NAME: "ftpuser"
      FTP_USER_PASS: "ftpuser"
      FTP_USER_HOME: "/home/ftpusers/ftpuser"
```



#### 问题4：ftp 被动模式依赖iptable服务

