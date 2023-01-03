import os, sys, time, random, datetime
import numpy as np
from win32api import SetCursorPos, GetCursorPos, GetSystemMetrics, mouse_event, keybd_event
from win32gui import SetWindowPos, SetForegroundWindow, GetWindowRect, \
    EnumWindows, FindWindow, GetClassName, GetWindowText, \
    GetDC, ClientToScreen
from win32print import GetDeviceCaps
from win32con import LOGPIXELSX, HORZRES, VERTRES, DESKTOPHORZRES, DESKTOPVERTRES, \
    SWP_SHOWWINDOW, \
    MOUSEEVENTF_MOVE, MOUSEEVENTF_ABSOLUTE, \
    MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, \
    KEYEVENTF_KEYUP, \
    SM_CXSCREEN, SM_CYSCREEN
from ctypes import windll

# from pymouse import *
# from pykeyboard import PyKeyboard

from PIL import Image, ImageGrab
import cv2
# from cv2 import imread, cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCORR_NORMED, minMaxLoc

# 创建Haar级联器
facer = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
# 导入人脸图片并灰度化
img = cv2.imread('p3.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 调用接口
faces = facer.detectMultiScale(gray, 1.1, 5)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('img', img)
cv2.waitKey()