---
title: Linux-Tools-on-my-zsh
date: 2018-04-30 09:42:41
updated: 2018-05-01 18:31:32
categories: Linux
tags: [Linux,zsh]
---

## ZSH

zsh (Mac 系统自带，无需安装)。

安装[**Oh-My-Zsh**](http://ohmyz.sh/)管理zsh的配置工具 `sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"`

### 常用功能

配置文件`cat ~/.zshrc`

#### 命令历史记录功能`ctrl+r`

历史记录存放在`cat ~/.zsh_history`

`ctrl+r`搜索命令历史记录,`!!`执行上一条命了

补全`TAB`

#### 命令别名`alias`

在`~/.zshrc`中添加`alias name=command`即可

查看所有命令别名`alias`

#### 插件

git

### iterm2 修改[配色](https://github.com/mbadolato/iTerm2-Color-Schemes)

### Solarized Dark Higher Contrast

在这里找到自己https://github.com/mbadolato/iTerm2-Color-Schemes/tree/master/schemes喜欢的

然后保存文件，双击安装，然后color->color下来框选择自己安装的

#### item2 安装[powerlevel9k](https://github.com/bhilburn/powerlevel9k)主题

```powershell
git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k #下载主题
vim ~/.zshrc #编辑配置文件设置主题ZSH_THEME="powerlevel9k/powerlevel9k"，去用户名添加 DEFAULT_USER="your user name"
git clone https://github.com/supermarin/powerline-fonts.git #下载字体
```

安装字体，双击`/Monaco/Monaco for Powerline.otf`文件安装字体



### 参考

https://gist.github.com/qhh0205/5570934d25a627dd9e9629a8ceeb415c





