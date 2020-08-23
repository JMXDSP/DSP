import requests
import pymysql
import json
requests.packages.urllib3.disable_warnings()

conn = pymysql.connect('127.0.0.1', 'root', '1234567', 'test')
cur = conn.cursor()

headers = {
    "Authorization":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2FwaS5kYXRhLmNhYXNkYXRhLmNvbS9jaGVja0xvZ2luIiwiaWF0IjoxNTg5MTE2MzkxLCJleHAiOjE1OTE3MDgzOTEsIm5iZiI6MTU4OTExNjM5MSwianRpIjoib1JwQ2ZGZTBaZnBTNUpNMCIsInN1YiI6IjE4MzY1MCIsInNvdXJjZSI6ImRvdXlpbl9jYWFzZGF0YSIsIkxvZ2luVG9rZW4iOiJaOU5qaUxpSDh6NlFaIn0.3aXxo_Zuk8PpmeQ7KDybwt5p41j83ljxudzX7aJ13dY",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    "sign":"a5941bd864d0f8eeaa55231cc5506808", # 这个不能错 错了就会报签名错误  每次需要修改一下
    "salt":"1590673227826",  # 上面的那个是根据这个时间戳生成的 所以两个要对应上
}

# tag={
#     '0':'全部','669':'小姐姐','670':'小哥哥','671':'明星','672':'萌娃','673':'民间艺人','674':'搞笑','700':'剧情',
#     '675':'宠物','676':'美妆','677':'美食','678':'旅游','679':'游戏','680':'二次元','681':'音乐','682':'舞蹈',
#     '683':'影视','684':'母婴','685':'生活百科','686':'运动健身','688':'科技','689':'财经','690':'军事','691':'文化',
#     '692':'教育','693':'创意','694':'摄影','695':'种草开箱','696':'手工手绘','697':'生活资讯','701':'Vlog','699':'正能量',
# }

# for t in tag.keys():
for i in range(1,999):
    # https://api.data.caasdata.com/video-search?platform_id=998&order=up_count&time=1&page=1&tag_id=0&v_flag=0&topic_flag=0
    # https://api.data.caasdata.com/video-search?platform_id=998&order=up_count&time=1&page=1&tag_id=0&v_flag=0&topic_flag=0
    url = "https://api.data.caasdata.com/video-search?platform_id=998&order=up_count&time=1&page=%s&tag_id=0&v_flag=0&topic_flag=0" % i
    response = requests.request("GET", url, headers=headers, verify=False)
    try:
        print(json.loads(response.text))
        data = json.loads(response.text).get('data')
        if data:
            for l in data:
                print(l['id'], l['title'])
                video_id=l['video_id']
                desc=l['title']
                url=l['url']
                pic_url=l['pic_url']
                publish_time=l['publish_time']
                play_count=l['play_count']
                comment_count=l['comment_count']
                up_count=l['up_count']
                share_count=l['share_count']
                title=l['channel']['data']['title']
                signature=l['channel']['data']['intro']
                yh_url=l['channel']['data']['url']
                yh_picture=l['channel']['data']['pic_url']
                platform_approve=l['channel']['data']['platform_approve']
                uid=l['channel']['data']['extra_id']
                video_count=l['channel']['data']['video_count']
                fan_count=l['channel']['data']['fan_count']
                birthday=l['channel']['data']['birthday']
                gender=l['channel']['data']['gender']
                constellation=l['channel']['data']['constellation']
                area=l['channel']['data'].get('area') if l['channel']['data'].get('area') else ''
                province = l['channel']['data']['province']
                country = l['channel']['data']['country']

                str_sql = "insert into kasi_remen_shipin(video_id,str_desc,url,pic_url,publish_time,play_count,comment_count,up_count,share_count,title,signature,yh_url,yh_picture,platform_approve,uid,video_count,fan_count,birthday,gender,constellation,area, province,country) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}', '{}')".format(
                    video_id, desc, url, pic_url, publish_time, play_count, comment_count, up_count, share_count, title,
                    signature, yh_url, yh_picture, platform_approve, uid, video_count, fan_count, birthday, gender,
                    constellation, area, province, country )
                print(str_sql)
                cur.execute(str_sql)
                conn.commit()
        else:
            print(i)
            break
    except Exception as e:
        print(e)
        print(i)
        break
# a = {'679': '游戏', '680': '二次元'}
# a.keys()
# a.values()
# https://api.data.caasdata.com/video-search?platform_id=998&order=up_count&time=1&page=1&tag_id=680&v_flag=0&topic_flag=0
# https://api.data.caasdata.com/video-search?platform_id=998&order=up_count&time=1&page=1&tag_id=679&v_flag=0&topic_flag=0
#https://api.data.caasdata.com/video-search?platform_id=998&order=up_count&time=1&page=1&tag_id=0&v_flag=0&topic_flag=0