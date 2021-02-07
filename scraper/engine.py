import os
import scraper.video as video
import requests
import urllib
from colorama import init, Fore, Style
from time import sleep
import random
init()

def download_videos(username,save_dir,url_list):
    if not os.path.exists(save_dir + "/" + username):
        os.makedirs(save_dir + "/" + username)
    save_dir = os.path.join(save_dir, username)

    for i, urls in enumerate(url_list):
        data_time, url = urls
        try:
            res = requests.get(url, stream=True)
            with open(save_dir + '/' + data_time + '_post-' + str(i + 1) + ".mp4", "wb") as mp4:
                for chunk in res.iter_content(
                        chunk_size=1024 * 1024):  # 当流下载时，用Response.iter_content或许更方便些。requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content　来边下载边存硬盘
                    if chunk:
                        mp4.write(chunk)
        except:
            print('\r[' + Fore.YELLOW + 'WARNING' + Style.RESET_ALL + '] ' +  url + " video download failed")

        sleep(random.randint(0, 2))


def download_images(username,save_dir,url_list):
    if not os.path.exists(save_dir + "/" + username):
        os.makedirs(save_dir + "/" + username)
    save_dir = os.path.join(save_dir, username)

    for i, urls in enumerate(url_list):
        data_time,url=urls
        try:
            urllib.request.urlretrieve(url, save_dir + '/'+data_time+'_post-'+str(i+ 1) + ".jpg")
        except:
            try:
                imgres = requests.get(url)
                with open(save_dir + '/' + data_time + '_post-' + str(i + 1) + ".jpg", "wb") as f:
                    f.write(imgres.content)
            except:
                print('\r[' + Fore.YELLOW + 'WARNING' + Style.RESET_ALL + '] ' + url + " image download error")

        sleep(random.randint(0,2))