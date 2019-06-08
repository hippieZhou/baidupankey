"""
Author:hippieZhou
Date:20190608
Description: Get BaiDuYun shared link's Code 
"""

import argparse
import time
import re
import requests
from datetime import datetime
import json

accessKey = "4fxNbkKKJX2pAm3b8AEu2zT5d2MbqGbD"
clientVersion = "web-client"


def getPid(url: str) -> str:
    matches = re.match(
        "https?:\/\/pan\.baidu\.com\/s\/1([a-zA-Z0-9_\-]{5,22})", url)
    return matches[1] if matches else None


def getUuid(pid: str) -> str:
    return f"BDY-{pid}"


def getKey(url: str) -> str:
    pid = getPid(url)
    uuid = getUuid(pid)
    headers = {
        "type": "GET",
        "data": '',
        "dataType": "json"
    }
    url = f"http://ypsuperkey.meek.com.cn/api/items/{uuid}?access_key={accessKey}&client_version={clientVersion}&{datetime.utcnow()}"
    try:
        req = requests.get(url, headers=headers)
        code = req.status_code
        if code == 200:
            data = json.loads(req.text)
            accessCode = data.get("access_code", None)
            return "没找到提取密码，o(╥﹏╥)o" if (accessCode == "undefined" or accessCode == None or accessCode == "") else accessCode
        elif code == 400:
            return " 服务器不理解请求的语法"
        elif code == 404:
            return "不存在该链接的记录"
        else:
            return f"请求服务器失败，错误代码:{code}"
    except Exception as e:
        return e


def get_parser():
    parser = argparse.ArgumentParser()
    parser.description = "百度网盘提取码一键获取器"
    parser.add_argument('urls', metavar="urls", type=str, nargs="*",
                        help='设置要获取提取码的链接(多个链接请用空格分隔)')
    parser.add_argument('-v', '--version', action='store_true',
                        help='版本号')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print(VERSION)
        return

    s_time = time.time()
    if len(args['urls']) > 1:
        for item in args["urls"][1:]:
            print(f"{item}:\r\n\t{getKey(item)}")
        e_time = time.time()
        print(f"\n\n操作完毕，总耗时：{e_time-s_time} 秒")


def main():
    command_line_runner()


if __name__ == "__main__":
    main()
