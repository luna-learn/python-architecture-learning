
# --* encoding: utf-8 *--

import time
import json
import requests
import pandas as pd

from bs4 import BeautifulSoup


url = 'https://dl.stream.qqmusic.qq.com/C400003xRoqM3WiRKR.m4a?guid=2769278550&vkey=E0028B37141710302FEB76D5C275E32CB8544B8F3286CD443EAF7C51FA20E8A3ADCC672D0C2FD8E22E82E70CD54CDE96A25DAEDE58376B1D&uin=&fromtag=120002'


def serach(name):
    timestamp = int(time.time())
    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?_=%d&sign=zzb7ff559f5tn6stjzclmbn52nisxaruq3f3522f7' % timestamp
    request_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'refrer': 'https://y.qq.com/',
        'origin': 'https://y.qq.com/'
    }
    params ={
        "comm": {
            "cv": 4747474,
            "ct": 24,
            "format": "json",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": 0,
            "platform": "yqq.json",
            "needNewCode": 1, "uin": 373214689,
            "g_tk_new_20200303": 246137610,
            "g_tk": 246137610
        },
        "req_1": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "remoteplace": "txt.yqq.top",
                "searchid": "59341764399604878",
                "search_type": 0,
                "query": "谪仙",
                "page_num": 1,
                "num_per_page": 10
            }
        }
    }


    response = requests.get(url, headers=request_header, params=params)
    response.encoding = 'utf-8'

    print(response.text)


def download(url, path):
    request_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'refrer': 'https://y.qq.com/'
    }

    response = requests.get(url, headers=request_header)

    # print(response.content)

    fp = open(path, mode='wb')
    fp.write(response.content)
    fp.close()

# download(url, "C400003xRoqM3WiRKR.m4a")
serach("")


