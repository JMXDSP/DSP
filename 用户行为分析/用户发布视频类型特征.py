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
select '#' text,count(1) con from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and locate('#', da.aweme_desc) > 0
union all
select '@' text,count(1) con from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and locate('@', da.aweme_desc) > 0
union all
select '文字' text,count(1) con from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and locate('@', da.aweme_desc) = 0 and locate('#', da.aweme_desc) = 0
union all
select '无' text,count(1) con from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and da.aweme_desc = ""
"""
curs.execute(str_sql)
data = curs.fetchall()
# data = (('#', 206), ('文字', 30859), ('@', 82), ('无', 11698))
x = [i[0] for i in data]
print(x)
y = [i[1] for i in data]
print(y)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xticks(rotation=25)
plt.title("用户发布视频类型", fontproperties="SimHei")
# plt.xlabel("视频类型", fontproperties="SimHei")
# plt.ylabel("点赞数（平均/条）", fontproperties="SimHei")
plt.pie(y, labels=x, autopct='%1.1f%%')
plt.show()