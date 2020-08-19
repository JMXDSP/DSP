# -*- coding:utf-8 -*-
import requests
import json
import time
import pymysql
import ast
from pymysql import Error
conn = pymysql.connect("localhost", "root", "1234567",
                       "wangan116")  # 创建数据库连接
curs = conn.cursor()

str_sql = "select aweme_id from dy_aweme_copy1 group by aweme_id"
curs.execute(str_sql)
url = [i[0] for i in curs.fetchall()]
# print(url)
for i in url:
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'cookie': '_ga=GA1.2.1740371928.1589378534;_gid=GA1.2.441578102.1589378534'
    }

    url = "https://www.amemv.com/web/api/v2/aweme/iteminfo/?item_ids={}".format(
        i
    )
    # print(url)

    try:
        response = requests.request("GET", url, headers=headers)

        response_json = json.loads(response.text.encode().decode())
        if response_json['item_list']:
            for aweme in response_json['item_list']:
                aweme_id = aweme['aweme_id']  # 视频id
                aweme_desc = aweme['desc']  # 视频名称
                aweme_type = aweme['aweme_type']  # 视频类型
                aweme_duration = aweme['duration']  # 视频时长
                for extra in aweme['text_extra']:  # 视频标签
                    extra_hashtag_name = extra['hashtag_name']  # 标签名称
                    extra_hashtag_id = extra['hashtag_id']  # 标签id
                    extra_user_id = extra.get('user_id', '')  # 标签用户？
                    str_sql = """
                    insert into hongjiu_extra(aweme_id,extra_hashtag_name, extra_hashtag_id, extra_user_id) values (
                        "{}","{}", "{}", "{}"
                    )
                    """.format(aweme_id,extra_hashtag_name, extra_hashtag_id, extra_user_id)
                    curs.execute(str_sql)
                    conn.commit()
                aweme_author_user_id = aweme['author_user_id']  # 视频发布者id
                if aweme.get('author',None):
                    aweme_author_uid = aweme['author']['uid']  # 视频发布者id
                    aweme_author_unique_id = aweme['author']['unique_id']  # 视频发布者抖音号
                    aweme_author_nickname = aweme['author']['nickname']  # 视频发布者名称
                    aweme_author_signature = aweme['author']['signature']  # 视频发布者签名
                    aweme_author_short_id = aweme['author']['short_id']
                    aweme_author_avatar_thumb = aweme['author']['avatar_thumb']['url_list'][0]  # 视频发布者头像 100*100
                    aweme_author_avatar_medium = aweme['author']['avatar_medium']['url_list'][0]  # 视频发布者头像 720*720
                    aweme_author_avatar_larger = aweme['author']['avatar_larger']['url_list'][0]  # 视频发布者头像 1080*1080
                else:
                    aweme_author_uid = ""  # 视频发布者id
                    aweme_author_unique_id = ""  # 视频发布者抖音号
                    aweme_author_nickname = ""  # 视频发布者名称
                    aweme_author_signature = ""  # 视频发布者签名
                    aweme_author_short_id = ""
                    aweme_author_avatar_thumb = ""  # 视频发布者头像 100*100
                    aweme_author_avatar_medium = ""  # 视频发布者头像 720*720
                    aweme_author_avatar_larger = ""

                if aweme.get('music',None):
                    aweme_music_title = aweme['music']['title']  # 音乐名称
                    aweme_music_author = aweme['music']['author']  # 音乐发布者
                    if aweme['music']['play_url']['url_list']:
                        aweme_music_url = aweme['music']['play_url']['url_list'][0]  # 音乐地址
                    else:
                        aweme_music_url = aweme['music']['play_url']['url_list']
                    aweme_music_id = aweme['music']['id']  # 音乐id
                    aweme_music_mid = aweme['music']['mid']
                    aweme_music_duration = aweme['music']['duration']  # 音乐时长
                    if aweme['music']['cover_thumb']['url_list']:
                        aweme_music_cover_thumb = aweme['music']['cover_thumb']['url_list'][0]  # 音乐发布者头像 100*100
                        aweme_music_cover_large = aweme['music']['cover_large']['url_list'][0]  # 音乐发布者头像 1080*1080
                        aweme_music_cover_medium = aweme['music']['cover_medium']['url_list'][0]  # 音乐发布者头像 720*720
                        aweme_music_cover_hd = aweme['music']['cover_hd']['url_list'][0]  # 音乐发布者头像 1080*1080
                    else:
                        aweme_music_cover_thumb = ""  # 音乐发布者头像 100*100
                        aweme_music_cover_large = ""  # 音乐发布者头像 1080*1080
                        aweme_music_cover_medium = ""  # 音乐发布者头像 720*720
                        aweme_music_cover_hd = ""  # 音乐发布者头像 1080*1080
                    aweme_music_status = aweme['music']['status']  # 音乐状态
                else:
                    aweme_music_title = ""  # 音乐名称
                    aweme_music_author = ""  # 音乐发布者
                    aweme_music_url = ""  # 音乐地址
                    aweme_music_id = ""  # 音乐id
                    aweme_music_mid = ""
                    aweme_music_duration = ""  # 音乐时长
                    aweme_music_cover_thumb = ""  # 音乐发布者头像 100*100
                    aweme_music_cover_large = ""  # 音乐发布者头像 1080*1080
                    aweme_music_cover_medium = ""  # 音乐发布者头像 720*720
                    aweme_music_cover_hd = ""  # 音乐发布者头像 1080*1080
                    aweme_music_status = ""  # 音乐状态
                if aweme.get('video',None):
                    aweme_video_duration = aweme['video']['duration']  # 视频时长
                    if aweme['video']['play_addr']['url_list']:
                        aweme_video_play_addr_url = aweme['video']['play_addr']['url_list'][0]  # 视频 有码
                    else:
                        aweme_video_play_addr_url = ""
                    aweme_video_cover = aweme['video']['cover']['url_list'][0]  # 视频图片
                    if aweme['video']['dynamic_cover']['url_list']:
                        aweme_video_dynamic_cover = aweme['video']['dynamic_cover']['url_list'][0]  # 视频动态图片
                    else:
                        aweme_video_dynamic_cover = ""  # 视频动态图片
                    aweme_video_origin_cover = aweme['video']['origin_cover']['url_list'][0]  # 视频图片原图
                    aweme_video_vid = aweme['video']['vid']
                else:
                    aweme_video_duration = ""  # 视频时长
                    aweme_video_play_addr_url = ""  # 视频 有码
                    aweme_video_cover = ""  # 视频图片
                    aweme_video_dynamic_cover = ""  # 视频动态图片
                    aweme_video_origin_cover = ""  # 视频图片原图
                    aweme_video_vid = ""

                aweme_share_url = aweme['share_url']  # 视频分享地址

                if aweme.get('statistics',None):
                    aweme_statistics_comment_count = aweme['statistics']['comment_count']  # 视频评论数
                    aweme_statistics_digg_count = aweme['statistics']['digg_count']  # 视频点赞数
                else:
                    aweme_statistics_comment_count = ""  # 视频评论数
                    aweme_statistics_digg_count = ""

                aweme_create_time = aweme['create_time']  #

                str_sql = """
                insert into hongjiu_aweme(aweme_id, aweme_desc, aweme_type, aweme_duration, aweme_author_user_id, aweme_author_uid,
                 aweme_author_unique_id, aweme_author_nickname,
                 aweme_author_signature, aweme_author_short_id, aweme_author_avatar_thumb, aweme_author_avatar_medium,
                 aweme_author_avatar_larger, aweme_music_title, aweme_music_author,
                 aweme_music_url, aweme_music_id, aweme_music_mid, aweme_music_duration,aweme_music_cover_thumb,
                 aweme_music_cover_large,aweme_music_cover_medium,aweme_music_cover_hd,aweme_music_status,
                 aweme_video_duration,aweme_video_play_addr_url,aweme_video_cover,aweme_video_dynamic_cover,aweme_video_origin_cover,
                 aweme_video_vid,aweme_share_url,aweme_statistics_comment_count,aweme_statistics_digg_count,
                 aweme_create_time) values (
                 "{}", "{}", "{}", "{}", "{}", "{}",
                 "{}", "{}", 
                 "{}", "{}", "{}", "{}",
                 "{}", "{}", "{}",
                 "{}", "{}", "{}", "{}","{}",
                 "{}","{}","{}","{}",
                 "{}","{}","{}","{}","{}",
                 "{}","{}","{}","{}",
                 "{}")
                """.format(
                    aweme_id, aweme_desc.replace("'", "''"), aweme_type, aweme_duration, aweme_author_user_id, aweme_author_uid,
                    aweme_author_unique_id, aweme_author_nickname.replace("'", "''"),
                    aweme_author_signature, aweme_author_short_id, aweme_author_avatar_thumb,
                    aweme_author_avatar_medium,
                    aweme_author_avatar_larger, aweme_music_title.replace("'", "''"), aweme_music_author,
                    aweme_music_url, aweme_music_id, aweme_music_mid, aweme_music_duration, aweme_music_cover_thumb,
                    aweme_music_cover_large, aweme_music_cover_medium, aweme_music_cover_hd, aweme_music_status,
                    aweme_video_duration, aweme_video_play_addr_url, aweme_video_cover, aweme_video_dynamic_cover,
                    aweme_video_origin_cover,
                    aweme_video_vid, aweme_share_url, aweme_statistics_comment_count, aweme_statistics_digg_count,
                    aweme_create_time
                )
                print(aweme_id, aweme_desc)
                # str_sql = "insert into test(str_desc, aweme_id) values ("{}", "{}")".format(
                #     desc, aweme_id
                # )
                # print(str_sql)
                str_sql = str_sql.replace("'", "\'")
                curs.execute(str_sql)
                conn.commit()
    except Error as e:
        print(e)
        conn.rollback()
    except Exception as e:
        print(e)
