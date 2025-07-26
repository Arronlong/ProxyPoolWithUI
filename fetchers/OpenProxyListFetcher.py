# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re

class OpenProxyListFetcher(BaseFetcher):
    """
    https://github.com/roosterkid/openproxylist
    """

    def fetch(self):

        proxies = []
        # 使用正则表达式匹配 IP:Port 格式
        pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(?P<port>\d+)'
        headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.130 Chrome/79.0.3945.130 Safari/537.36'
            }

        # https代理
        html = requests.get('https://cdn.jsdelivr.net/gh/roosterkid/openproxylist@main/HTTPS_RAW.txt', headers=headers, timeout=10).text
        matches = re.findall(pattern, html)
        # 构造结果列表
        result = [('https', match[0], int(match[1])) for match in matches]
        proxies.extend(result)

        # socks4代理
        html = requests.get('https://cdn.jsdelivr.net/gh/roosterkid/openproxylist@main/SOCKS4_RAW.txt', headers=headers, timeout=10).text
        matches = re.findall(pattern, html)
        # 构造结果列表
        result = [('socks4', match[0], int(match[1])) for match in matches]
        proxies.extend(result)

        # socks5代理
        html = requests.get('https://cdn.jsdelivr.net/gh/roosterkid/openproxylist@main/SOCKS5_RAW.txt', headers=headers, timeout=10).text
        matches = re.findall(pattern, html)
        # 构造结果列表
        result = [('socks5', match[0], int(match[1])) for match in matches]
        proxies.extend(result)

        return list(set(proxies))
