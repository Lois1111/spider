# -*- coding:utf-8 -*-  
# @Time    : 2020/11/6 12:53
# @Author  : lois
# @FileName: pic.py
# @Software: PyCharm


import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pymysql

# 打开chrome浏览器（需提前安装好chromedriver）
browser = webdriver.Chrome()
browser.maximize_window()
print("正在打开网页...")
browser.get("https://www.freebuf.com/")

# soup = BeautifulSoup(browser.page_source,'lxml')
soup = BeautifulSoup(browser.page_source,'lxml')

def create():
    db = pymysql.connect("localhost", "root", "root", "myblog")  # 连接数据库

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS PIC")

    sql = """CREATE TABLE PIC (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            PATH  CHAR(255),
            URL CHAR(255)  
            )CHARACTER SET utf8 COLLATE utf8_general_ci"""

    cursor.execute(sql)

    db.close()

def insert(value):
    db = pymysql.connect("localhost", "root", "root", "myblog")

    cursor = db.cursor()
    sql = "INSERT INTO PIC(PATH,URL) VALUES (%s, %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入数据成功')
    except Exception as e: #打印错误信息
        print('插入数据失败', e)
        db.rollback()
    finally:
        db.close()

def mkdir():
    path = 'F:/pic'
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print('创建成功！')
    else:
        print('已经存在！')
    return path

def save_to_file(path,num,data):
    filepath = path +'//{}.jpg'.format(num)
    try:
        r = requests.get(data)
        r.raise_for_status()
        with open(filepath,'wb') as f:
            f.write(r.content)
    except requests.exceptions.ConnectionError:
        print("下载失败！")

def get_imag():
    findPic = re.compile(r'<img .*? data-src="(.*?)"')
    path = mkdir()
    a=1
    for item in soup.find('div','article-list'):
        item =str(item)
        links = (re.findall(findPic, item))
        print(links)
        # length = len(links)
        # if(length > 0):
        #     links = (re.findall(findPic, item))[0].strip()
        #     save_to_file(path,a,links)
        #     data = (path,links)
        #     insert(data)
        # print('\r当前完成：已完成{}个'.format(a))
        # a+=1

if __name__ == '__main__':
    # create()
    get_imag()






