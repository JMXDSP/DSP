# -*- coding:utf-8 -*-
import requests
import json
import time
import psycopg2
from psycopg2 import Error
import ast

conn = psycopg2.connect(database='test', user='postgres', password='1234567', host='localhost', port=5432)
curs = conn.cursor()
uid_sql = "select uid from appium_aweme_user group by uid"
curs.execute(uid_sql)
uid = [str(i[0]) for i in curs.fetchall()]
# https://www.amemv.com/web/api/v2/aweme/post/?user_id=78502437069&sec_uid=&count=21&max_cursor=1581591437000&
# "https://www.amemv.com/web/api/v2/aweme/post/?user_id=104255897823&max_cursor={}",
# "https://www.amemv.com/web/api/v2/aweme/post/?user_id=88784318612&max_cursor={}",
# "https://www.amemv.com/web/api/v2/aweme/post/?user_id=96608588706&max_cursor={}"
for i in uid:
    max_cursor = ""
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'cookie': '_ga=GA1.2.1740371928.1589378534;_gid=GA1.2.441578102.1589378534'
    }

    while True:
        url = "https://www.amemv.com/web/api/v2/aweme/post/?user_id={}&count=21&max_cursor={}".format(
            i, max_cursor
        )
        try:
            response = requests.request("GET", url, headers=headers)
        except Exception as e:
            continue

        response_json = json.loads(response.text.encode().decode())
        # print(response.text)
        # print(type(response_json))
        # print(response_json)
        try:
            # &max_cursor=1581591437000
            max_cursor = response_json['max_cursor']
            if response_json['aweme_list']:
                for aweme in response_json['aweme_list']:
                    aweme_desc = aweme['desc']  # 视频名称
                    aweme_id = aweme['aweme_id']  # 视频id
                    aweme_play_video_url = aweme['video']['play_addr']['url_list'][0]  # 视频地址 无码
                    aweme_download_video_url = aweme['video']['download_addr']['url_list'][0]  # 视频地址 有码
                    aweme_video_cover_url = aweme['video']['cover']['url_list'][0]  # 视频封面

                    aweme_author_uid = aweme['author']['uid']  # 作者id
                    aweme_author_nickname = aweme['author']['nickname']  # 作者名称
                    aweme_author_signature = aweme['author']['signature']  # 作者签名
                    aweme_author_favoriting_count = aweme['author']['favoriting_count']
                    aweme_author_total_favorited = aweme['author']['total_favorited']  # 作者全部？
                    aweme_author_short_id = aweme['author']['short_id']  # 作者短id
                    aweme_author_avatar_thumb = aweme['author']['avatar_thumb']['url_list'][0]  # 作者头像100*100
                    aweme_author_avatar_medium = aweme['author']['avatar_medium']['url_list'][0]  # 作者头像720*720
                    aweme_author_avatar_larger = aweme['author']['avatar_larger']['url_list'][0]  # 作者头像1080*1080
                    aweme_author_following_count = aweme['author']['following_count']  # 作者粉丝
                    aweme_author_aweme_count = aweme['author']['aweme_count']  # 作者视频数
                    aweme_author_unique_id = aweme['author']['unique_id']  # 作者抖音id
                    aweme_author_region = aweme['author']['region']  # 作者国家缩写

                    aweme_statistics_comment_count = aweme['statistics']['comment_count']  # 评论数
                    aweme_statistics_digg_count = aweme['statistics']['digg_count']  # 点赞数
                    aweme_statistics_play_count = aweme['statistics']['play_count']  #
                    aweme_statistics_share_count = aweme['statistics']['share_count']  # 分享数
                    aweme_statistics_forward_count = aweme['statistics']['forward_count']  # 转发数

                    str_sql = """
                          insert into appium_aweme_user_list (aweme_id, aweme_desc, aweme_play_video_url, aweme_download_video_url, aweme_video_cover_url,
                          aweme_author_uid, aweme_author_nickname, aweme_author_signature,aweme_author_favoriting_count,
                          aweme_author_total_favorited, aweme_author_short_id, aweme_author_avatar_thumb,
                          aweme_author_avatar_medium,aweme_author_avatar_larger, aweme_author_following_count, 
                          aweme_author_aweme_count,aweme_author_unique_id, aweme_author_region, 
                          aweme_statistics_comment_count,aweme_statistics_digg_count, aweme_statistics_play_count, 
                          aweme_statistics_share_count,aweme_statistics_forward_count) values 
                          ('{}', '{}', '{}', '{}', '{}',
                          '{}', '{}', '{}','{}',
                          '{}', '{}', '{}',
                          '{}','{}', '{}', 
                          '{}','{}', '{}', 
                          '{}','{}', '{}', 
                          '{}','{}')""".format(
                        aweme_id, aweme_desc, aweme_play_video_url, aweme_download_video_url, aweme_video_cover_url,
                        aweme_author_uid, aweme_author_nickname, aweme_author_signature, aweme_author_favoriting_count,
                        aweme_author_total_favorited, aweme_author_short_id, aweme_author_avatar_thumb,
                        aweme_author_avatar_medium, aweme_author_avatar_larger, aweme_author_following_count,
                        aweme_author_aweme_count, aweme_author_unique_id, aweme_author_region,
                        aweme_statistics_comment_count, aweme_statistics_digg_count, aweme_statistics_play_count,
                        aweme_statistics_share_count, aweme_statistics_forward_count
                    )
                    print(aweme_desc)
                    curs.execute(str_sql)
                    conn.commit()
            if not response_json['has_more']:
                print('*' * 33)
                break
        except Error as e:
            print(e)
            conn.rollback()
        except Exception as e:
            print(e)

        # print(response_json['has_more'])

#
# curs.close()
# conn.close()
