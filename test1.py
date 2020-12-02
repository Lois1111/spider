# -*- coding:utf-8 -*-  
# @Time    : 2020/11/6 8:42
# @Author  : lois
# @FileName: test1.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
import re
import pymysql


def create():
    db = pymysql.connect("localhost", "root", "root", "myblog")  # 连接数据库

    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS FUN_TEST")

    sql = """CREATE TABLE FUN_TEST (
            ID INT PRIMARY KEY AUTO_INCREMENT,
            NAME CHAR(20),
            DESCRIBE1 CHAR(255)
            )CHARACTER SET utf8 COLLATE utf8_general_ci"""

    cursor.execute(sql)

    db.close()


def insert(value):
    db = pymysql.connect("localhost", "root", "root", "myblog")

    cursor = db.cursor()
    sql = "INSERT INTO FUN_TEST(NAME,DESCRIBE1) VALUES (%s, %s)"
    try:
        cursor.execute(sql, value)
        db.commit()
        print('插入数据成功')
    except:
        db.rollback()
        print("插入数据失败")
    db.close()


create()  # 创建表

# re匹配需要的数据
pertern = re.compile(
    r'<a.*?><span data-stu-id="52d82-.*?">(.*?)</span>.*?</a>.*?<td><span data-ttu-id="52d82-.*?">(.*?)</span>.*?</td>',
    re.S)
url = 'https://docs.microsoft.com/zh-cn/sql/mdx/mdx-function-reference-mdx?view=sql-server-2017'
res = requests.get(url)
res.encoding = 'utf-8'
print(res.status_code)
soup = BeautifulSoup(res.text, 'html.parser')
data = soup.find_all('tbody')
data = str(data)
item = re.findall(pertern, data)
for i in item:
    print(i)
    insert(i)

