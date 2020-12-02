# -*- coding:utf-8 -*-  
# @Time    : 2020/11/18 18:31
# @Author  : lois
# @FileName: yu.py
# @Software: PyCharm

import requests
import wget
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymysql
import datetime

now_time = datetime.datetime.now().strftime('%F')


browser = webdriver.Chrome()
url = "https://www.freebuf.com"
browser.get(url)
browser.find_element_by_class_name('ant-modal-close').click()
#browser.find_element_by_class_name('ant-modal-close').click()
for i in range(1, 5):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
sopu = BeautifulSoup(browser.page_source, 'html.parser')
result1 = sopu.find_all("span",{"class": "title text-line-1"})
result2 = sopu.find_all("a",{"class": "text text-line-2"})
image = sopu.find_all('img')
Title = ''
Summry = ''
Article_Link = ''
Image_Link = ''
for i in range(len(result1)):
    for j in range(len(image)):
        if result1[i].get_text().strip("[' ''\n']") in str(image[j]):
            try:
                print("文章图片的链接："+image[j].attrs['data-src'])
            except:
                print("Error!!!"+result1[i].get_text())
                continue
            try:
                wget.download(str(image[j].attrs['data-src']),out = "./Image")
                print("下载成功"+image[j].attrs['data-src'])
            except:
                print("\n下载失败"+image[j].attrs['data-src'],end='\n\n\n')
                break
            Title = result1[i].get_text().strip("[' ''\n']")
            Summry = result2[i].get_text().strip("[' ''\n']")
            Image_Link = image[j].attrs['data-src']
            Article_Link = url+result2[i].attrs['href']
            break
    # print("文章的标题："+result1[i].get_text().strip("[' ''\n']")+"\n文章的简介"+result2[i].get_text().strip("[' ''\n']"),end='\n\n\n')