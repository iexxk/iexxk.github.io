---
title: SpringBoot使用jackson转xml
date: 2019-12-12 15:00:32
updated: 2019-12-12 15:11:42
categories: SpringBoot
tags: [jackson,xml]
---

## springboot 添加xml报文接口

一般的接口都是用json，这篇介绍如何用jackson写xml报文接口

### 1. 给springboot添加依赖

```groovy
compile group: 'com.fasterxml.jackson.dataformat', name: 'jackson-dataformat-xml', version: '2.10.1'
compile group: 'com.fasterxml.jackson.module', name: 'jackson-module-jaxb-annotations', version: '2.10.1'
```

### 2. 创建实体类类

#### 封装属性类

`<Element attr="s,103">value</Element>`如果不封装，就没有attr这个属性

```
@Data
public class Element {
    @JacksonXmlProperty(isAttribute = true)
    private String attr="q";

    @JacksonXmlText
    private String value;

    public Element() {
    }

    public Element(String attr) {
        this.attr = attr;
    }

    public Element(String attr, String value) {
        this.attr = attr;
        this.value = value;
    }
}
```

#### 用户测试类

```java
import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlProperty;
import com.fasterxml.jackson.dataformat.xml.annotation.JacksonXmlRootElement;
import lombok.Data;

@JacksonXmlRootElement(localName = "service")
@Data
public class XmlTestBean {
    @JacksonXmlProperty(isAttribute = true)
    private String version = "2.0";
    @JacksonXmlProperty(localName = "BODY")
    private Body body;
    @Data
    public class Body {
        @JacksonXmlProperty(localName = "TX_CODE")
        private Element txCode;
        @JacksonXmlProperty(localName = "Name")
        private Element name;
    }
    @JacksonXmlProperty(localName = "SYS_HEAD")
    private SysHead sysHead;
    @Data
    public class SysHead {
        @JacksonXmlProperty(localName = "TRAN_TIMESTAMP")
        private Element tranTimestamp;
    }
}
```

### 3. 写测试接口

```java
@RestController
@RequestMapping("/xml")
public class XmlController {
    private Logger logger=Logger.getLogger(String.valueOf(getClass()));

    /***
     * consumes为请求参数的格式 Content-Type设置为application/xml
     * produces为返回内容的格式 Content-Type设置为application/xml
     * @param xmlTestBean
     * @return
     */
    @RequestMapping(value = "/test",consumes = MediaType.APPLICATION_XML_VALUE,produces = MediaType.TEXT_XML_VALUE)
    @ResponseBody
    public XmlTestBean test(@RequestBody XmlTestBean xmlTestBean){
        logger.info("receive data: "+xmlTestBean.toString());
        xmlTestBean.setVersion(xmlTestBean.getVersion()+"0");
        XmlTestBean.Body body= xmlTestBean.getBody();
        Element name =body.getName();
        name.setAttr(name.getAttr()+"1");
        name.setValue(name.getValue()+"2");
        body.setName(name);
        body.setTxCode(new Element(body.getTxCode().getAttr()+"3",body.getTxCode().getValue()+"4"));
        xmlTestBean.setBody(body);
        return xmlTestBean;
    }
}
```

### 4. 优化返回

返回添加

```java
@Configuration
public class Config {
    /**
     * jackson 转xml 全局配置
     *
     * @param builder
     * @return
     */
    @Bean
    public MappingJackson2XmlHttpMessageConverter mappingJackson2XmlHttpMessageConverter(
            Jackson2ObjectMapperBuilder builder) {
        ObjectMapper mapper = builder.createXmlMapper(true).build();
//        设置全局返回显示 <?xml version='1.0' encoding='UTF-8'?>
        ((XmlMapper) mapper).enable(ToXmlGenerator.Feature.WRITE_XML_DECLARATION);
        //<?xml version='1.0' encoding='UTF-8'?> 改为双引号 <?xml version="1.0" encoding="UTF-8"?>
        String propName = com.ctc.wstx.api.WstxOutputProperties.P_USE_DOUBLE_QUOTES_IN_XML_DECL;
        ((XmlMapper) mapper).getFactory()
                .getXMLOutputFactory()
                .setProperty(propName, true);
        return new MappingJackson2XmlHttpMessageConverter(mapper);
    }
}
```

### 5. 测试数据

##### 请求数据

```xml
<?xml version="1.0" encoding="UTF-8"?>
<service version="2.0">
    <BODY>
        <TX_CODE attr="s,10">facecompare</TX_CODE>
        <Name attr="s,10">facecompare</Name>
        <IdentNo attr="s,10">99999</IdentNo>
        <IdentPhtFilePath attr="s,255">1.jpg</IdentPhtFilePath>
        <SpotPhtFilePath attr="s,255">1.jpg</SpotPhtFilePath>
        <OvlapPhtFlg attr="s,255">1</OvlapPhtFlg>
        <CnlNo attr="s,255">12</CnlNo>
    </BODY>
    <SYS_HEAD>
        <TRAN_TIMESTAMP attr="s,6">153907</TRAN_TIMESTAMP>
        <CONSUMER_SEQ_NO attr="s,42">137000140118100000042563</CONSUMER_SEQ_NO>
        <WS_ID attr="s,30">p5</WS_ID>
        <SERVICE_SCENE attr="s,2">01</SERVICE_SCENE>
        <CONSUMER_ID attr="s,6">137000</CONSUMER_ID>
        <SERVICE_CODE attr="s,11">11002000018</SERVICE_CODE>
        <TRAN_DATE attr="s,8">20140118</TRAN_DATE>
    </SYS_HEAD>
    <APP_HEAD>
        <USER_ID attr="s,30">00120242</USER_ID>
        <PER_PAGE_NUM attr="s,3"></PER_PAGE_NUM>
        <QUERY_KEY attr="s,256"></QUERY_KEY>
        <BRANCH_ID attr="s,9">0135</BRANCH_ID>
    </APP_HEAD>
</service>
```

##### 返回数据

```xml
<?xml version="1.0" encoding="UTF-8"?>
<service version="2.00">
    <BODY>
        <TX_CODE attr="s,103">facecompare4</TX_CODE>
        <Name attr="s,101">facecompare2</Name>
    </BODY>
    <SYS_HEAD>
        <TRAN_TIMESTAMP attr="s,6">153907</TRAN_TIMESTAMP>
    </SYS_HEAD>
</service>
```

### 源码

[xuanfong1/springLeaning](https://github.com/xuanfong1/springLeaning/tree/master/xml)

