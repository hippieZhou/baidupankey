"""
Author:hippieZhou
Date:20190606
Description: Get BaiDuYun shared link's Code 
"""
import argparse
import re
import requests
import json
import time

VERSION = "VERSION 1.0.0"


def checkUrl(url: str) -> str:
    m1 = re.match(
        "https?:\/\/pan\.baidu\.com\/s\/1([a-zA-Z0-9_\-]{5,22})", url)
    m2 = re.match(
        "https?:\/\/pan\.baidu\.com\/share\/init\?surl=([a-zA-Z0-9_\-]{5,22})", url)
    if not m1 and not m2:
        print("参数不合法")
        return False
    else:
        return True


def getKey(url: str) -> bool:
    if checkUrl(url):
        try:
            req = requests.get(f"https://node.pnote.net/public/pan?url={url}")
            code = req.status_code
            if code == 200:
                data = dict(json.loads(req.text))
                status = data.get("status", False)
                if status:
                    return data.get("access_code", "未能查询到该链接的提取码，可能原因是：该链接不需要提取码或已过期")
                else:
                    return data.get("messages", "为能查询到提取码")
            elif code == 404:
                return "不存在该链接的记录"
        except Exception as e:
            return f"请求服务器失败，错误代码:{code}"


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
    """
    https://pan.baidu.com/s/1qYEj76s
    {'status': True, 'access_url': 'https://pan.baidu.com/s/1qYEj76s'}
    https://pan.baidu.com/s/1qYLrSOs 密码：wezk
    {'status': True, 'access_url': 'https://pan.baidu.com/s/1qYLrSOs', 'access_code': 'wezk'}
    http://pan.baidu.com/s/1dtT3i7y
    {'status': True, 'access_url': 'https://pan.baidu.com/s/1dtT3i7y'}
    https://pan.baidu.com/s/1gfrjidd 密码: imfc
    http://pan.baidu.com/s/1bnXdqdp
    {'status': True, 'access_url': 'https://pan.baidu.com/s/1bnXdqdp'}
    https://pan.baidu.com/s/1c7VEcIXt1ELRMwMbg1dcGg
    {'messages': '暂未收录该链接的提取码', 'status': False}
    """
    lis = ["https://pan.baidu.com/s/1qYEj76s",
           "https://pan.baidu.com/s/1qYLrSOs",
           "http://pan.baidu.com/s/1dtT3i7y",
           "https://pan.baidu.com/s/1gfrjidd",
           "http://pan.baidu.com/s/1bnXdqdp",
           "https://pan.baidu.com/s/1c7VEcIXt1ELRMwMbg1dcGg"]
    command_line_runner()


if __name__ == "__main__":
    main()
