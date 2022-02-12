# --* encoding: utf-8 *--

import time
import json
import requests
import pandas as pd

from bs4 import BeautifulSoup

# https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs=%E5%8C%97%E4%BA%AC,BJP&ts=%E4%B8%8A%E6%B5%B7,SHH&date=2022-02-11&flag=N,N,Y
# https://search.12306.cn/search/v1/train/search?keyword=G609&date=20220212
# https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no=240000G6090B&leftTicketDTO.train_date=2022-02-12&rand_code=
urls = {
    'base': 'https://www.12306.cn/index/',
    'stations': 'https://www.12306.cn/index/script/core/common/station_name.js',
    'trains': 'https://www.12306.cn/index/otn/zwdch/queryCC',
    'ticket': 'https://kyfw.12306.cn/otn/leftTicket/init',
    'train': 'https://search.12306.cn/search/v1/train/search',
    'trainInfo': 'https://kyfw.12306.cn/otn/queryTrainInfo/query'
}



# popcitylist
def list_cities():
    request_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'refrer': 'https://www.12306.cn'
    }
    request = requests.get(urls['base'], headers=request_header)
    request.encoding = 'utf-8'
    print(request.text)
    soup = BeautifulSoup(request.text, 'html.parser')
    cities = soup.find_all('ul', attrs={'class': 'popcitylist'}).find_all('li')
    for city in cities:
        print(city)


def list_stations():
    request_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
        'refrer': 'https://www.12306.cn'
    }
    request = requests.get(urls['stations'], headers=request_header)
    request.encoding = 'utf-8'
    print(request.text)
    a = request.text.index("'", 0)
    b = request.text.index("'", a + 1)
    print(request.text[(a + 1): b].split('@'))
    result = []
    for x in request.text[(a + 1): b].split('@'):
        if len(x) > 0:
            result.append(x.split('|'))
    return pd.DataFrame(data=result, columns=['name_short', 'name', 'code', 'name_pinyin', 'name_sample', 'id'])


def list_station_trains(station_code):
    """
    通过 station_code 查询经过车站的车次列表
    :param station_code: 车站代码
    :return:
    """
    request_header = {
        'Host': 'www.12306.cn',
        'Origin': 'https://www.12306.cn',
        'Referer': 'https://www.12306.cn/index/index.html',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
    }
    request = requests.post(urls['trains'], data={'train_station_code': station_code}, headers=request_header)
    request.encoding = 'utf-8'
    print(request.text)
    data = json.loads(request.text)
    print(data['data'])
    return pd.DataFrame(data=data['data'], columns=['train_number'])


def search_trains():
    pass

def search_train(train_number):
    request_header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
    }
    # keyword=G609&date=20220212
    tomorrow = time.strftime('%Y%m%d', time.localtime(time.time() + 86400))
    url = urls['train'] + "?keyword=%s&date=%s" % (train_number, tomorrow)
    print(url)
    request = requests.get(url, headers=request_header)
    request.encoding = 'utf-8'
    print(request.text)
    try:
        data = json.loads(request.text)
        print(data['data'])
    except:
        print("error")



def get_train_info(train_no):
    request_header = {
        'Host': 'kyfw.12306.cn',
        'Referer': 'https: // kyfw.12306.cn / otn / queryTrainInfo / init',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
    }
    # keyword=G609&date=20220212
    tomorrow = time.strftime('%Y-%m-%d', time.localtime(time.time() + 86400))
    url = urls['trainInfo'] + "?leftTicketDTO.train_no=%s&leftTicketDTO.train_date=%s&rand_code=" % (train_no, tomorrow)
    print(url)
    request = requests.get(url, headers=request_header)
    request.encoding = 'utf-8'
    print(request.text)
    data = json.loads(request.text)
    print(data['data'])


# list_cities()
# print(list_stations())
# list_station_trains("BJP")
search_train('G609')
get_train_info('240000G6090B')

