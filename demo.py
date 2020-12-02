# -*- coding:utf-8 -*-  
# @Time    : 2020/11/6 8:12
# @Author  : lois
# @FileName: demo.py
# @Software: PyCharm

import pymysql

conn = pymysql.connect('localhost','root','root','myblog',charset = 'utf8')

cursor = conn.cursor()

sql = 'insert into qiushi(author,funny_num,comment_num,content) values(%s,%s,%s,%s) '
# (2)准备数据
data = ('nancy', '30', '100', '太好笑了')
# (3)操作
try:
    cursor.execute(sql, data)
    conn.commit()
except Exception as e:
    print('插入数据失败', e)
    conn.rollback()  # 回滚

# 关闭游标
cursor.close()
# 关闭连接
conn.close()
