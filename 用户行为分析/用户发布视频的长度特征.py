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
select t1.x,round(t1.y/t2.total_y*100,2) from (
select case when aweme_video_duration/100 <= 60 then '一分钟以内' when aweme_video_duration/100 > 60 and aweme_video_duration/100 <= 120 then '一分钟到两分钟' when aweme_video_duration/100 > 120 and aweme_video_duration/100 <= 180 then '两分钟到三分钟' when aweme_video_duration/100 > 180 and aweme_video_duration/100 <= 240 then '三分钟到四分钟' when aweme_video_duration/100 > 240 and aweme_video_duration/100 <= 300 then '四分钟到五分钟' else '五分钟以上' end x, count(1) y from dsp_user du, dsp_aweme da where du.aweme_id = da.aweme_id group by case when aweme_video_duration/100 <= 60 then '一分钟以内' when aweme_video_duration/100 > 60 and aweme_video_duration/100 <= 120 then '一分钟到两分钟' when aweme_video_duration/100 > 120 and aweme_video_duration/100 <= 180 then '两分钟到三分钟' when aweme_video_duration/100 > 180 and aweme_video_duration/100 <= 240 then '三分钟到四分钟' when aweme_video_duration/100 > 240 and aweme_video_duration/100 <= 300 then '四分钟到五分钟' else '五分钟以上' end
) t1 left join (
select count(1) total_y from dsp_user du, dsp_aweme da where du.aweme_id = da.aweme_id
) t2 on 1=1
order by case when t1.x = '一分钟以内' then 1 when t1.x = '一分钟到两分钟' then 2 when t1.x = '两分钟到三分钟' then 3 when t1.x = '三分钟到四分钟' then 4 when t1.x = '四分钟到五分钟' then 5 when t1.x = '五分钟以上' then 6 end asc
"""
curs.execute(str_sql)
data = curs.fetchall()

# data = (('一分钟以内', 33221), ('一分钟到两分钟', 586971), ('两分钟到三分钟', 1169339),
#         ('三分钟到四分钟', 271620), ('四分钟到五分钟', 188273), ('五分钟以上', 834632))
x = [i[0] for i in data]



print(x)
y = [i[1] for i in data]
print(y)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.xticks(rotation=25)
plt.bar(x, y)
# plt.title("发布视频的长度特征", fontproperties="SimHei")
# plt.xlabel("时间", fontproperties="SimHei")
plt.ylabel("百分比%", fontproperties="SimHei")
plt.show()