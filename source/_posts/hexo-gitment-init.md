---
title: hexo-gitment-init
date: 2018-02-24 14:33:54
updated: 2018-04-25 20:47:32
categories: 杂谈
tags: [hexo,bolg,gitment,ruby]
---

## 自动初始化gitment评论

**暂时不采用，见不足。**

#### 需求

每次发布文章，会自动产生issue但是发布一篇就要点击`initialize comments`按钮才能初始化评论，下面的步骤通过GitHub api实现ruby脚本自动初始化评论

#### 步骤

1. 添加sitemap,参考[hexo seo优化Google添加站点地图](https://jingyan.baidu.com/article/d621e8da7f4c542864913f10.html)

   主要再配置文件`.travis.yml`添加` - npm install hexo-generator-sitemap --save`,编译后会产生一个`sitemap.xml`对应url:[http://bolg.iexxk.com/sitemap.xml](http://bolg.iexxk.com/sitemap.xml),url后面会用到

2. 在github的`setting->Developer settings-> Personal access tokens->Generate new token`生成一个新的token 勾选`repo`，记住保存好token只会显示一次

3. 在travis-ci添加`GITMENT`环境变量存储上一步生成的token，似乎GitHub不能把token明码直接放到脚本里，会导致GitHub的token失效消失

4. 新建脚本文件`comment.rb`，放到`source\`目录,一次填入自己的信息，这里新加了忽略openssl的校验，以及token通过命令传参进行传入

   ```ruby
   username = "xuanfong1" # GitHub 用户名
   new_token = ARGV.first  # GitHub Token，通过命令行参数传进来，获取第一个参数
   repo_name = "xuanfong1.github.io" # 存放 issues
   sitemap_url = "http://bolg.iexxk.com/sitemap.xml" # sitemap
   kind = "gitment" # "Gitalk" or "gitment"

   require 'open-uri'
   require 'faraday'
   require 'active_support'
   require 'active_support/core_ext'
   require 'sitemap-parser'
   # 忽略openssl校验
   require 'openssl'
   OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

   puts"Token: #{new_token}"

   sitemap = SitemapParser.new sitemap_url
   urls = sitemap.to_a

   conn = Faraday.new(:url => "https://api.github.com/repos/#{username}/#{repo_name}/issues") do |conn|
     conn.basic_auth(username, new_token)
     conn.adapter  Faraday.default_adapter
   end

   urls.each_with_index do |url, index|
     title = open(url).read.scan(/<title>(.*?)<\/title>/).first.first.force_encoding('UTF-8')
     response = conn.post do |req|
       req.body = { body: url, labels: [kind, url], title: title }.to_json
     end
     puts response.body
     sleep 15 if index % 20 == 0
   end
   ```

5. 添加脚本执行命令，在`.travis.yml`添加安装`  - gem install faraday activesupport sitemap-parser`和执行脚本` - ruby comment.rb ${GITMENT}`

   ```ruby
   language: node_js
   node_js: stable
   install:
     - npm install
     - npm install hexo-generator-sitemap --save
     - npm install hexo-generator-baidu-sitemap --save
     - gem install faraday activesupport sitemap-parser
   script:
     - hexo cl
     - hexo g
   after_script:
     - cd ./public
     - git init
     - git config user.name "xuanfong1"
     - git config user.email "xuan.fong1@163.com"
     - git add .
     - git commit -m "update"
     - git push --force --quiet "https://${BLOG_GITHUB}@${GH_REF}" master:master
     - ruby comment.rb ${GITMENT}
   branches:
     only:
       - hexo
   env:
    global:
      - GH_REF: github.com/xuanfong1/xuanfong1.github.io.git
   ```


##### 不足

1. 会初始化多余的评论，例如目录页，没做过滤
2. 编译时间长
3. 相同issues可以创建多次，而且官方没提供删除接口
4. 概率性出现验证失败

##### 错误解决

1. 证书错误

   ```
   OpenSSL::SSL::SSLError SSL_connect returned=1 errno=0 state=SSLv3 read server certificate B: certificate verify failed
   ```

   解决，在脚本添加忽略证书校验

   ```
   require 'openssl'
   OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
   ```



##### 参考

[自动初始化 Gitalk 和 Gitment 评论](https://draveness.me/git-comments-initialize)