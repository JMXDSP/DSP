import pymysql

import matplotlib.pyplot as plt  #约定俗成的写法plt
from matplotlib.font_manager import FontProperties
import matplotlib
#首先定义两个函数（正弦&余弦）
import numpy as np

conn = pymysql.connect("localhost", "root", "1234567",
                       "wangan116")  # 创建数据库连接
curs = conn.cursor()

str_sql = """
select t.dt, round((t.number/t.total)*100,2) y from (
select * from (
select from_unixtime(da.aweme_create_time, '%H') dt,count(1) number from dsp_user du,dsp_aweme da where du.aweme_id = da.aweme_id group by from_unixtime(da.aweme_create_time, '%H') order by from_unixtime(da.aweme_create_time, '%H')
) t1 inner join (
select count(1) total from dsp_user du,dsp_aweme da where du.aweme_id = da.aweme_id
) t2 on 1=1
) t
"""
curs.execute(str_sql)
data = curs.fetchall()
# data = (('00', 1.59), ('01', 0.78), ('02', 0.47), ('03', 0.34), ('04', 0.38),
#         ('05', 0.79), ('06', 1.84), ('07', 3.00), ('08', 3.68), ('09', 4.62),
#         ('10', 5.45), ('11', 6.42), ('12', 6.01), ('13', 5.13), ('14', 4.86),
#         ('15', 5.00), ('16', 5.64), ('17', 7.38), ('18', 7.73), ('19', 7.36),
#         ('20', 7.03), ('21', 6.36), ('22', 4.90), ('23', 3.14))

x = [i[0] for i in data]
print(x)
y = [i[1] for i in data]
print(y)
plt.plot(x, y)
plt.title("抖音日分布图", fontproperties="SimHei")
plt.xlabel("时间单位（小时）", fontproperties="SimHei")
plt.ylabel("百分比（%）", fontproperties="SimHei")
plt.grid()
plt.show()