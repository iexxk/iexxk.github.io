---
title: JavaEE-SpringBoot-thymeleaf-layui
date: 2018-03-29 09:04:55
updated: 2018-03-29 09:51:04
categories: JavaEE
tags: [SpringBoot,Java,thymeleaf,layui]
---

### SpringBoot thymelef的使用以及模版

thymelef模版配置,可以不用配置

```yaml
spring:
  thymeleaf:
    cache: false
    prefix: classpath:/templates/
    check-template-location: true
    suffix: .html
    encoding: UTF-8
    content-type: text/html
    mode: HTML5
```

1. thymelef添加依赖

   ```Xml
   		<dependency>
   			<groupId>org.springframework.boot</groupId>
   			<artifactId>spring-boot-starter-thymeleaf</artifactId>
   		</dependency>
   ```

2. 在`resource/templates`添加网页

   `${error}`接收参数，`th:action="@{/userLogin}"`表单提交地址

   ```html
           <p th:if="${error}" class="bg-danger" th:text="${error}"></p>
           <form method="post" class="layui-form" th:action="@{/userLogin}" >
               <input name="username" placeholder="用户名" >
               <input name="password" lay-verify="required" placeholder="密码">
               <input value="登录" id="login" style="width:100%;" type="submit">
           </form>
   ```

3. 添加`controller`

   ```java
   @Controller
   public class LoginControl {
       @RequestMapping(value = "/login")
       public String login(Model model)
       {
           model.addAttribute("error","跳转而已");  //设置往网页传参数
           return "login"; //跳转login.html,并接受上面的参数
       }
       @RequestMapping(value = "/userLogin", method = RequestMethod.POST)
       public String userLogin(User user, Model model) {
           model.addAttribute("error", "出现异常");
           return "login"; //更新网页返回值
       }
   }
   ```

#### layui前端样式模版

直接复制到`resource/static`资源目录即可

1. layui简单的post请求

   ```html
   <button class="layui-btn"  lay-submit="" lay-filter="addsort">增加</button>
   <script>
           layui.use(['layer', 'form'], function() {
               var layer = layui.layer //引用layer模块
                   , form = layui.form;//引用form模块
               form.on('submit(addsort)', function (data) { //addsort监听提交按钮
                   console.log(data.elem) //被执行事件的元素DOM对象，一般为button对象
                   console.log(data.form) //被执行提交的form对象，一般在存在form标签时才会返回
                   console.log(data.field) //当前容器的全部表单字段，名值对形式：{name: value}
                   $.ajax({
                       type: 'POST',
                       url: '/img/addSort',
                       dataType: 'json',
                       contentType: 'application/json',
                       data: JSON.stringify(data.field),
                       success:function (result) {
                          console.log(result);
                           if (result.code==200){
                               layer.msg('添加成功');
                           }else {
                               layer.msg(result.msg);
                           }
                       }
                   });
                   return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
               });
           });
       </script>
   ```

2. 表单数据加载

   ```java
       @RequestMapping(value = "/feedback")
       public String feedback(Model model){
           model.addAttribute("feedBacks",feedBacks);
           return "feedback";
       }
   ```

   ```Html
   <table class="layui-table">
       <thead>
       <tr>
           <th>ID</th>
           <th>用户名</th>
       </thead>
       <tbody>
       <tr th:each="feedBack:${feedBacks}">
           <td th:text="${feedBack.feedbackid}"></td>
           <td th:text="${feedBack.user.username}"></td>
       </tr>
       </tbody>
   </table>
   ```

3. 含文件图片的表单混合一起提交,原理首先使用layui绑定按钮提交

   上传图片按钮设置不自动`  auto: false`提交，然后存到文件里，然后表单提交的时候触发图片上传，以及绑定表单参数,设计时最好避免一起提交，设计可以先传好图片，然后填图片地址，分两次请求

   ```javascript
   <script>
       var uploadInst;
       var pathObj; //存文件
       layui.use(['layer', 'form'], function () {
           var layer = layui.layer
               , form = layui.form;
           form.on('submit(addpaper)', function (data) {
               if (pathObj == undefined) {
                   layer.msg("没有选择壁纸");
                   return;
               }
               var sortid= $("select option:checked").attr("id");
               //选了文件直接改参数上传
               uploadInst.config.data = {
                   paperdetail:data.field.paperdetail,
                   sortid:sortid,
                   papername:data.field.papername
               };
               uploadInst.config.auto = true;
               uploadInst.upload();
               return false; //阻止表单跳转。如果需要表单跳转，去掉这段即可。
           });
       });

       layui.use(['layer', 'upload'], function () {
           var layer = layui.layer
               , upload = layui.upload;
           //普通图片上传
           uploadInst = upload.render({
               elem: '#post-photo'
               , url: '/img/uploadpaper'
               , auto: false
               , before: function (obj) {
                   //预读本地文件示例，不支持ie8
                   obj.preview(function (index, file, result) {
                       $('#demo1').attr('src', result); //图片链接（base64）
                   });
               },
               choose: function (object) {
                   pathObj = object;
               }
               , done: function (res) {
                   if (res.code == 200) {
                       layer.msg("添加壁纸成功");
                   } else {
                       layer.msg("添加壁纸失败：" + res.msg);
                   }
                   //上传成功
               }
           });
       });
   </script>
   ```

   ```Java
       @PostMapping("/uploadpaper")
       public Msg singleFileUpload(@RequestParam("file") MultipartFile file, @RequestParam("sortid") int sortid, @RequestParam("paperdetail") String paperdetail, @RequestParam("papername") String papername) {
           List<String> urls = new ArrayList<>();
           if (file == null) {
               return ResultUtil.error(-300, "上传文件为空");
           }
           Paper paper = new Paper();
           paper.setSortid(sortid);
           paper.setPapername(papername);
           paper.setPaperdetail(paperdetail);
           try {
               Files.write(Paths.get(uploadPath + file.getOriginalFilename()), file.getBytes());
               paper.setPaperurl(imgUrl + file.getOriginalFilename());
               paperMapper.insertPaper(paper);

           } catch (Exception e) {
               e.printStackTrace();
               return ResultUtil.error(-301, e.getMessage());
           }
           return ResultUtil.success();
       }
   ```

4. 动态读取下拉框

   ```Html
   <select name="sortid" id="sortid">
      <option th:each="arrayS:${sorts}" th:text="${arrayS.sortname}" th:id="${arrayS.sortid}">默认选项</option>
    </select>
   ```

   ```java
       @RequestMapping(value = "/addwallpaper")
       public String addwallpaper(Model model){
           List<Sort> sorts;
           sorts = paperMapper.selectSort();
           model.addAttribute("sorts",sorts);
           return "addwallpaper";
       }
   ```

   ​

