# -- coding: utf-8 --

from time import sleep
from video import *
from login import *

def main() -> None:
	print("Bilibili视频下载器")
	print("="*30)
	print("1. 下载单个视频")
	print("2. 下载视频合集")
	print("3. 下载选集视频")
	print("4. 退出程序")
	print("="*30)

	get_qrcode()
	print(f"请扫描二维码登录")
	status = get_status()
	while status:
		print(f"二维码扫描状态: {status}")
		sleep(0.5)
		status = get_status()
	print(f"登陆成功")
	cookies = session.cookies.get_dict()
	print(cookies)

	headers["cookie"] = '; '.join([f'{key}={value}' for key, value in cookies.items()])

	choice = input("请输入选项：")
	url = input("请输入链接：")
	if choice == "1":
		save_video(url)
	elif choice == "2":
		collection_videos(url)
	elif choice == "3":
		list_videos(url)
	elif choice == "4":
		exit()
	else:
		print("输入错误，请重新输入！")

if __name__ == '__main__':
	main()