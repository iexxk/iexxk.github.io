---
title: SpringBoot前后端分离架构
date: 2018-03-28 10:32:34
updated: 2018-03-28 10:32:34
categories: Java
tags: [Java,SpringBoot,SpringSecurity,vue]
---

### 架构模型（**Spring boot+vue+Spring Security**）

#### [SpringSecurity](https://vincentmi.gitbooks.io/spring-security-reference-zh/content/1_introduction.html)

是一个安全认证权限控制等spring框架依赖注入原理(ioc)

这里简单用于登陆校验

1. 添加maven依赖

   ```Xml
   		<dependency>
   			<groupId>org.springframework.boot</groupId>
   			<artifactId>spring-boot-starter-security</artifactId>
   		</dependency>
   ```


2. 新建`User`实体类

   ```java
   public class User implements UserDetails {
       private int userid;
       private String username;
       private String password;
   	
       //get,set省略
       
       @Override
       public String getUsername() {
           return username;
       }
       @JsonIgnore
       @Override
       public boolean isAccountNonExpired() {
           return true; //改为true
       }
       @JsonIgnore
       @Override
       public boolean isAccountNonLocked() {
           return true; //改为true，不然账号是锁定的
       }
       @JsonIgnore
       @Override
       public boolean isCredentialsNonExpired() {
           return true; //改为true
       }
       @JsonIgnore
       @Override
       public boolean isEnabled() {
           return true; //改为true，不然账号是禁用的
       }
       @JsonIgnore
       @Override
       public Collection<? extends GrantedAuthority> getAuthorities() {
           return null;
       }
       @JsonIgnore
       @Override
       public String getPassword() {
           return password;
       }
   }
   ```

3. 新建`UserMapper`接口连接数据库

   ```Java
   @Mapper
   public interface UserMapper {
       @Select("select * from user where username=#{username}")
       User loadUserByUsername(String username);
   }
   ```

4. 新建`UserService`用户服务,注意实现`UserDetailsService`接口

   ```Java
   @Service
   public class UserService implements UserDetailsService {
       @Autowired
       UserMapper userMapper;
       @Override
       public UserDetails loadUserByUsername(String s) throws UsernameNotFoundException {
           User user = userMapper.loadUserByUsername(s);
           if (user == null) {
               throw new UsernameNotFoundException("用户名不对");
           }
           return user;
       }
   }
   ```

5. 新建`UserUtil`工具类用户获取登陆后的用户信息

   ```java
   public class UserUtils {
       public static User getCurrentHr() {
           return (User) SecurityContextHolder.getContext().getAuthentication().getPrincipal();
       }
   }
   ```

6. 最重要的一步继承该类`WebSecurityConfigurerAdapter`，并配置,添加注解标明是配置文件

   ```Java
   @Configuration
   @EnableGlobalMethodSecurity(prePostEnabled = true)
   public class WebSecurityConfig extends WebSecurityConfigurerAdapter {
       @Autowired
       UserService userService;
       @Override
       public void configure(WebSecurity web) throws Exception {
           //解决静态资源被拦截的问题，下面的忽略拦截，下面的路径不会走安全验证
           web.ignoring().antMatchers("/index.html", "/static/**", "/login_p","/user/register");
       }
       @Override
       protected void configure(AuthenticationManagerBuilder auth) throws Exception {
           auth.userDetailsService(userService).passwordEncoder(new BCryptPasswordEncoder());//配置用户登陆服务，并配置密码加密方式，这里可以自定义加密方式
       }

       @Override
       protected void configure(HttpSecurity http) throws Exception {
           http.authorizeRequests()
                   .antMatchers("/", "/index.html").permitAll()
                   //其他地址的访问均需验证权限
                   .anyRequest().authenticated()
                   .and().formLogin()
        .loginPage("/login_p")//指定登录页是"/login_p"，输入其他地址会替跳转到该页面
               .loginProcessingUrl("/login").usernameParameter("username").passwordParameter("password").permitAll() //指定登陆接口，只能用表单，如果要json请求要添加过滤器
                   .failureHandler(new AuthenticationFailureHandler() {
                       @Override
                       public void onAuthenticationFailure(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, AuthenticationException e) throws IOException, ServletException {
                           log.info("登陆失败");
                         httpServletResponse.setContentType("application/json;charset=utf-8");
                           PrintWriter out = httpServletResponse.getWriter();
                           ObjectMapper mapper = new ObjectMapper();
                           String jsonResult;
                           if (e instanceof UsernameNotFoundException ){
                               jsonResult=e.getMessage();
                           }else if( e instanceof BadCredentialsException) {
                               jsonResult="密码输入错误，登录失败!";
                           }  else {
                               jsonResult="登录失败!";
                               log.error(e.getMessage());
                           }                      jsonResult=mapper.writeValueAsString(ResultUtil.error(-201,jsonResult));
                           out.write(jsonResult);
                           out.flush();
                           out.close();
                       }
                   }).successHandler(new AuthenticationSuccessHandler() {
                       @Override
                       public void onAuthenticationSuccess(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Authentication authentication) throws IOException, ServletException {
                           log.info("登陆成功");
                         httpServletResponse.setContentType("application/json;charset=utf-8");
                           PrintWriter out = httpServletResponse.getWriter();
                           ObjectMapper mapper = new ObjectMapper();
                           String jsonResult=mapper.writeValueAsString(ResultUtil.success(UserUtils.getCurrentHr()));
                           out.write(jsonResult);
                           out.flush();
                           out.close();
                       }
                   })
                   .and().logout().permitAll()
                   .and().csrf().disable(); //解决非thymeleaf的form表单提交被拦截问题

       }
   }
   ```

   ​

#### 常见问题

1. 输出错误`User account is locked`。

   解决：用户类设置返回true，原因自带安全机制，如果需要实现登陆错误次数，此处根据逻辑修改，并在user表添加该字段，通过数据库记录设置是否锁定。

   ```
      @Override
       public boolean isAccountNonLocked() {
           return true;
       }
   ```

2. 错误`No AuthenticationProvider found for org.springframework.security.authentication.UsernamePasswordAuthenticationToken`

   解决:`WebSecurityConfigurerAdapter`没有配置注册userService，而且必须对密码加密，这里必须设置加密方式，可以`new PasswordEncoder`实现自定加密

   ```java
       @Override
       protected void configure(AuthenticationManagerBuilder auth) throws Exception {
    		auth.userDetailsService(userService).passwordEncoder(new BCryptPasswordEncoder());
       }
   ```

3. 错误`Encoded password does not look like BCrypt`原因不识别数据库密码，有可能密码字段太短，或者被截断，另一种就是通过网页手动加密，复制进数据库也有可能不识别，解决通过代码加密插入解决

   ```java
      BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();
      String encode = encoder.encode(user.getPassword());
   ```

   ​

##### 参考

[lenve/vhr](https://github.com/lenve/vhr)

[](http://wiki.jikexueyuan.com/project/spring-security/first-experience.html)