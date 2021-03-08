---
title: python-base
date: 2020-09-24 14:12:20
updated: 2021-03-02 17:33:04
categories: python
tags: [python]
---

## python pip 国内仓库代理

在改配置文件 `vim ~/.pip/pip.conf`添加如下内容，没有该文件创建该文件及目录

```properties
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
```

## python 版本切换工具-[pyenv](https://github.com/pyenv/pyenv)

常用命令[commands](https://github.com/pyenv/pyenv/blob/master/COMMANDS.md)

常见问题[issues](https://github.com/pyenv/pyenv/issues/1643)

```bash
#更新安装
brew update
brew install pyenv
#添加补齐
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.zshrc
#重启shell
exec "$SHELL"
# 可选，但建议安装python依赖项
brew install openssl readline sqlite3 xz zlib bzip2 libiconv libzip
#查看支持的版本
pyenv install --list
#安装指定版本
pyenv install 2.7.15
#如遇安装问题，升级Xcode command line tools和配置下面的环境变量，上面可选变必选
vim ~/.zshenv

#zlib
#For compilers to find zlib you may need to set:
export LDFLAGS="-L/usr/local/opt/zlib/lib"
export CPPFLAGS="-I/usr/local/opt/zlib/include"
#For pkg-config to find zlib you may need to set:
export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"

#bzip2
#If you need to have bzip2 first in your PATH, run:
export PATH="/usr/local/opt/bzip2/bin:$PATH"
#For compilers to find bzip2 you may need to set:
export LDFLAGS="-L/usr/local/opt/bzip2/lib"
export CPPFLAGS="-I/usr/local/opt/bzip2/include"

#libiconv
#If you need to have libiconv first in your PATH, run:
export PATH="/usr/local/opt/libiconv/bin:$PATH"
#For compilers to find libiconv you may need to set:
export LDFLAGS="-L/usr/local/opt/libiconv/lib"
export CPPFLAGS="-I/usr/local/opt/libiconv/include"

```

## python包管理工具

包管理工具是指类似maven/gradle的管理工具，和maven包管理不同的是，python还要考虑虚拟环境，有了虚拟环境，才能在不同的虚拟环境安装不同版本的包，就相当于一个项目对应一个虚拟环境，一个虚拟环境安装不同的包

## 名词介绍

`pip`包管理

`virtualenv`虚拟环境

### 不同的管理工具及方案

#### 方案一：传统模式`pip`+`virtualenv`

包依赖管理文件`requirements.txt`

问题：在pycharm中莫名其妙的找不到已经安装的包(eg:pandas_bokeh)

#### 方案二：`pipenv`

包依赖管理文件`Pipfile`

问题：网上说依赖慢，依赖乱

```bash
brew install pipenv
#设置虚拟环境默认建立在项目目录
echo 'export PIPENV_VENV_IN_PROJECT=true' >> ~/.zshenv
```

参考：[PyCharm+Pipenv虚拟环境作开发和依赖管理](https://my.oschina.net/u/4274818/blog/3236481)

#### ~~方案三：[poetry](https://github.com/python-poetry/poetry)~~ 

问题：放弃有各种bug，对PyCharm兼容差，安装依赖经常失败，pycharm不能自动识别poetry

[官方文档](https://python-poetry.org/docs/)

包依赖管理文件`pyproject.toml`

```bash
# mac zsh安装步骤,注意后面用python3安装
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
# 当前终端临时生效
source $HOME/.poetry/env
# 终端永久生效
echo 'export PATH="$PATH:$HOME/.poetry/bin"' >> ~/.zshrc
# 设置虚拟环境安装到项目目录，如果设置改设置，所有项目的虚拟目录都默认到了~/Library/Caches/pypoetry/virtualenvs该路径下面
poetry config virtualenvs.in-project true

brew update
brew install pyenv

#卸载
wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
python3 get-poetry.py --uninstall
rm get-poetry.py
```

PyCharm安装插件`Poetry`

poetry虚拟环境目录`~/Library/Caches/pypoetry/virtualenvs`

```bash
#查看虚拟环境
poetry env list 
#移除虚拟环境
poetry env remove python3
```



### pyproject.toml 配置文件详解

```toml
[tool.poetry]
name = "pythonleaning"
version = "0.1.0"
description = ""
authors = ["xuanleung <exxk.lx@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.8"
pandas = "^1.1.4"
nupy = "^0.1.1"
pymongo = "^3.11.1"
matplotlib = "^3.3.3"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

#配置代理仓库
[[tool.poetry.source]]
name = "aliyun"
url = "https://mirrors.aliyun.com/pypi/simple/"
```





## python使用数据库

### python与mongodb

```python
import pymongo
#连接数据库
fund = pymongo.MongoClient('mongodb://ip.cn:14011/')["db_name"]
#条件查询数据，0代表不返回该字段，1代表返回该字段,sort第二个参数1升序，-1降序
result = fund["tb_name"].find({"name": "1"}, {"_id": 0, "name": 1}).sort("name",-1)
```

## python之pandas

### DataFrame

#### [loc](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html)

```python
#返回为'列标'的那列数据
Series=df['col']
#给满足条件的行row和列col赋新值
df.loc['row','col']='赋新值'
#单列计算，该列全部乘以2
df['col2'] = df['col1'].map(lambda x: x*2)
#不用lambda表达式为下方写法
define square(x):
    return (x * 2)
df['col2'] = df['col1'].map(square)
#多列计算用apply,例如col3 = col1 + 2 * col2:
df['col3'] = df.apply(lambda x: x['col1'] + 2 * x['col2'], axis=1)
#图表分开展示
df.plot.line(subplots=True)

# 显示所有列
pd.set_option('display.max_columns', None)
# 显示所有行
# pd.set_option('display.max_rows', None)
# 设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)
# 设置显示的宽度
pd.set_option('display.width', 5000)

```





## 参考

[一款让Python开发效率提升50%的工具包](https://www.modb.pro/db/31508)

[Python in 2020 (1) - 环境搭建](https://lenciel.com/2020/07/python-in-2020-part1-env-setup/)



