#!usr/bin/python
#-*- coding:UTF-8-*-

import requests
import bs4
import urllib, urllib2
import re
import sys

root_url = "https://book.douban.com/"

def get_url(after):
	return root_url + '/tag/' + after

def get_urls(taglists):
	return map(get_url, taglists)

def get_data():
	taglists = ['小说', '随笔', '散文', '日本文学', '童话', '诗歌', '名著', '港台']
	urls = get_urls(taglists)
	file_object = open('../dbread.txt', 'a')
	for i in range(0, len(urls)):
		number = 0
		while(True):
			if number == 0: #说明是该类别的第一个页面，它与后续页面的url格式是不同的
				request = urllib2.Requests(urls[i])
			else: #说明是该类别的后续页面
				request = urllib2.Requests(urls[i] + '?start=' + number + '&type=T')
			response = urllib2.urlopen(request)
			response = response.read()
			file_object.write(taglists[i] + '\n')
			soup = bs4.BeautifulSoup(response.text, 'html-parser')
			tags_a = soup.find_all('a', href = re.compile(r'https://book.douban.com/subject/'))
            
            #判断列表是否为空，实际上是判断是否已经爬完每一种类的每一个页面
			if not tags_a:
				file_object.write('\n\n') #爬完了一个种类，与下一个种类之间保持间隔
				break
	       
			#遍历该类别的每一个页面
			for a in tags_a:
				#a节点的父节点的第一个兄弟节点包含了对这本书的描述，a节点的父节点的第二个兄弟节点的子节点包含了对这本书的评分
				book_name = a.get('title') #书名
				parent = a.parent #这是当前节点的父节点
				firstbrother = parent.next_sibling #这是父节点的第一个兄弟节点，包含了对这本书的描述
				secondbrother = parent.next_sibling.next_sibling #这是父节点的第二个兄弟节点，它的第二个子节点包含了对这本书的评分
				book_description = firstbrother.string #书的描述
				book_rating = secondbrother.contents[1] #书的评分
				file_object.write(book_name + ' ' + book_description + ' ' + book_rating + '\n')

			number += 20 #用于构建下一个页面的url

if __name__ == '__main__':
	''' 模块是对象，并且所有的模块都有一个内置属性 __name__。一个模块的 __name__ 的值取决于您如何应用模块。如果 import 一个模块，那么模块__name__ 的值通常为模块文件名，不带路径或者文件扩展名。但是您也可以像一个标准的程序样直接运行模块，在这 种情况下, __name__ 的值将是一个特别缺省"__main__"。'''
	get_data()
		

