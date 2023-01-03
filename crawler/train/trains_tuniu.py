# --* encoding: utf-8 *--

import time
import requests
import pandas as pd

from bs4 import BeautifulSoup

urls = {
    'base': 'https://huoche.tuniu.com',
    'stations': 'https://www.12306.cn/index/script/core/common/station_name.js'
}

