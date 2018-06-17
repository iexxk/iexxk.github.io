---
title: Tools-Jenkins-pipeline
date: 2018-06-04 14:33:16
updated: 2018-06-10 14:47:58
categories: Tools
tags: [Jenkins,pipeline]
---

## jenkins使用pipeline

脚本名词解释

##### `pipeline` **<必须>** Pipeline是CD管道的用户定义模型。Pipeline的代码定义了您的整个构建过程，通常包括构建应用程序，测试和交付应用程序的阶段。 

##### `agent` **<必须>** 定义pipeline的执行环境，必须存在

##### `stages`<阶段> 包含多个子阶段stage('子阶段名')

 jenkins 的工作空间目录 `/var/jenkins_home/workspace/`

### node vs agent 区别

agent是声明性的pipelines，node是脚本性的pipelines

## 实践

#### pipeline使用gradle

学习到如何使用工具，和配置工具全局变量

1. 配置工具`系统管理->全局工具配置->Gradle->Gradle 安装`

   name：gradle4.8

   - [x] 自动安装

   版本 Gradle 4.8

   `Apply->Save`即可

   注释：如果没有Gradle设置，先去安装Gradle插件，默认推荐设置是安装了的

2. 编写Jenkinsfile进行测试

   ````groovy
   #!/usr/bin/env groovy Jenkinsfile
   node {
   	def gradleHome = tool 'gradle4.8'   //这里的gradle4.8要和gradle工具的配置里的name要一致
   	env.PATH = "${gradleHome}/bin:${env.PATH}"
   	stage('build') {
   		sh 'gradle -v'
   	}
   }
   ````

#### pipeline使用gradle打包java spring boot

```groovy
#!/usr/bin/env groovy Jenkinsfile
node {
    def gradleHome = tool 'gradle4.8'  //这里的gradle4.8要和gradle工具的配置里的name要一致
    env.PATH = "${gradleHome}/bin:${env.PATH}"
    stage('gradle build') {
        if (isUnix()) {
            //sh './gradlew clean :eurekaserver:build'  //这里会自动下载项目里的gradle版本(4.7)
            sh 'gradle clean :eurekaserver:build' //使用jenkns安装的gradle工具(4.8)
        } else {
           // bat 'gradlew.bat clean :eurekaserver:build'
            bat 'gradle clean :eurekaserver:build'
        }
    }
}
```

#### 打包jar为镜像

```groovy
#!/usr/bin/env groovy Jenkinsfile
node {
    def gradleHome = tool 'gradle4.8'  //这里的gradle4.8要和gradle工具的配置里的name要一致
    env.PATH = "${gradleHome}/bin:${env.PATH}"
    stage('gradle build') {
        if (isUnix()) {
            //sh './gradlew clean :eurekaserver:build'  //这里会自动下载项目里的gradle版本(4.7)
            sh 'gradle clean :eurekaserver:build' //使用jenkns安装的gradle工具(4.8)
        } else {
           // bat 'gradlew.bat clean :eurekaserver:build'
            bat 'gradle clean :eurekaserver:build'
        }
    }
    stage('docker build image'){
        dir('eurekaserver'){  //dockerfile的跟目录
            docker.build("springcould/eurekaserver:${env.BUILD_NUMBER}")
        }
    }
}
```

#### 运行镜像

```groovy
#!/usr/bin/env groovy Jenkinsfile
node {
    def gradleHome = tool 'gradle4.8'  //这里的gradle4.8要和gradle工具的配置里的name要一致
    env.PATH = "${gradleHome}/bin:${env.PATH}"
    stage('gradle build') {
        if (isUnix()) {
            sh 'gradle clean :eurekaserver:build' //使用jenkns安装的gradle工具(4.8)
        } else {
            bat 'gradle clean :eurekaserver:build'
        }
    }
    stage('docker build image'){
        dir('eurekaserver'){  //dockerfile的跟目录
            docker.build("springcould/eurekaserver:${env.BUILD_NUMBER}")
        }
    }
    stage('docker run Application'){
        sh "docker run -p 8091:8091 springcould/eurekaserver:${env.BUILD_NUMBER}"
    }
}
```

#### pipeline 环境变量选择设置

###### `**严重注意**`这个需要第二次运行才会生效，第一次设置之后运行，不会出来，第二次拉去运行才会出来

```groovy
#!/usr/bin/env groovy Jenkinsfile
pipeline {
    agent any
    parameters {
        choice(name: 'door_choice',
                choices: 'one\ntwo\nthree\nfour',
                description: 'What door do you choose?')
    }
    stages {
        stage('build') {
            steps {
                echo "${params.door_choice}"
            }
        }
    }
}
```

#### pipeline agent版gradle脚本

not support `tool "gradle4.8"`单个设置

```groovy
#!/usr/bin/env groovy Jenkinsfile
pipeline {
    agent any
    parameters {
        choice(name: 'door_choice',
                choices: 'one\ntwo\nthree\nfour',
                description: 'What door do you choose?')
    }
    stages {
        stage('build') {
            tools{
                gradle "gradle4.8"
            }
            steps {
                echo "${params.door_choice}"
                sh 'gradle -v'
            }
        }
    }
}
```

#### 申明式使用脚本式语言`script`

```groovy
#!/usr/bin/env groovy Jenkinsfile

pipeline {
    agent any
    parameters {
        choice(name: 'project_choice',
                choices: 'eurekaserver\neurekaclient\neurekafeign\neurekazuul',
                description: '你要编译构建那个项目?')
    }
    stages {
        stage('docker build'){
            steps{
               dir("${params.project_choice}"){
                   sh "pwd"
                   script {  //需要用script包裹，就能使用脚本式语言
                       docker.build("my-image:${env.BUILD_ID}")
                   }
               }
            }
        }
    }
}
```

#### 环境变量

env.BUILD_ID 当前的编译id，和Jenkins versions 1.597+ 的env.BUILD_NUMBER一样

env.JOB_NAME 当前项目名

env.JENKINS_URL only available if Jenkins URL set in "System Configuration"

` git diff HEAD^ eurekaserver/` 和上个版本比较eurekaserver目录，可以不要



### 参考

https://github.com/arun-gupta/docker-jenkins-pipeline