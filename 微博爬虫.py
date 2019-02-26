# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 18:02:56 2019

@author: Administrator
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
from scipy import *
import time

browser = webdriver.Chrome()
#browser = webdriver.Firefox()

"""test"""
browser.get("http://www.baidu.com")
print(browser.page_source)
browser.close() 


def simulate_logging():
    try:
   		 print(u'登陆新浪微博手机端...')
   		 ##打开Firefox浏览器
    	 browser = webdriver.Firefox()
    	 ##给定登陆的网址
        url = 'https://passport.weibo.cn/signin/login'
        browser.get(url)
        time.sleep(3)
        #找到输入用户名的地方，并将用户名里面的内容清空，然后送入你的账号
        username = browser.find_element_by_css_selector('#loginName')
        time.sleep(2)
        username.clear()
        username.send_keys('****')#输入自己的账号
        #找到输入密码的地方，然后送入你的密码
        password = browser.find_element_by_css_selector('#loginPassword')
        time.sleep(2)
        password.send_keys('ll117117')
        #点击登录
        browser.find_element_by_css_selector('#loginAction').click()
        ##这里给个15秒非常重要，因为在点击登录之后，新浪微博会有个九宫格验证码，下图有，通过程序执行的话会有点麻烦（可以参考崔庆才的Python书里面有解决方法），这里就手动
        time.sleep(15)
    except:
        print('########出现Error########')
    finally:
        print('完成登陆!')
        
def spyder_weibo():
	#本文是以GUCCI为例，GUCCI的用户id为‘GUCCI’
	id = 'GUCCI'
    niCheng = id
    #用户的url结构为 url = 'http://weibo.cn/' + id
    url = 'http://weibo.cn/' + id
    browser.get(url)
    time.sleep(3)
    #使用BeautifulSoup解析网页的HTML
    soup = BeautifulSoup(browser.page_source, 'lxml')
    #爬取商户的uid信息
    uid = soup.find('td',attrs={'valign':'top'})
    uid = uid.a['href']
    uid = uid.split('/')[1]
    #爬取最大页码数目
    pageSize = soup.find('div', attrs={'id': 'pagelist'})
    pageSize = pageSize.find('div').getText()
    pageSize = (pageSize.split('/')[1]).split('页')[0]
    #爬取微博数量
    divMessage = soup.find('div',attrs={'class':'tip2'})
    weiBoCount = divMessage.find('span').getText()
    weiBoCount = (weiBoCount.split('[')[1]).replace(']','')
     #爬取关注数量和粉丝数量
    a = divMessage.find_all('a')[:2]
    guanZhuCount = (a[0].getText().split('[')[1]).replace(']','')
    fenSiCount = (a[1].getText().split('[')[1]).replace(']', '')

#通过循环来抓取每一页数据
 for i in range(1, pageSize+1):  # pageSize+1
 		#每一页数据的url结构为 url = 'http://weibo.cn/' + id + ‘?page=’ + i
        url = 'https://weibo.cn/GUCCI?page=' + str(i)
        browser.get(url)
        time.sleep(1)
        #使用BeautifulSoup解析网页的HTML
        soup = BeautifulSoup(browser.page_source, 'lxml')
        body = soup.find('body')
        divss = body.find_all('div', attrs={'class': 'c'})[1:-2]
        for divs in divss:
            # yuanChuang : 0表示转发，1表示原创
            yuanChuang = '1'#初始值为原创，当非原创时，更改此值
            div = divs.find_all('div')
            #这里有三种情况，两种为原创，一种为转发
            if (len(div) == 2):#原创，有图
           		 #爬取微博内容
                content = div[0].find('span', attrs={'class': 'ctt'}).getText()
                aa = div[1].find_all('a')
                for a in aa:
                    text = a.getText()
                    if (('赞' in text) or ('转发' in text) or ('评论' in text)):
                    	#爬取点赞数
                        if ('赞' in text):
                            dianZan = (text.split('[')[1]).replace(']', '')
                        #爬取转发数
                        elif ('转发' in text):
                            zhuanFa = (text.split('[')[1]).replace(']', '')
                         #爬取评论数目
                        elif ('评论' in text):
                            pinLun = (text.split('[')[1]).replace(']', '')    
                 #爬取微博来源和时间   
                span = divs.find('span', attrs={'class': 'ct'}).getText()
                faBuTime = str(span.split('来自')[0])
                laiYuan = span.split('来自')[1]

			#和上面一样
            elif (len(div) == 1):#原创，无图
                content = div[0].find('span', attrs={'class': 'ctt'}).getText()
                aa = div[0].find_all('a')
                for a in aa:
                    text = a.getText()
                    if (('赞' in text) or ('转发' in text) or ('评论' in text)):
                        if ('赞' in text):
                            dianZan = (text.split('[')[1]).replace(']', '')
                        elif ('转发' in text):
                            zhuanFa = (text.split('[')[1]).replace(']', '')
                        elif ('评论' in text):
                            pinLun = (text.split('[')[1]).replace(']', '')
                span = divs.find('span', attrs={'class': 'ct'}).getText()
                faBuTime = str(span.split('来自')[0])
                laiYuan = span.split('来自')[1]
				
			#这里为转发，其他和上面一样
            elif (len(div) == 3):#转发的微博
                yuanChuang = '0'
                content = div[0].find('span', attrs={'class': 'ctt'}).getText()
                aa = div[2].find_all('a')
                for a in aa:
                    text = a.getText()
                    if (('赞' in text) or ('转发' in text) or ('评论' in text)):
                        if ('赞' in text):
                            dianZan = (text.split('[')[1]).replace(']', '')
                        elif ('转发' in text):
                            zhuanFa = (text.split('[')[1]).replace(']', '')
                        elif ('评论' in text):
                            pinLun = (text.split('[')[1]).replace(']', '')
                span = divs.find('span', attrs={'class': 'ct'}).getText()
                faBuTime = str(span.split('来自')[0])
                laiYuan = span.split('来自')[1]
        time.sleep(2)
        print(i)

if __name__ == '__main__':
    
    simulate_logging()
    spyder_weibo()
    
    print("spyder finished!")
