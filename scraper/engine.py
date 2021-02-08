import os
import scraper.video as video
import requests
import urllib
from colorama import init, Fore, Style
from time import sleep
import random,re,datetime
init()


def download_videos(data_frame,save_dir):
    try:
        username = data_frame['UserName'].iloc[0]
        if not os.path.exists(save_dir + "/" + username):
            os.makedirs(save_dir + "/" + username)
        save_dir = os.path.join(save_dir, username)
    except:
        pass

    for i, url_video in enumerate(data_frame["Video link"]):
        if len(url_video)==0:
            continue
        try:
            data_time = data_frame['Timestamp'].iloc[i]
            res = requests.get(url_video[0], stream=True)
            with open(save_dir + '/' + data_time + '_post-' + str(i + 1) + ".mp4", "wb") as mp4:
                for chunk in res.iter_content(chunk_size=1024 * 1024):  # 当流下载时，用Response.iter_content或许更方便些。requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content　来边下载边存硬盘
                    if chunk:
                        mp4.write(chunk)
        except:
            print('\r[' + Fore.YELLOW + 'WARNING' + Style.RESET_ALL + '] ' +  url_video + " video download failed")
        sleep(random.uniform(0, 1))


def download_images(data_frame, save_dir):
    username = data_frame['UserName'].iloc[0]
    if not os.path.exists(save_dir + "/" + username):
        os.makedirs(save_dir + "/" + username)
    save_dir = os.path.join(save_dir, username)

    for i, url_v in enumerate(data_frame["Image link"]):
        for j, url in enumerate(url_v):
            data_time=data_frame['Timestamp'].iloc[i]
            try:
                urllib.request.urlretrieve(url, save_dir + '/'+data_time+'_post-'+str(i+ 1)+"-"+str(j+1) + ".jpg")
            except:
                try:
                    imgres = requests.get(url)
                    with open(save_dir + '/' + data_time + '_post-' + str(i + 1) + ".jpg", "wb") as f:
                        f.write(imgres.content)
                except:
                    print('\r[' + Fore.YELLOW + 'WARNING' + Style.RESET_ALL + '] ' + url + " image download error")
            sleep(random.uniform(0,1))

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

def parse_blog(mblog):
    current_time = mblog['mblog']['created_at']
    current_date = parse_time(current_time)
    username=mblog['mblog']['user']['screen_name']
    user_id = mblog['mblog']['user']['id']
    reposts=mblog['mblog']['reposts_count']
    comments=mblog['mblog']['comments_count']
    likes=mblog['mblog']['attitudes_count']
    text = filter_text(mblog['mblog']['text'])
    images=[]
    videos=[]

    img_url_list = mblog['mblog']['pic_ids']
    if len(img_url_list):
        img_prefix = mblog['mblog']['original_pic'].split("large")[0]
        for url in img_url_list:
            images.append(img_prefix + "large/" + url + ".jpg")

    if r"微博视频" in text:
        video_url = mblog['mblog']["page_info"]["urls"]['mp4_ld_mp4']
        videos.append(video_url)
    return current_date,[username,user_id,current_date.strftime("%Y-%m-%d %H:%M:%S").split(" ")[0],text,reposts,comments,likes,images,videos]