# -*- coding:utf-8 -*-  
# @Time    : 2020/11/7 8:49
# @Author  : lois
# @FileName: title.py
# @Software: PyCharm
import re

from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql

# 打开chrome浏览器（需提前安装好chromedriver）
browser = webdriver.Chrome()
browser.maximize_window()
print("正在打开网页...")
browser.get("https://www.freebuf.com/")
soup = BeautifulSoup(browser.page_source,'lxml')

def create():
    db = pymysql.connect("localhost", "root", "root", "myblog")  # 连接数据库

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS INFO")

    sql = """CREATE TABLE INFO (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            TITLE  CHAR(255),
            SKETCH CHAR(255),
            lINK CHAR(255) 
            )CHARACTER SET utf8 COLLATE utf8_general_ci"""

    cursor.execute(sql)

    db.close()

def insert(value):
    db = pymysql.connect("localhost", "root", "root", "myblog")

    cursor = db.cursor()
    sql = "INSERT INTO INFO(TITLE,SKETCH,lINK) VALUES (%s, %s,  %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入数据成功')
    except Exception as e: #打印错误信息
        print('插入数据失败', e)
        db.rollback()
    finally:
        db.close()


def info():
    for item in soup.find_all(class_="article-item"):
        title = item.find(class_="title text-line-1").get_text()
        link = 'https://www.freebuf.com'+((item.find(class_="item-right")).find('a')).get('href')
        # print('https://www.freebuf.com'+link)
        content = (((item.find(class_="item-right")).find('a').get_text()).replace('\n','')).strip()
        print(content)
        data = (title,content,link)
        # print(data)
        # insert(data)

def get_imag():
    findPic = re.compile(r'<img .*? data-src="(.*?)"')
    for item in soup.find('div','article-list'):
        # print(item)
        item =str(item)
        links = (re.findall(findPic, item))


if __name__ == '__main__':
    # create()
    info()









