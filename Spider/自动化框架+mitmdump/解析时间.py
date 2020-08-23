import datetime,time
import pymysql
from itertools import chain
import re

conn = pymysql.connect("localhost", "root", "1234567", "test")  # 创建数据库连接
cursor = conn.cursor()  # 获取游标
cursor.execute('select create_time from dy_aweme')
text = cursor.fetchall()
dt = list(chain.from_iterable(text))
#print(dt)

otherStyleTime =''
with open('D:/mmx.txt', 'w') as f:
        for i in dt:
            timeStamp=int(i)
            timeArray = time.localtime(timeStamp)
            otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
           # otherStyleTime=re.compile(r,'otherStyleTime'+/'/n')
            print(otherStyleTime)
            otherStyleTime=re
            f.write(otherStyleTime)
            f.write('\n')


















# timeStamp = 1562556852
# timeArray = time.localtime(timeStamp)
# otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
# print(otherStyleTime)






