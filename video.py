# -- coding: utf-8 --

# from time import sleep
from re import findall
from json import loads
from os import mkdir, remove
from os.path import exists
from requests import get, Response
from urllib3 import disable_warnings
from subprocess import check_output, DEVNULL

disable_warnings()

# 变量初始化
ffmpeg_path: str = "D:\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe"
video_num: int = 0
now_index: int = 0
title: str = ""
headers: dict = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
	'authority': 'api.vc.bilibili.com', 'accept': 'application/json, text/plain, */*',
	'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'content-type': 'application/x-www-form-urlencoded',
	'origin': 'https://message.bilibili.com', 'referer': 'https://message.bilibili.com/',
	'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
	"Connection": "close",
    "Cookie": "DedeUserID=3494353660020892; DedeUserID__ckMd5=47b872492f6c0cc3; SESSDATA=943378c1%2C1740575427%2C3e5d9%2A81CjBfgl8PkPGvEPG-lPgr-LtPUVC3mdeEcHjgwwl1wjLByGJFopL6Bh9zOdoI8mf9eD8SVl82OFp1MzJ1M0JmTzlKSHpTcnphZVhUVmVUSjNEQ1Y1TjQ4d2NYZFNUWXRhdmpUQU10RjNKbUFrZlBxTTRLaEJsU0tkUjVQOHVtYUtCeklsWUtpcHlBIIEC; bili_jct=574a4913903f83540e07122e3d237d63; sid=8k9ddh79"
}

def get_response(url: str) -> Response:
		global headers
		# sleep(0.1)
		response: Response = get(url=url, headers=headers, timeout=5, verify=False)
		status_code: int = response.status_code
		if status_code >= 300: # 响应码在300~599, 请求发生错误
			raise Exception("status code is between 300 and 599, request error")
		return response

def make_dir(path: str) -> None:
    if not exists(path):
        mkdir(path)

def make_file(path: str, content: str, mode: str = "w") -> None:
    path: str = "\\".join(path.split("\\")[0:-1])
    if path:
        make_dir(path)
    with open(path, mode) as f:
        f.write(content)

def get_video_info(url: str) -> dict:
    html: str = get_response(url).content.decode()
    datas: dict = loads(findall(pattern="<script>window.__playinfo__=(.*?)</script>", string=html)[0])
    return {
        "audio_url": datas["data"]["dash"]["audio"][0]["baseUrl"],
        "video_url": datas["data"]["dash"]["video"][0]["baseUrl"],
        "title": findall(pattern="<h1 data-title=\"(.*?)\"", string=html)[0]
    }

def save_video(url: str, title: str = None, path: str = "video\\") -> None:
    info: dict = get_video_info(url)
    # bilibili的音视频是分开的
    audio: bytes = get_response(url=info["audio_url"]).content
    video: bytes = get_response(url=info["video_url"]).content
    title: str = title if title else info["title"]
    with open(f"{url}.mp4", "wb") as f:
        f.write(video)
    with open(f"{url}.mp3", "wb") as f:
        f.write(audio)
    # 合并视频和音频
    check_output(f'{ffmpeg_path} -i "{url}.mp4" -i "{url}.mp3" -c:v copy -c:a copy -bsf:a aac_adtstoasc "{path+title}.mp4"', encoding="utf-8", shell=True, stderr=DEVNULL)
    remove(f"{url}.mp4")
    remove(f"{url}.mp3")

# 爬取视频合集
def collection_videos(url: str) -> None:
    mid: str = findall(pattern="space.bilibili.com/(\d+)", string=url)[0]
    sid: str = findall(pattern="\?sid=(\d+)", string=url)[0]
    num_per_page: int = 100
    data: dict = get_response(f"https://api.bilibili.com/x/polymer/web-space/seasons_archives_list?mid={mid}&season_id={sid}&sort_reverse=false&page_num=1&page_size={num_per_page}").json()
    name: str = data["data"]["meta"]["name"]
    video_num: int = data["data"]["page"]["total"]
    page_num: int = video_num // num_per_page + 1
    for page in range(1, page_num+1):
        data: dict = get_response(f"https://api.bilibili.com/x/polymer/web-space/seasons_archives_list?mid={mid}&season_id={sid}&sort_reverse=false&page_num={page}&page_size={num_per_page}").json()
        for video in range(num_per_page):
            bv: str = data["data"]["archives"][video]["bvid"]
            now_index: int = (page-1)*num_per_page+video+1
            # print(f"{(page-1)*num_per_page+video+1}/{video_num}", end='\r')
            save_video(f"https://www.bilibili.com/video/{bv}/?vd_source=c3aacec0b3723c2104cb91bcb760c4c5", path=f"video\\{sid}\\[{now_index}]{name}")

# 爬取选集的视频
def list_videos(url: str) -> tuple:
    html: str = get_response(url).content.decode()
    data: dict = loads(findall(pattern="<script>window.__INITIAL_STATE__=(.*?);", string=html)[0])
    name: str = data["videoData"]["title"]
    video_num: int = len(data["videoData"]["pages"])
    videos = []
    for page in range(1, video_num+1):
        now_index: int = page
        videos.append((
            f"{url}&p={page}", 
            page, 
            f"video\\{name}\\"
        ))
    return videos

if __name__ == "__main__":
    print(list_videos("https://www.bilibili.com/video/BV1qW4y1a7fU/?spm_id_from=333.337.search-card.all.click&vd_source=c3aacec0b3723c2104cb91bcb760c4c5"))