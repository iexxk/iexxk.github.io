---
t
itle: SpringBoot前后端分离架构
date: 2018-03-28 10:32:34
updated: 2018-03-29 12:13:05
categories: Java
tags: [Java,SpringBoot,SpringSecurity,vue]
---

### 架构模型（**Spring boot+vue+Spring Security**）

#### [SpringSecurity](https://vincentmi.gitbooks.io/spring-security-reference-zh/content/1_introduction.html)

是一个安全认证权限控制等spring框架依赖注入原理(ioc)

##### 简单用于登陆校验

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
               .antMatchers("/admin/**")..hasRole("超级管理员")//改地址需要超管
               .anyRequest().authenticated()//其他地址的访问均需验证权限
               .and().formLogin()
               .loginPage("/login_p")//指定登录页是"/login_p"，输入其他地址会替跳转到该页面
               .loginProcessingUrl("/login")
               .usernameParameter("username").passwordParameter("password")
               .permitAll() //指定登陆接口，只能用表单，如果要json请求要添加过滤器
               .failureHandler(new AuthenticationFailureHandler()) //登陆失败回调
               .successHandler(new AuthenticationSuccessHandler()) //登陆成功回调
               .and().logout().permitAll()
               .and().csrf().disable(); //解决非thymeleaf的form表单提交被拦截问题
       }
   }
   ```

7. 登陆成功会自动有cookie返回，清除cookie然后测试都成功了

##### 角色权限控制

这里简单实用，没有添加角色表，user表机构

| username | password | role  |
| -------- | -------- | ----- |
| admin    | ***      | admin |
| zhangsan | ***      | user  |

8. 在用户实体类重写`getAuthorities`该方法，该方法读取用户角色并存储返回到角色数组，如果是分表，role可以存储多个依次添加即可

   ```java
       @Override
       public Collection<? extends GrantedAuthority> getAuthorities() {
           List<GrantedAuthority> authorities = new ArrayList<>();
            	//“ROLE_”由于数据库未添加，所以这里手动添加
               authorities.add(new SimpleGrantedAuthority("ROLE_" + role));
           return authorities;
       }
   ```

9. 然后在配置里添加,意思是`antMatchers`里的地址只能是`admin`角色返回

   ```Java
       http.authorizeRequests()
                   .antMatchers("/flower/imgUpload", "/flower/ddClass").hasRole("admin") //这两个地址需要管理员角色
   ```

10. 现在已经能控制角色权限了，但是权限不足返回不友好，这里设置权限不足，返回提示信息

    ```Java
    .exceptionHandling().accessDeniedHandler(new AccessDeniedHandler() {
        @Override
        public void handle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, AccessDeniedException e) throws IOException, ServletException {
            log.info("权限不足");
        }
    });
    ```

##### 菜单角色管理

主要方法是设置过滤器

11. 在配置文件添加

    ```Java
     .withObjectPostProcessor(new ObjectPostProcessor<FilterSecurityInterceptor>() {
        @Override
    	public <O extends FilterSecurityInterceptor> O postProcess(O o) {
        	o.setSecurityMetadataSource(urlFilterInvocationSecurityMetadataSource);
            o.setAccessDecisionManager(urlAccessDecisionManager);
            return o;
        }
     })
    ```

12. 添加`urlFilterInvocationSecurityMetadataSource`

    ```java
    @Component
    public class UrlFilterInvocationSecurityMetadataSource implements FilterInvocationSecurityMetadataSource {
        @Autowired
        MenuService menuService;
        AntPathMatcher antPathMatcher = new AntPathMatcher();
        @Override
        public Collection<ConfigAttribute> getAttributes(Object o) throws IllegalArgumentException {
            //获取请求地址
            String requestUrl = ((FilterInvocation) o).getRequestUrl();
            if ("/login_p".equals(requestUrl)) {
                return null;
            }
            List<Menu> allMenu = menuService.getAllMenu();
            for (Menu menu : allMenu) {
                if (antPathMatcher.match(menu.getUrl(), requestUrl)&&menu.getRoles().size()>0) {
                    List<Role> roles = menu.getRoles();
                    int size = roles.size();
                    String[] values = new String[size];
                    for (int i = 0; i < size; i++) {
                        values[i] = roles.get(i).getName();
                    }
                    return SecurityConfig.createList(values);
                }
            }
            //没有匹配上的资源，都是登录访问
            return SecurityConfig.createList("ROLE_LOGIN");
        }
        @Override
        public Collection<ConfigAttribute> getAllConfigAttributes() {
            return null;
        }
        @Override
        public boolean supports(Class<?> aClass) {
            return FilterInvocation.class.isAssignableFrom(aClass);
        }
    }
    ```

13. 添加`urlAccessDecisionManager`

    ```Java
    @Component
    public class UrlAccessDecisionManager implements AccessDecisionManager {
        @Override
        public void decide(Authentication authentication, Object o, Collection<ConfigAttribute> collection) throws AccessDeniedException, AuthenticationException {
            Iterator<ConfigAttribute> iterator = collection.iterator();
            while (iterator.hasNext()) {
                ConfigAttribute ca = iterator.next();
                //当前请求需要的权限
                String needRole = ca.getAttribute();
                if ("ROLE_LOGIN".equals(needRole)) {
                    if (authentication instanceof AnonymousAuthenticationToken) {
                        throw new BadCredentialsException("未登录");
                    } else
                        return;
                }
                //当前用户所具有的权限
                Collection<? extends GrantedAuthority> authorities = authentication.getAuthorities();
                for (GrantedAuthority authority : authorities) {
                    if (authority.getAuthority().equals(needRole)) {
                        return;
                    }
                }
            }
            throw new AccessDeniedException("权限不足!");
        }
        @Override
        public boolean supports(ConfigAttribute configAttribute) {
            return true;
        }
        @Override
        public boolean supports(Class<?> aClass) {
            return true;
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

###### 详情

```java
@Override
    protected void configure(HttpSecurity http) throws Exception {
        http.authorizeRequests()
                .antMatchers("/flower/imgUpload", "/flower/ddClass").hasRole("admin") //这两个地址需要管理员角色
                //其他地址的访问均需验证权限
                .anyRequest().authenticated()
                .and().formLogin()
                //指定登录页是"/login"
                .loginPage("/login_p")
                .loginProcessingUrl("/login").usernameParameter("username").passwordParameter("password").permitAll()
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
                        }
                        jsonResult=mapper.writeValueAsString(ResultUtil.error(-201,jsonResult));
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
                .and().csrf().disable() //解决非thymeleaf的form表单提交被拦截问题
                .exceptionHandling().accessDeniedHandler(new AccessDeniedHandler() {
                    @Override
                    public void handle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, AccessDeniedException e) throws IOException, ServletException {
                        log.info("登陆失败");
                        httpServletResponse.setContentType("application/json;charset=utf-8");
                        PrintWriter out = httpServletResponse.getWriter();
                        ObjectMapper mapper = new ObjectMapper();
                        String jsonResult;
                        jsonResult="权限不足";
                        jsonResult=mapper.writeValueAsString(ResultUtil.error(-201,jsonResult));
                        out.write(jsonResult);
                        out.flush();
                        out.close();
                    }
                });
```

