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
select * from (
select from_unixtime(da.aweme_create_time, '%H') dt,(avg(da.aweme_statistics_digg_count)+avg(da.aweme_statistics_comment_count)+avg(du.aweme_statistics_share_count)) from dsp_user du,dsp_aweme da where du.aweme_id = da.aweme_id group by from_unixtime(da.aweme_create_time, '%H') order by from_unixtime(da.aweme_create_time, '%H')
) t
"""
curs.execute(str_sql)
data = curs.fetchall()
# data = (('00', 6731.543000000001), ('01', 3255.1482), ('02', 880.3632),
#         ('03', 5137.399), ('04', 840.1227), ('05', 1949.1205),
#         ('06', 3995.3186), ('07', 4004.578), ('08', 5041.4521),
#         ('09', 4533.642000000001), ('10', 8702.1383), ('11', 15239.1572),
#         ('12', 5861.6179), ('13', 9225.1647), ('14', 6645.5921),
#         ('15', 6075.983800000001), ('16', 9701.4598), ('17', 17726.7144),
#         ('18', 14685.1897), ('19', 14813.3219), ('20', 7757.4259999999995),
#         ('21', 5130.2981), ('22', 10693.9217), ('23', 6528.9298))

x = [i[0] for i in data]
print(x)
y = [i[1] for i in data]
print(y)
plt.plot(x, y)
plt.xlabel("时间单位（小时）", fontproperties="SimHei")
plt.ylabel("互动量平均值（个）", fontproperties="SimHei")
plt.grid()
plt.show()