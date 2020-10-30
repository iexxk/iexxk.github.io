---
title: python-base
date: 2020-09-24 14:12:20
updated: 2020-10-30 17:07:45
categories: python
tags: [python]
---

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

问题：网上说依赖慢，依赖乱，未实际体验

#### 方案三：[poetry](https://github.com/python-poetry/poetry)

[官方文档](https://python-poetry.org/docs/)

包依赖管理文件`pyproject.toml`

```bash
# mac zsh安装步骤
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
# 当前终端临时生效
source $HOME/.poetry/env
# 终端永久生效
echo 'export PATH="$PATH:$HOME/.poetry/bin"' >> ~/.zshrc
# 设置虚拟环境安装到项目目录，如果设置改设置，所有项目的虚拟目录都默认到了~/Library/Caches/pypoetry/virtualenvs该路径下面
poetry config virtualenvs.in-project true
```

PyCharm安装插件`Poetry`

poetry虚拟环境目录`~/Library/Caches/pypoetry/virtualenvs`

```bash
#查看虚拟环境
poetry env list 
#移除虚拟环境
poetry env remove python3
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



