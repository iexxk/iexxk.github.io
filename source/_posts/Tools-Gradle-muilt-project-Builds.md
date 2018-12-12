---
title: Tools-Gradle-muilt-project-Builds
date: 2018-05-11 17:09:29
updated: 2018-12-12 10:47:58
categories: Tools
tags: [Gradle,Tools]
---

### 多项目构建

##### 初始化顶级项目

1. 项目初始化

   ```powershell
   mkdir multi-project
   cd multi-project
   gradle init
   ```

2. 顶级构建，也就是采用跟项目的配置，从而减少子项目的重复配置，可以把子项目的公共配置抽离到跟项目配置里。

   ```groovy
   //跟项目build.gradle添加
   allprojects {
       repositories {
           jcenter() //将jcenter仓库配置到所有项目
       }
   }
   subprojects {
       version = '1.0' //设置版本号
   }
   ```

##### 添加Groovy library子项目

1. 执行`mkdir multi-library`创建一个子项目名为`multi-library`

2. 进入`multi-library`子项目根目录，新建一个`build.gradle`

   ```groovy
   //multi-library/build.gradle
   apply plugin : 'groovy'
   dependencies {
       compile 'org.codehaus.groovy:groovy:2.4.10'
       testCompile 'org.spockframework:spock-core:1.0-groovy-2.4', {
           exclude module : 'groovy-all'
       }
   }
   ```

3. 修改顶级项目根项目的`settings.gradle`,添加`include 'multi-library'`

4. 完善子项目，创建两个目录`mkdir -p multi-library/src/main/groovy/greeter`和`mkdir -p multi-library/src/test/groovy/greeter`

5. 在目录`src/main/groovy/greeter`新建`GreetingFormatter.groovy`文件

   ```groovy
   //multi-library/src/main/groovy/greeter/GreetingFormatter.groovy
   package greeter
   import groovy.transform.CompileStatic
   @CompileStatic
   class GreetingFormatter {
       static String greeting(final String name) {
           "Hello, ${name.capitalize()}"
       }
   }
   ```

6. 在目录`src/test/groovy/greeter`新建`GreetingFormatterSpec.groovy`文件

   ```groovy
   //multi-library/src/test/groovy/greeter/GreetingFormatterSpec.groovy
   package greeter
   import spock.lang.Specification
   class GreetingFormatterSpec extends Specification {
       def 'Creating a greeting'() {
           expect: 'The greeting to be correctly capitalized'
           GreetingFormatter.greeting('gradlephant') == 'Hello, Gradlephant'

       }
   }
   ```

7. 最后在顶级项目的根目录运行`./gradlew build`，到此一个项目依赖一个子项目就完成了

##### 添加一个java 子项目

1. 执行`mkdir java-demo`创建一个子项目名为`java-demo`

2. 进入`java-demo`子项目根目录，新建一个`build.gradle`

   ```groovy
   apply plugin : 'java' 
   apply plugin : 'application' 
   ```

3. 完善子项目，创建目录`mkdir -p  java-demo/src/main/java/greeter`

4. 修改顶级项目根项目的`settings.gradle`,添加`include 'java-demo'`

5. 在目录`java-demo/src/main/java/greeter`新建`Greeter.java`文件

   ```java
   package greeter;

   public class Greeter {
       public static void main(String[] args) {
           final String output = GreetingFormatter.greeting(args[0]);
           System.out.println(output);
       }
   }
   ```

6. 进入`java-demo`子项目根目录，修改`build.gradle`

   ```
   apply plugin : 'java' 
   apply plugin : 'application' 
   mainClassName = 'greeter.Greeter'
   ```

7. 最后在顶级项目的根目录运行`./gradlew build`,会出现依赖错误

   ```
   * What went wrong:
   Execution failed for task ':java-demo:compileJava'.
   > Compilation failed; see the compiler error output for details.
   ```

8. 解决，进入`java-demo`子项目根目录，修改`build.gradle`

   ```
   apply plugin : 'java' 
   apply plugin : 'application' 
   mainClassName = 'greeter.Greeter'
   dependencies {
       compile project(':multi-library') 
   }
   ```

9. 重新执行`./gradlew build`，编译成功

10. 添加test测试编译，进入`java-demo`子项目根目录，修改`build.gradle`

   ```groovy
   apply plugin : 'java' 
   apply plugin : 'application' 
   apply plugin : 'groovy'
   mainClassName = 'greeter.Greeter'
   dependencies {
       compile project(':multi-library') 
       testCompile 'org.spockframework:spock-core:1.0-groovy-2.4', {
       	exclude module : 'groovy-all'
       }
   }
   ```

11. 创建测试目录`mkdir -p  java-demo/src/test/groovy/greeter`，添加`GreeterSpec.groovy`文件

    ```groovy
    //java-demo/src/test/groovy/greeter/GreeterSpec.groovy
    package greeter

    import spock.lang.Specification

    class GreeterSpec extends Specification {

        def 'Calling the entry point'() {

            setup: 'Re-route standard out'
            def buf = new ByteArrayOutputStream(1024)
            System.out = new PrintStream(buf)

            when: 'The entrypoint is executed'
            Greeter.main('gradlephant')

            then: 'The correct greeting is output'
            buf.toString() == "Hello, Gradlephant\n".denormalize()
        }
    }
    ```

12. 单项目编译，执行`./gradlew :java-demo:test` 其中java-demo为项目名，test为那种编译类型，也可以执行去子项目跟目录执行`../gradlew test`进行单模块编译


##### 添加文档子项目

1. 在顶级项目的`build.gradle`添加插件`asciidoctor`该插件的作用主要是将文档生成网页文件

   ```groovy
   plugins {
     //apply false将插件添加到整个项目中，但不会将其添加到根项目中。
     id 'org.asciidoctor.convert' version '1.5.6' apply false  //文档插件
   }
   ```

2. 创建文档项目目录，在顶级项目跟目录，执行`mkdir docs`

3. 然后在docs目录新建个`build.gradle`，在里头添加如下内容

   ```groovy
   apply plugin : 'org.asciidoctor.convert'  //将插件用于该子项目
   //asciidoctor任务
   asciidoctor {
       sources {
           include 'greeter.adoc'  //文档资源文件，需要自己新建
       }
   }
   //将asciidoctor任务添加到构建生命周期中，以便如果为顶级项目执行构建，则也将构建文档。
   build.dependsOn 'asciidoctor' 
   ```

4. 修改顶级项目根项目的`settings.gradle`,添加`include 'docs'`

5. 然后新建个文档`docs/src/docs/asciidoc/greeter.adoc`,没有该目录创建就行,内容随便，后面会把此文件文档转为网页文件

   ```tex
   = Greeter Command-line Application

   A simple application demonstrating the flexibility of a Gradle multi-project.

   == Installation

   Unpack the ZIP or TAR file in a suitable location

   == Usage

   [listing]
   ----
   $ cd greeter-1.0
   $ ./bin/greeter gradlephant

   Hello, Gradlephant
   ----
   ```

6. 然后在顶级项目跟目录，运行task任务`asciidoctor`,执行`./gradlew asciidoctor`

7. 会在目录`docs/build/asciidoc/html5`目录生成网页文件`greeter.html`

##### 将文档包含到发布的项目

1. 要将文档包含到发布的项目的目录可以新建task任务即可，修改`java-demo`项目的配置文件`build.gradle`增加如下内容

   ```groovy
   distZip {
       from project(':docs').asciidoctor, { 
           into "${project.name}-${version}"
       }
   }
   distTar {
       from project(':docs').asciidoctor, {
           into "${project.name}-${version}"
       }
   }
   ```

2. 然后重新编译文件即可，在顶级项目跟目录执行`./gradlew build`

3. 最后会在`java-demo//build/distributions`目录生成两个`greeter-1.0.zip` 和 `greeter-1.0.tar`，里面包含了编译好了的网页文件

##### 整理顶级构建脚本

在java-demo和muilt-library项目中有相同的配置，这里把他们抽到顶级项目里配置

1. 在顶级项目的`build.gradle`里添加公共配置

   ```groovy
   configure(subprojects.findAll {it.name == 'java-demo' || it.name == 'multi-library'} ) { //指定配置那些项目

       apply plugin : 'groovy'
       dependencies {
           testCompile 'org.spockframework:spock-core:1.0-groovy-2.4', {
               exclude module : 'groovy-all'
           }
       }
   }
   ```

2. 删除子项目公有的配置，最终所有`build.gradle`配置如下

   ```groovy
   //顶级项目build.gradle
   plugins {
     //apply false将插件添加到整个项目中，但不会将其添加到根项目中。
     id 'org.asciidoctor.convert' version '1.5.6' apply false  //文档插件
   }
   allprojects {
       repositories {
           jcenter() //将jcenter仓库配置到所有项目
       }
   }
   subprojects {
       version = '1.0' //设置版本号
   }
   configure(subprojects.findAll {it.name == 'java-demo' || it.name == 'multi-library'} ) { 

       apply plugin : 'groovy'

       dependencies {
           testCompile 'org.spockframework:spock-core:1.0-groovy-2.4', {
               exclude module : 'groovy-all'
           }
       }
   }
   //----------------------------------------------------------
   //multi-library项目build.gradle
   dependencies {
       compile 'org.codehaus.groovy:groovy:2.4.10'
   }
   //-----------------------------------------------------------
   //java-demo项目build.gradle
   apply plugin : 'java' 
   apply plugin : 'application' 
   mainClassName = 'greeter.Greeter'

   dependencies {
       compile project(':multi-library') 
   }

   distZip {
       from project(':docs').asciidoctor, { 
           into "${project.name}-${version}"
       }
   }
   distTar {
       from project(':docs').asciidoctor, {
           into "${project.name}-${version}"
       }
   }
   ```

3. 最后执行`./gradlew clean build`重新构建

## 总结

1. 子项目只需`build.gradle`配置即可，且子项目不能gradle init

2. 要父项目包含子项目，需要在`setting.gradle`设置`include '项目名'`

3. 子项目依赖其他子项目只需要设置`compile project(':子项目名') `

4. 插件需要在最顶部定义

5. 运行单模块执行`./gradlew :子项目名:构建命令`构建命令目前包括test、build、clean

6. 抽离子项目共有配置到父项目用`configure`

7. 常用命令

   ```groovy
   gradle :eurekaserver:build //执行子项目eurekaserver构建build命令
   ```

   

   