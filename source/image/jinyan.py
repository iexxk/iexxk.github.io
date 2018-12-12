import requests
#正则
import re
#需要爬数据的url
url = 'https://jingyan.baidu.com/user/nucpage/content'
#浏览器访问网站的cookie信息
cookie = {"BDUSS":"ko3Wkl6bkR2em9JNlI1ZnlQdjVTaFVsdGh6YkhjTWVNZS1-QjhSeFkzQkMxVk5iQUFBQUFBJCQAAAAAAAAAAAEAAACeqQVC0uzP69it0NC~1QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEJILFtCSCxbc"}

#提供你所使用的浏览器类型、操作系统及版本、CPU 类型、浏览器渲染引擎、浏览器语言、浏览器插件等信息的标识
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
# 从那个连接来的
referer="https://jingyan.baidu.com/user/nucpage/content"
# 设置请求头
headers = {
"User-Agent": user_agent,
"Referer": referer
}


#requests请求,获取发布数量
published = requests.get(url,cookies=cookie,headers=headers).content
#<li><a class="on" href="/user/nucpage/content">已发布 (505)</a></li>
reg=r'<li><a class="on" href="/user/nucpage/content">已发布 \((.*?)\)</a></li>'
publishedNum=re.search(reg,published.decode(),re.I|re.M|re.S).group(1)
#group(0) 匹配的串，group(1) 匹配的串中第一个括号
print(publishedNum)
#算页数,实际篇数-1
pages=int((int(publishedNum)-1)/20)+1
print(pages)
#把内容保存为文件,'w'是写，'wb'是写入byte
with open("jingyan.md", 'w') as f:
	for page in range(0,pages):
		pn=page*20
		print(pn)

		# url参数
		# https://jingyan.baidu.com/user/nucpage/content?tab=exp&expType=published&pn=20
		params = {
		'tab': 'exp',
		'expType': 'published',
		'pn': pn
		}

		#requests请求，获取登录网站页面的内容
		html = requests.get(url,cookies=cookie,headers=headers,params=params).content

		#过滤
		reg=r'<a class="f14" target="_blank" title=(.*?)>'

		#re.I 使匹配对大小写不敏感 
		#re.M 多行匹配，影响 ^ 和 $ 
		#re.S 使 . 匹配包括换行在内的所有字符 
		#这个是查找此字符串中所有符合条件的内容并返回一个列表
		list=re.findall(reg,html.decode(),re.I|re.M|re.S)
		
		for item in list:
			item=item.replace('" href="','](https://jingyan.baidu.com')
			item=item.replace('.html"','.html)')
			item=item.replace('"','[')
			f.write("%s\n" % item)
f.close()