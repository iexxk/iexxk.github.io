---
title: db-mongodb-Backup
date: 2019-05-30 09:07:04
updated: 2019-05-30 18:03:27
categories: 数据库
tags: [MongoDB]
---

## mongodb手动备份

#### 备份命令`mongodump`

```bash
mongodump --host 127.0.0.1 --port 27017 --username user --password pass --out /data/backup/ --db test --collection mycollection
#参数解释
#hsot 数据库ip
#port 数据库端口
#out 备份指定输出目录
#db 备份指定数据库
#collection 备份指定的表
```

默认备份本地运行在27017端口下的 MongoDB 实例中的所有数据库（`local` 除外），并在当前目录下生成 `dump/` 路径存放备份文件，备份以文件名区分数据库，里面以`bson`和`json`单独存表

1. 在安装好mongodb的服务器上执行`mongodump`命令就可以备份数据库了，备份的文件会在当前目录的dump里面

#### 恢复命令`mongorestore dump/`

参数同备份，其中dump为备份文件的路径

## mongodb自动备份

1. 创建脚本`mongod_bak.sh`

   ```bash
   #!/bin/sh
   DUMP=mongodump
   #备份文件临时目录
   OUT_DIR=/data/backup/mongod/tmp   
   #备份文件正式目录
   TAR_DIR=/data/backup/mongod 
   #备份文件将以备份时间保存
   DATE=`date +%Y_%m_%d_%H_%M_%S`
   #数据库操作员,建议设置个单独的用户作为备份用户
   #DB_USER=<USER>     
   #数据库操作员密码
   #DB_PASS=<PASSWORD>       
   #保留最新14天的备份
   DAYS=14                          
   #备份文件命名格式
   TAR_BAK="mongod_bak_$DATE.tar.gz"
   #远程备份ip
   #REMOTEIP=<远程服务ip>
   #远程备份用户名
   #REMOTEUSER=<远程连接用户名>
   #创建文件夹
   cd $OUT_DIR        
   #清空临时目录 
   rm -rf $OUT_DIR/*               
   #创建本次备份文件夹
   mkdir -p $OUT_DIR/$DATE          
   #执行备份命令，带用户
   #$DUMP -u $DB_USER -p $DB_PASS -o $OUT_DIR/$DATE 
   #执行备份命令，不带用户
   $DUMP -o $OUT_DIR/$DATE 
   #将备份文件打包放入正式目录
   tar -zcvf $TAR_DIR/$TAR_BAK $OUT_DIR/$DATE
   #删除14天前的旧备份
   find $TAR_DIR/ -mtime +$DAYS -delete 
   #远程备份,需要自行配置ssh证书登陆方式,需在远程提前建好备份文件目录TAR_DIR中设置的路径值
   #scp $TAR_DIR/$TAR_BAK $REMOTEUSER@$REMOTEIP:$TAR_DIR/
   ```

2. 添加执行权限`chmod +x mongod_bak.sh`

3. 执行测试`./mongod_bak.sh`，这步可忽略

4. 添加自动执行脚本功能，执行

   ```bash
   #每天凌晨2点自动执行，脚本路径更改为自己存放的路径
   echo "0 2 * * * root /root/mongod_bak.sh"  >>/etc/crontab
   #使能配置
   crontab /etc/crontab
   #检查配置是否生效
   crontab -l
   #检查crond是否运行
   service crond status
   ```

#### 备份恢复

```bash
#解压备份文件
tar -zxvf mongod_bak_2019_xx_xx_xx_xx_xx.tar.gz
#执行mongorestore进行恢复,切换到解压的备份目录里面
mongorestore tmp/
```



## 自动生成脚本及自动配置定时备份

```bash
#!/bin/bash
echo "欢迎使用mongodb自动备份配置脚本"
read -p  "请输入mongodb备份路径(/data/mongodbBackUp)：" -t 30 path #等待30秒
if    [ ! -n "$path" ]  ;then
      path="/data/mongodbBackUp"
      echo "备份路径默认设置为: $path"
else
      echo "备份路径为: $path"
fi
read -p "请输入mongodb用户名：" -t 120 dbUserName 
if    [ ! -n "$dbUserName" ]  ;then
      echo "用户名输入为空"
      exit
else
      echo "用户名为: $dbUserName"
fi
read -p "请输入mongodb密码：" -s password
if    [ -z "$password" ]  ;then
      echo "密码输入为空$password"
      exit
else
      echo -e "\n"
      read -p "请再次输入mongodb密码：" -s rpassword
	if    [ "$rpassword"x != "$password"x ]  ;then
              echo "输入密码不一致"
              exit
        else
              echo "密码设置成功"
        fi
fi
read -p "是否设置远程备份，请输入[y/n]" -n 1  remote
if    [ "$remote"x = "y"x ]  ;then
      echo -e "\n"
      echo "进入远程配置，远程备份功能需提前自行配置好ssh证书登陆,远程地址样例"
      echo "root@192.168.1.1:/backupPath/"
      read -p "请设置远程服务器地址："  scpPath
      echo "远程地址为：$scpPath"
fi
echo "正在配置中...."
echo "#!/bin/bash" >/data/mongod_bak.sh
echo -e "DATE=\`date +%Y_%m_%d_%H_%M_%S\`" >>/data/mongod_bak.sh
echo "rm -rf $path/tmp/*" >>/data/mongod_bak.sh
echo "mkdir -p $path/tmp/$DATE" >>/data/mongod_bak.sh
echo "mongodump -u $dbUserName -p $password -o $path/tmp/$DATE" >>/data/mongod_bak.sh
echo -e "tar -zcvf $path/mongod_bak_\$DATE.tar.gz $path/tmp/$DATE" >>/data/mongod_bak.sh
echo "find $path/ -mtime +14 -delete" >>/data/mongod_bak.sh
if    [ "$remote"x = "y"x ]  ;then
      echo -e "scp $path/mongod_bak_\$DATE.tar.gz $scpPath" >>/data/mongod_bak.sh
fi
chmod +x /data/mongod_bak.sh
echo "配置完成"
echo "开始设置定时备份,定时设置目录/etc/crontab"
echo "定时任务脚本生成路径/data/mongod_bak.sh"
echo "0 2 * * * root /data/mongod_bak.sh"  >>/etc/crontab
crontab /etc/crontab
crontab -l
echo "设置成功" 
```





