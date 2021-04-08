---
title: spring-Cache
date: 2021-04-08 09:29:06
updated: 2021-04-08 16:52:40
categories: Spring
tags: [Spring,Cacheable]
---

发现项目里面的redis缓存与数据库的数据混乱不一致，因为很多自定义的数据库update方法更新了数据库，但是并没有更新redis，于是想在底层实现自动缓存

## Spring cache简单使用

[教程](https://www.baeldung.com/spring-cache-tutorial)

1. 引入依赖

   ```groovy
   compile group: 'org.springframework.boot', name: 'spring-boot-starter-cache', version: '2.1.1.RELEASE'
   compile group: 'org.springframework.boot', name: 'spring-boot-starter-data-redis', version: '2.1.1.RELEASE'
   ```

2. 添加redis缓存的中间件，缓存的中间件也可以不用redis用其他中间件一样的，可选generic,ehcache,hazelcast,infinispan,jcache,redis,guava,simple,none

   ```
   spring.redis.host=gt163.cn
   spring.redis.port=14043
   ```

3. 开启cache功能,在`@SpringBootApplication`启动类或`@Configuration`配置类上面添加该注解`@EnableCaching`

4. 使用缓存功能,在要缓存的方法上面或者类上面添加注解`@Cacheable("<redis里面的唯一key，也可以叫表名>")`

   ```java
       //例如
       @Cacheable("user_info")
       public User findById(String id) {
           return userDao.findById(id);
       }
   ```

   [![cYVwvT.png](https://z3.ax1x.com/2021/04/08/cYVwvT.png)](https://imgtu.com/i/cYVwvT)](https://imgtu.com/i/cJAnB9)

## 常见几个注解

```java
//开启缓存功能
@EnableCaching
//缓存没有数据查执行方法里面的内容，然后将执行的结果缓存起来，缓存里面有直接读缓存，不会执行方法里面的内容，参数会作为key
@Cacheable("user_info")
public User findById(String id)
//参数unless对结果进行判断，condition对参数进行判断  
//缓存不管是否存在都会执行方法里面的内容并更新缓存   
@CachePut(value="user_info")   
//删除缓存   
@CacheEvict(value="user_info")
//多个缓存分组   
@Caching
//注解到类上面，类里面的方法只需要添加注解@Cacheable，不用在指定cacheName了
@CacheConfig(cacheNames={"user_info"})
   
```

## redis缓存mongo数据库表的架构设计

### 设计方案一

详细代码见github:[iexxk/springLeaning:mongo](https://github.com/iexxk/springLeaning/tree/master/mongo)

在`BaseDao`接口层添加缓存注解，然后在各个子类继承实现，达到通用缓存框架的配置

`BaseDao.java`

```java
@CacheConfig(cacheNames = {"mongo"})
public interface BaseDao<T, ID> {
  	//#root.target.table为SpEL表达式，当前被调用的目标对象实例的table的值
    @Cacheable(key = "#root.target.table+#p0",condition ="#root.target.isCache")
    T findById(ID id);
    @CachePut(key = "#root.target.table+#p0.id",condition ="#root.target.isCache")
    <S extends T> S save(S entity);
    @CacheEvict(key = "#root.target.table+#p0",condition ="#root.target.isCache")
    void deleteById(ID id);
  	//删除所有是删除mongo所有的表，粒度不能到key
    @CacheEvict(key="#root.target.table",allEntries=true,condition="#root.target.isCache")
    void deleteAll();
  	//用来设置是否开启缓存
    void enableCache(boolean isCache);
}
```

`BaseDaoImpl.java`

```java
public class BaseDaoImpl<T, ID> implements BaseDao<T, ID> {
    private SimpleMongoRepository<T, ID> mongoRepository;
    private Class<T> entityType;
    private Class<ID> identifierType;
    protected MongoTemplate mongoTemplate;
		//这里用来存储表的名字
    public String table;
  	//这里用来判断是否开启redis缓存
    public Boolean isCache = false;
		//构造方法初始化
    public BaseDaoImpl() {
        ResolvableType resolvableType = ResolvableType.forClass(getClass());
        entityType=(Class<T>)resolvableType.as(BaseDao.class).getGeneric(0).resolve();
        identifierType=(Class<ID>)resolvableType.as(BaseDao.class).getGeneric(1).resolve();
      	//初始化表的名字，用“:”是因为可以在redis里面进行分类
        table=entityType.getSimpleName()+":";
    }
  
    @Autowired
    public void setMongoTemplate(MongoTemplate mongoTemplate) {
        this.mongoTemplate = mongoTemplate;
        MappingMongoEntityInformation<T, ID> entityInformation = new MappingMongoEntityInformation<T, ID>(
                new BasicMongoPersistentEntity<>(ClassTypeInformation.from(entityType)), identifierType);
        mongoRepository = new SimpleMongoRepository<T, ID>(entityInformation, mongoTemplate);
    }

    @Override
    public T findById(ID id) {
        return mongoTemplate.findOne(Query.query(Criteria.where("Id").is(id.toString())), entityType);
    }
  
      @Override
    public void enableCache(boolean isCache) {
        this.isCache = isCache;
    }
}
```

下面开始进行使用,新建一个`UserDao.jva`

```java
public interface UserDao extends BaseDao<User, String> {
    void updateAddNumById(String id); //自定义的接口
}
```

`UserDaoImpl.jva`

```java
@Repository
public class UserDaoImpl extends BaseDaoImpl<User, String> implements UserDao {
		
    public UserDaoImpl() {
        super.enableCache(true); //这里进开启缓存设置，默认是不开启的
    }

    @Override
    public void updateAddNumById(String id) {
    }
}
```

最好调用`findById`就会进行缓存了

[![cYVQv8.png](https://z3.ax1x.com/2021/04/08/cYVQv8.png)](https://imgtu.com/i/cYVQv8)

#### 存在的问题

1. 因为`cacheNames`也就是表名不支持SpEL，因此获取不到表名，因此设计是，表就用通用`mongo`字段做完通用表，然后key里面才是表加id的设计，因此也导致了`deletAll`是删除所有的表，因为`deletAll`基本不会用到，也还可以接受，就算用到了，只是缓存没了，还是能从数据库重建缓存

### 参考

[史上超详细的SpringBoot整合Cache使用教程](https://www.javazhiyin.com/4618.html)

