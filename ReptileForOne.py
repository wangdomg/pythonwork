#!/usr/bin/python
#-*- coding:UTF-8 -*-

#这里用到了requests模块和beautifulsoup4模块，在使用之前先要安装，在ubuntu下安装的命令：
#安装requests：pip install requests
#安装beautifulsoup：pip install beautifulsoup4
#其中pip是python的包管理器，需要预先安装

import requests
import bs4
import urllib
import sys

def get_url(num):
	return root_url + '/one/' + str(num)

def get_urls(num):
	urls = map(get_url, range(100, 100+num)) #map函数有两个参数，一个是函数，一个是序列。将序列的每个值，作为参数传递给函数，返回一个列表。
	return urls 

def get_data(urls):
	dataList = {}
	count = 0
	sentenceFile = open("../OneSentence.txt", "a") #以追加模式打开一个文件
	for url in urls:
		response = requests.get(url) #这时就能从response.text中获得网页的HTML了
		if response.status_code != 200:
			return {'noValue':'noValue'}
		soup = bs4.BeautifulSoup(response.text, 'html.parser')
		dataList['index'] = soup.title.string[4:8]
		for meta in soup.select('meta'):
			if meta.get('name') == 'description':
				dataList['content'] = meta.get('content')
		sentenceFile.write(dataList['content'] + '\n') #将句子写入文件末尾并加上换行符
		
		#下面是获取页面中的图片的src并下载到本地的代码
		#dataList['imgUrl'] = soup.find_all('img')[1]['src']
		#filename = "img" + str(count) + ".jpg"
		#urllib.urlretrieve(dataList["imgUrl"], filename)
		#count = count + 1
reload(sys)
sys.setdefaultencoding('utf-8') #更改系统默认的编码方式，这样才能正常地向文件中写入中文
root_url = "http://wufazhuce.com"
List = get_urls(10) #得到是个网页的url
get_data(List)
			
