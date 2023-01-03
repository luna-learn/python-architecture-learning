# --* encoding: utf-8 *--

import time
import requests
import pandas as pd

import bs4

urls = {
    'base': 'https://train.qunar.com'
}

request_header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
    'refrer': 'https://www.qunar.com/',
    
}
