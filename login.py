import qrcode
from urllib3 import disable_warnings
from requests import Response, Session
from qrcode.image.pil import PilImage
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QByteArray, QBuffer

disable_warnings()
# 变量初始化
image: PilImage|None = None
qrcode_key: str = ""
session: Session = Session()
session.headers.update({
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
	'authority': 'api.vc.bilibili.com', 'accept': 'application/json, text/plain, */*',
	'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'content-type': 'application/x-www-form-urlencoded',
	'origin': 'https://message.bilibili.com', 'referer': 'https://message.bilibili.com/',
	'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"',
	'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-site',
	"Connection": "close"
})
session.verify = False

def get_response(url: str, type: str = "get") -> Response:
		# sleep(0.1)
		if type == "post":
			response: Response = session.post(url=url, timeout=10)
		else:
			response: Response = session.get(url=url, timeout=10)
		status_code: int = response.status_code
		if status_code != 200: # 响应码不是200, 请求发生错误
			raise Exception("status code is between 300 and 599, request error")
		return response

def get_qrcode() -> None:
	global qrcode_key, image
	datas: dict = get_response("https://passport.bilibili.com/x/passport-login/web/qrcode/generate?source=main-fe-header").json()
	url: str = datas["data"]["url"]
	qrcode_key = datas['data']['qrcode_key']
	print(f"get qrcode key: {qrcode_key}")
	# code: int = datas["code"]
	image_PIL = qrcode.make(url)
	byte_array = QByteArray()
	buffer = QBuffer(byte_array)
	buffer.open(QBuffer.WriteOnly)
	image_PIL.save(buffer, "PNG")  # 你可以根据需要更改格式
	buffer.close()
	
	# 从字节流中创建QPixmap对象
	qpixmap = QPixmap()
	qpixmap.loadFromData(byte_array, "PNG")  # 确保格式一致
	
	return qpixmap
	# return image_PIL

def get_status() -> int:
	global qrcode_key
	"""
	获取二维码扫描状态
	返回值:
		0: 已登陆
		其它: 未登陆
	"""
	# https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key=
	data: dict = get_response(f"https://passport.bilibili.com/x/passport-login/web/qrcode/poll?qrcode_key={qrcode_key}&source=main-fe-header").json()
	return data["data"]["code"]

def get_user_info() -> dict:
	"""
	获取用户信息
	返回值:
		用户信息字典:
			{
				name: str, # 用户名
				image: QPixmap # 用户头像
			}
	"""
	# https://api.bilibili.com/x/web-interface/nav
	data: dict = get_response("https://api.bilibili.com/x/web-interface/nav").json()
	name: str = data["data"]["uname"]
	image_url: str = data["data"]["face"]
	image_format: str = image_url.split(".")[-1]
	image_bytes: bytes = get_response(image_url, "get").content
	image = QPixmap()
	image.loadFromData(image_bytes, image_format)
	return {
		"name": name,
		"image": image
	}

# def main() -> None:
# 	get_qrcode()
# 	print(f"请扫描二维码登录")
# 	status = get_status()
# 	while status:
# 		print(f"二维码扫描状态: {status}")
# 		sleep(0.5)
# 		status = get_status()
# 	print(f"登陆成功")
# 	print(session.cookies.get_dict())

# if __name__ == '__main__':
# 	main()