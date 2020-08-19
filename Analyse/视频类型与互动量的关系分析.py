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
select '#' text,(avg(da.aweme_statistics_digg_count)+avg(du.aweme_statistics_share_count)+avg(da.aweme_statistics_comment_count)) from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and locate('#', da.aweme_desc) > 0
union all
select '@' text,(avg(da.aweme_statistics_digg_count)+avg(du.aweme_statistics_share_count)+avg(da.aweme_statistics_comment_count)) from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and locate('@', da.aweme_desc) > 0
union all
select '文字' text,(avg(da.aweme_statistics_digg_count)+avg(du.aweme_statistics_share_count)+avg(da.aweme_statistics_comment_count)) from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and locate('@', da.aweme_desc) = 0 and locate('#', da.aweme_desc) = 0
union all
select '无' text,(avg(da.aweme_statistics_digg_count)+avg(du.aweme_statistics_share_count)+avg(da.aweme_statistics_comment_count)) from dsp_aweme da,dsp_user du where da.aweme_id = du.aweme_id and da.aweme_desc = ""
"""
curs.execute(str_sql)
data = curs.fetchall()
# data = (('话题', 26258.138600000002), ('圈人', 22207.3729), ('纯标题', 12589.8624),
#         ('空', 754.4687))
x = [i[0] for i in data]
print(x)
y = [i[1] for i in data]
print(y)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xticks(rotation=25)
plt.xlabel("视频类型", fontproperties="SimHei")
plt.ylabel("互动量平均值（个）", fontproperties="SimHei")
plt.bar(x, y)
plt.show()