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

result1 = soup.find_all("span",{"class":"title text-line-1"})
result2 = soup.find_all("a",{"class":"text text-line-2"})
image = sopu.find_all('img')
Title = ''
Summry = ''
Article_Link = ''
Image_Link = ''
for i in range(len(result1)):
    for j in range(len(image)):
        if (result1[i].get_text().strip("[' ''\n']") in str(image[j])):
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
            sql = "insert into Article (Title, Summry, Article_Link, Image_Link,Data) VALUES(\'{0}\',\'{1}\',\'{2}\',\'{3}\',\'{4}\')".format(Title, Summry, Article_Link, Image_Link, now_time)
            print(sql)
            sql_cursor.execute(sql)
            sql_cursor.rowcount
            conn.commit()
            break
    print("文章的标题："+result1[i].get_text().strip("[' ''\n']")+"\n文章的简介"+result2[i].get_text().strip("[' ''\n']"),end='\n\n\n')


if __name__ == '__main__':
    # create()
    info()









