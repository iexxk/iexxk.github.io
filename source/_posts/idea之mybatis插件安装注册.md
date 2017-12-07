---
title: idea之mybatis插件安装注册
date: 2017-09-08 17:33:28
categories: JavaEE
tags: [JavaEE,idea,MyBatis]
---

#### MyBatis plugin插件安装步骤

1. 安装setting->Plugins->Browse Respositories...->MyBatis plugin

2. 重启

3. 执行下面代码生成KEY和RESULT

   ```java
   import java.security.InvalidKeyException;
   import java.security.KeyPair;
   import java.security.KeyPairGenerator;
   import java.security.NoSuchAlgorithmException;
   import java.security.interfaces.RSAPrivateKey;
   import java.security.interfaces.RSAPublicKey;

   import javax.crypto.BadPaddingException;
   import javax.crypto.Cipher;
   import javax.crypto.IllegalBlockSizeException;
   import javax.crypto.NoSuchPaddingException;

   class Main {

       public static void main(String[] args) throws NoSuchAlgorithmException, NoSuchPaddingException, InvalidKeyException, BadPaddingException, IllegalBlockSizeException {
           KeyPairGenerator keygen = KeyPairGenerator.getInstance("RSA");
           keygen.initialize(512);
           KeyPair kp = keygen.generateKeyPair();
           RSAPrivateKey privateKey = (RSAPrivateKey)kp.getPrivate();
           RSAPublicKey publicKey = (RSAPublicKey)kp.getPublic();
           System.out.println("KEY:\n" + bytesToHexString(publicKey.getEncoded()) + "\n");
           Cipher cipher = Cipher.getInstance("RSA");
           cipher.init(Cipher.ENCRYPT_MODE,privateKey);
           System.out.println("RESULT:\n" + bytesToHexString(cipher.doFinal("ilanyu".getBytes())) + "\n");
       }

       private static String bytesToHexString(byte[] src){
           StringBuilder stringBuilder = new StringBuilder("");
           if (src == null || src.length <= 0) {
               return null;
           }
           for (byte aSrc : src) {
               int v = aSrc & 0xFF;
               String hv = Integer.toHexString(v);
               if (hv.length() < 2) {
                   stringBuilder.append(0);
               }
               stringBuilder.append(hv);
           }
           return stringBuilder.toString();
       }
   }
   ```

4. 把key和result填到`C:\Users\{用户}\.IntelliJIdea2017.2\config\options\mybatis.xml`中对应的字段