# -*- coding:utf-8 -*-  
# @Time    : 2020/11/9 14:10
# @Author  : lois
# @FileName: all.py
# @Software: PyCharm

import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pymysql

# 打开chrome浏览器（需提前安装好chromedriver）
browser = webdriver.Chrome()
print("正在打开网页...")
browser.get("https://www.freebuf.com/")

soup = BeautifulSoup(browser.page_source,'lxml')

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
    }


def create():
    db = pymysql.connect("localhost", "root", "root", "myblog")  # 连接数据库

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS ALL_INFO")

    sql = """CREATE TABLE ALL_INFO (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            TITLE  CHAR(255),
            CONTENT VARCHAR(10240),
            PATH CHAR(255),
            URL VARCHAR(265) 
            )CHARACTER SET utf8 COLLATE utf8_general_ci"""

    cursor.execute(sql)

    db.close()

def insert(value):
    db = pymysql.connect("localhost", "root", "root", "myblog")

    cursor = db.cursor()
    sql = "INSERT INTO ALL_INFO(TITLE,PATH,CONTENT,URL) VALUES (%s, %s, %s, %s)"
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
    path = 'F:\pics'
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print('创建成功！')
    else:
        print('已经存在！')
    return path

def get_link():#在首页获取文章的链接
    links = []
    for item in soup.find_all(class_="article-item"):
        link = ((item.find(class_="item-right")).find('a')).get('href')
        url = 'https://www.freebuf.com//'+link
        links.append(url)
    return links


def info():
    links =  get_link()
    path = mkdir()
    for link in links:
        page = requests.get(link, headers=headers)
        html = BeautifulSoup(page.text, "html.parser")
        web_title = (html.find('span', class_="title-span")).get_text()
        web_text = html.find('div', class_="content-detail")
        contents = (web_text.find_all('p'))
        datas = ''
        for item in contents:
            data = item.get_text()
            datas += data
        all = (web_title,path,datas,link)
        insert(all)

def get_imgs():
    a = 1
    path = mkdir()
    links = get_link()
    for link in links:
        page = requests.get(link, headers=headers)
        html = BeautifulSoup(page.text, "html.parser")
        web_text = html.find('div', class_="content-detail")
        imgs = (web_text.find_all('img'))
        for i in imgs:
            img = i.get('src')
            try:
                pic = requests.get(img)
            except requests.exceptions.ConnectionError:
                print('图片无法下载')
                continue
            print('\r当前完成：已完成{}个'.format(a), end='')
            with open(path+'\pic_' + str(a) + ".jpg", 'wb') as f:
                f.write(pic.content)
            a = a+1



if __name__ == '__main__':
    create()
    info()
    get_imgs()


