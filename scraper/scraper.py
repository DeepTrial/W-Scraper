from weibo_scraper import get_weibo_tweets_by_name
import datetime,re
from .engine import download_images,download_videos

def parse_time(time_str):

    month_convert={"Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,"Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

    time_split=time_str.split(" ")
    month=time_split[1]
    day=time_split[2]
    year=time_split[-1]

    time=str(year)+"-"+str(month_convert[month])+"-"+str(day)
    return datetime.datetime.strptime(time, '%Y-%m-%d')


def filter_text(text):
    re_tag = re.compile('</?\w+[^>]*>')  # HTML标签
    new_text = re.sub(re_tag, '', text)
    new_text = re.sub(",+", ",", new_text)  # 合并逗号
    new_text = re.sub(" +", " ", new_text)  # 合并空格
    new_text = re.sub("[...|…|。。。]+", "...", new_text)  # 合并句号
    new_text = re.sub("-+", "--", new_text)  # 合并-
    new_text = re.sub("———+", "———", new_text)  # 合并-
    return new_text


def scrap(
    account_name,
    start_date="2007-1-1",
    end_date="2077-4-13",
    save_images=False,
    save_videos=False,
):

    images=[]
    videos=[]

    start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d')# + datetime.timedelta(days=interval)
    end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d')

    if end_date<start_date:
        return


    for tweet in get_weibo_tweets_by_name(name=account_name, pages=None):
        current_time=tweet['mblog']['created_at']
        current_date=parse_time(current_time)
        if current_date>=start_date and current_date<=end_date:
            text=tweet['mblog']['text']
            img_url_list=tweet['mblog']['pic_ids']
            if len(img_url_list):
                img_prefix=tweet['mblog']['original_pic'].split("large")[0]
                for url in img_url_list:
                    images.append((current_date.strftime("%Y-%m-%d %H:%M:%S").split(" ")[0],img_prefix+"large/"+url+".jpg"))
            if r"微博视频" in text:

                video_url=tweet['mblog']["page_info"]["urls"]['mp4_ld_mp4']
                videos.append((current_date.strftime("%Y-%m-%d %H:%M:%S").split(" ")[0],video_url))
        # elif current_date<=start_date:
        #     break
            print(filter_text(text))
    print("\r[INFO] 图片下载中")
    if save_images:
        download_images(account_name,"./media/",images)

    print("\r[INFO] 视频下载中")
    if save_videos:
        download_videos(account_name,"./media/",videos)