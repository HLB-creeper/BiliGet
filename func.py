from requests import get, Response
# from time import sleep

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

def get_response(url: str, stream: bool = False) -> Response:
    global headers
    # sleep(0.1)
    return get(url=url, headers=headers, timeout=5, verify=False, stream=stream)