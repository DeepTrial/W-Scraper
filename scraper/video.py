import requests


def download_video(url):
    res = requests.get(url, stream=True)
    with open('chenyuqi.mp4', "wb") as mp4:
        for chunk in res.iter_content(chunk_size=1024 * 1024):  # 当流下载时，用Response.iter_content或许更方便些。requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content　来边下载边存硬盘
            if chunk:
                mp4.write(chunk)


