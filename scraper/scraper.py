from weibo_scraper import get_weibo_tweets_by_name
import datetime,re
from .engine import download_images,download_videos,parse_blog
import pandas as pd
import os

def merge_csv(from_account,file_list,start_date,end_date):
    csv_path = r'./csv_log/'  # 要拼接的文件夹及其完整路径，注意不要包含中文

    # 将该文件夹下的所有文件名存入一个列表
    merge_file_name=from_account+"_"+start_date+"_"+end_date+".csv"
    if file_list:
        df = pd.read_csv(file_list[0])  # 编码默认UTF-8，若乱码自行更改

    # 将读取的第一个CSV文件写入合并后的文件保存
        os.remove(file_list[0])
        df.to_csv(csv_path + '/' + merge_file_name, encoding="utf_8_sig", index=False)

    # 循环遍历列表中各个CSV文件名，并追加到合并后的文件
        for i in range(1, len(file_list)):
            df = pd.read_csv(file_list[i])
            df.to_csv(csv_path + '/' + merge_file_name, encoding="utf_8_sig", index=False, header=False, mode='a+')
            os.remove(file_list[i])


def scrap_interval(
    account_name,
    start_date,
    end_date,
    save_images=False,
    save_videos=False,
):
    csv_name=account_name+"_"+start_date.strftime("%Y-%m-%d")+"_"+end_date.strftime("%Y-%m-%d")+".csv"
    data=[]
    print("\r[INFO] 开始查询...",end="")
    #start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d')# + datetime.timedelta(days=interval)
    #end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d')

    if end_date<start_date:
        return
    print("\r[INFO] 搜索时间段：%s-%s" %(start_date.strftime("%Y-%m-%d"),end_date.strftime("%Y-%m-%d")), end="")
    for tweet in get_weibo_tweets_by_name(name=account_name, pages=None):
        current_date,blog_content=parse_blog(tweet)
        if current_date>=start_date and current_date<=end_date:
            data.append(blog_content)
        elif 'title' in tweet['mblog'].keys() and '置顶' in tweet['mblog']['title']['text']:
            continue
        elif current_date<=start_date:
            break

    data_df = pd.DataFrame(data, columns=['UserName', 'UserID','Timestamp', 'Text','Repost','Comment','Like','Image link','Video link'])
    if not os.path.exists("./csv_log/" ):
        os.makedirs("./csv_log/" )
    data_df.to_csv("./csv_log/"+csv_name, encoding="utf-8-sig",index=None)

    print("\r[INFO] 图片下载中",end="")
    if len(data)>0 and save_images:
        download_images(data_df,"./media/")

    print("\r[INFO] 视频下载中",end="")
    if len(data)>0 and save_videos:
        download_videos(data_df,"./media/")
    return "./csv_log/"+csv_name


def scrap(
    account_name,
    start_date="2007-1-1",
    end_date="2077-4-13",
    save_images=False,
    save_videos=False,
):
    init_date = start_date
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')  # + datetime.timedelta(days=interval)
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    csv_path = []

    while start_date + datetime.timedelta(days=60) <= end_date:
        log_name = scrap_interval(
            account_name=account_name,
            start_date=start_date,
            end_date=start_date + datetime.timedelta(days=60),
            save_images=save_images,
            save_videos=save_videos
        )
        csv_path.append(log_name)
        start_date = start_date + datetime.timedelta(days=60)

    if start_date < end_date:
        log_name = scrap_interval(
            account_name=account_name,
            start_date=start_date,
            end_date=end_date,
            save_images=save_images,
            save_videos=save_videos
        )
        csv_path.append(log_name)

    merge_csv(account_name, csv_path, init_date, end_date.strftime("%Y-%m-%d"))