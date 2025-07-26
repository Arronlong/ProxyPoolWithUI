# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re
import time

class ZdayeFetcher(BaseFetcher):
    """
    https://www.zdaye.com/free/1/?checktime=5&sleep=3
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        urls = [f'https://www.zdaye.com/free/{page}/?checktime=5&sleep=3' for page in range(1, 7)]

        proxies = []
        ip_regex = re.compile(r'^\d+\.\d+\.\d+\.\d+$')
        port_regex = re.compile(r'^\d+$')

        for url in urls:
            time.sleep(1)
            html = requests.get(url, timeout=10).text
            doc = pq(html)
            for line in doc('tr').items():
                tds = list(line('td').items())
                if len(tds) >= 3:
                    ip = tds[0].text().strip()
                    port = tds[1].text().strip()
                    http = "https" if len(tds[6].find('.iyes')) > 0 else "http"
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append((http, ip, int(port)))

        proxies = list(set(proxies))

        return proxies
