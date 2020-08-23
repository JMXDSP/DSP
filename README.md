# 抖音数据处理
####1数据爬取——Moudle部分
####分4个步骤来完成：
#####（1）根据自动化框架appium和mitmdump插件结合截取请求接口，进行数据保存。通过自动化框架模拟人点击滑动手机的操作（搜索关键字红酒，点击用户，遍历红酒用户下的粉丝信息，进行大批量抓取uid），mitdump来自动保存数据，保存数据字段如uid。
#####（2）爬取卡思数据热门视频，获取视频分享链接和用户界面分享链接。
#####视频分享链接：https://www.iesdouyin.com/share/video/6824055197489335565/?region=CN&mid=0&u_code=0&titleType=title
#####用户分享界面链接：https://www.douyin.com/share/user/690146621009436
#####（3）修改视频分享链接中的参数uid，进行批量爬取
#####（4）修改用户分享界面链接中的参数uid，进行批量爬取
###2 数据分析——Analyse
#####爬取到的数据 ，进行数据库基本的增删改查操作，同时进行数据的清洗。利用python可视化画图，作出数据分析图。
#####用户发布视频的时间特征
取视频发布时间段内的总数，在除以视频总数，最后乘以100%，保留2位小数，算出百分比。creat_time=1490723210时间戳转化为2017-03-29 01:46:50。取出%Y-%m-%d %H:%i:%s中的%H%H:%i
Eg：假设总共有100个视频，6-7时之间的视频有10个，那么6-7时的视频百分比是10%。

#####用户发布视频的时间长度特征
取视频时长duration的数值单位是毫秒，除以100变成秒，在进行60秒为一分钟换算取出时间范围1分钟以内...3-4分钟..5分钟以上，在取出各个范围的视频个数，在除以总视频数，乘以100%，保留2位小数。
Eg：duration=15113ms  duration1=15113ms/100=151.13s,  60s<151.13s<120s。所以duration=15113是1-2分钟内的视频，
假如总视频数是100，1-2分钟视频数是10，那么1-2分钟内视频百分比是10%

#####用户发布视频的类型特征
从aweme_desc标题名称中筛选出带有#，带有@，纯文字，无标题描述四种类型标题，取出4种类型标题视频数量，在饼图种自动显示百分比。
Eg：视频总数100   #20个  @30个   纯文字40个   无标题10
画出饼图 #20%   @30%  纯文字40%  无标题10%
#####视频发布时间与互动量的关系分析
从发布时间create_time 中取%H时间点的转发数量，点赞数量，分享数量/转发数数的平均值，在把这4个平均值加一起看作互动量P。
Eg:creat_time=1490723210时间戳转化为2017-03-29 01:46:50。
取出%Y-%m-%d %H:%i:%s中的%H作为横轴，然后计算这个%H时间点内互动量P的个数作为y轴。
01时共有10个视频，计算出10个视频总共的点赞数100，评论数50，转发数50，分享数100
点赞数z平均值是10，评论数c平均值是5  转发数f平均值是5， 分享数S是10
互动量P=z+c+f+s=30

#####视频类型与互动量的关系分析
从aweme_desc标题名称中筛选出带有#，带有@，纯文字，无标题描述四种类型标题，在分别取出4种类型视频的转发数量，点赞数量，分享数量/转发数数的平均值，在把这4个平均值加一起看作互动量P。
Eg：#视频数是10，计算出10个视频总共的转发数100，点赞数50，分享数50，评论数100
点赞数z平均值是10，评论数c平均值是5  转发数f平均值是5，分享数S是10
互动量P=z+c+f+s=30
#####同理可以得出其他3种类型的互动量
###3 模型建立——Moudle
#####S：接收者（粉丝+刷到的人）
#####I：传播者（点赞的人+评论的人+转发的人）
#####R：免疫者（取消点赞+删除评论+删除转发+浏览后滑走的人）
#####一条信息发出后，会有一部分人群S收到该信息，S中一部分人会以a的概率通过转发，点赞，评论，分享等行为传播信息变成传播者I，S中一部分人浏览信息以d为概率直接划走变成免疫者S。I会在一段时间后以b的概率取消点赞，评论，转发，分享使其变为免疫者R。在取消点赞，评论，转发的过程中也可能会以c的概率变成再次点赞评论转发变成传播者I，直接划走的人还会以e的概率再次接收信息。
 
 
 

