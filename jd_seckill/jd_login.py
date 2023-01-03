import random
import time
import requests
import functools
import json
import os
import pickle


class JDLogin(object):

    def __init__(self):
        self.__login_qr_image_file = 'jd_login_qr_code.png'
        self.__header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/96.0.4664.45 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;"
                          "q=0.9,image/webp,image/apng,*/*;"
                          "q=0.8,application/signed-exchange;"
                          "v=b3",
            "Connection": "keep-alive"
        }
        self.__session = requests.session()
        self.__cookie = self.__session.cookies
        