import time, random, datetime
from win32api import SetCursorPos, mouse_event, keybd_event
from win32gui import SetWindowPos, SetForegroundWindow, GetWindowRect, FindWindow
from win32con import SWP_SHOWWINDOW, MOUSEEVENTF_LEFTDOWN, \
    MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, \
    KEYEVENTF_KEYUP
from ctypes import windll
from PIL import Image, ImageGrab
from cv2 import imread, cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCORR_NORMED, minMaxLoc
from pytesseract import image_to_string
from VK_CODES import VK_CODE
from skimage.measure import compare_ssim


EXIT = False
INFO = []
# 1.需要训练字库
# 2.需要制定截屏位置
# 3.配置图片识别路径
class DnfTool(object):
    """扫拍"""

    def __init__(self, name):
        # 获得句柄
        self.handle = FindWindow(None, name)
        self.left, self.top, self.right, self.bottom = GetWindowRect(self.handle)

    def set_window(self):
        """设置窗口"""
        # 窗口大小
        width = self.right - self.left
        height = self.bottom - self.top
        # 设置窗口位置
        SetWindowPos(self.handle, None, 0, 0, width, height, SWP_SHOWWINDOW)
        # 设置窗口位于前台
        SetForegroundWindow(self.handle)

    def click_left(self, x, y, sleep1=0.05, sleep2=0.1):
        """模拟鼠标点击"""
        left, top, right, bottom = GetWindowRect(self.handle)
        # 鼠标移动到指定的坐标
        SetCursorPos((left + x, top + y))
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(sleep1)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(sleep2)

    def click_right(self, x, y, sleep1=0.05, sleep2=0.1):
        left, top, right, bottom = GetWindowRect(self.handle)
        # 鼠标移动到指定的坐标
        SetCursorPos((left + x, top + y))
        mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
        time.sleep(sleep1)
        mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
        time.sleep(sleep2)

    def open_vk(self, *key, sleep=0.02):
        """键盘模拟"""

        def vk_key(num, sleep):
            """模拟键盘"""
            # 获得特征码
            MapVirtualKey = windll.user32.MapVirtualKeyA
            keybd_event(VK_CODE[str(num)], MapVirtualKey(VK_CODE[str(num)], 0), 0, 0)
            time.sleep(sleep)
            keybd_event(VK_CODE[str(num)], MapVirtualKey(VK_CODE[str(num)], 0), KEYEVENTF_KEYUP, 0)

        # 要模拟的按键
        for num in key:
            vk_key(num, sleep)

    # 图片对比
    def compare_cv2(self, path_one, seat):
        goods = self.grab_dnf(seat)

        image_one = imread(path_one)
        get_one = imread(goods)

        gray1 = cvtColor(image_one, COLOR_BGR2GRAY)
        gray2 = cvtColor(get_one, COLOR_BGR2GRAY)

        (score, diff) = compare_ssim(gray1, gray2, full=True)
        return int(score * 100)

    # 图片识别
    def disting(self, coordinate, font_dnf="num"):
        """图片识别,
           coordinate为图片位置坐标数据为list
           font_dnf 训练的字体库
        """
        img = ImageGrab.grab(coordinate[0])
        out = img.resize((coordinate[1], coordinate[2]), Image.ANTIALIAS)
        out.save('get_image/wu.png')
        src = imread('get_image/wu.png')
        gray = cvtColor(src, COLOR_BGR2GRAY)
        text = image_to_string(gray, lang=font_dnf)
        return text

    # 截取指定位置图片
    def grab_dnf(self, seat):
        """识别指定位置图像seat:传入图片坐标点列表"""
        img = ImageGrab.grab(seat)
        img.save('get_image/goods.png')

        return 'get_image/goods.png'

    # 模板匹配
    def template_img(self, path, zuobiao_li, accuracy=98):
        """模板匹配"""
        # 模板图片
        tpl = imread(path)
        # 目标图片
        image_template = self.grab_dnf(zuobiao_li)
        target = imread(image_template)
        # 获得模板的高宽
        th, tw = tpl.shape[:2]
        result = matchTemplate(target, tpl, TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = minMaxLoc(result)
        br = (max_loc[0] + tw, max_loc[1] + th)
        if int(max_val * 100) >= accuracy:
            return br
        if path == 'image_template/006.png' and int(max_val * 100) >= 95:
            return br
        else:
            return None


class Price(DnfTool):
    """购买物品"""
    GOODS_DATA = None

    # 添加物品
    def input_dnf(self, goods_data):
        # 添加物品
        Price.GOODS_DATA = goods_data

    # 获得价格
    def check(self, coordinate, vi=None):
        # 判断价格符合则购买
        price = ''
        text = self.disting(coordinate)
        if not text:
            print('无法识别')
            if vi is None:
                self.click_left(638, 378)  # 物品不存在
            return 1
        for i in text:
            try:
                if int(i) or i == '0':
                    price += str(i)
            except Exception as e:
                pass
        return int(price)

    # 保存购买记录
    def write_info(self, price, name, num=None):
        str_info = self.complete_buy()
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print('购买结果%s' % str_info)
        if str_info:
            self.click_left(641, 395)  # 点击购买完成

            with open('goods_info.txt', 'a') as f:

                if num:
                    # 普通购买有数量时
                    self.total = num * price
                    f.write('\n%s购买: %s 单价 %d 数量 %d 总价是: %d' % (
                        now_time, name, price, num, self.total))

                    return '%s购买:%s成功单价%d 数量%d 总价是:%d' % (
                        now_time, name, price, num, self.total)
                else:
                    self.total = price
                    f.write('\n%s购买: %s 单价 %d 数量 %d 总价是: %d' % (
                        now_time, name, price, num, self.total))

                    return '%s购买: %s成功  价格%s' % (now_time, name, price)
        else:

            with open('goods_info.txt', 'a') as f:
                f.write('\n%s购买: %s 单价 %d 数量 %d 物品不存在 0' % (
                    now_time, name, price, num))

            print("物品不存在")
            self.click_left(638, 378)  # 物品不存在
            return '%s购买:%s失败 物品不存在' % (now_time, name)

    # 启动
    def start_dnf(self, vk=None):
        """启动"""
        self.set_window()  # 设置窗口位置
        time.sleep(1)
        self.empty_window()
        if vk is None:
            return
        else:
            self.open_vk(vk)

    # 清屏
    def empty_window(self):
        self.open_vk('esc')
        time.sleep(0.2)
        ret_num = self.compare_cv2('image_template/010.png', [599, 169, 695, 190])
        print('系统菜单:%s' % ret_num)
        if ret_num > 95:
            self.open_vk('esc')

    # 搜索
    def search(self, func_type, sleep=0.02):

        """搜索物品 ,num = 搜搜次数"""

        def search_input(goods, sleep, x, y=201):
            r_num = random.randint(1, 6)
            self.click_left(865 + r_num, 145 + r_num, sleep1=0.2, sleep2=0.1)  # 点击默认
            time.sleep(0.13)
            self.click_left(865 + r_num, 145 + r_num, sleep2=0.15)  # 点击默认
            self.click_left(353, 150)  # 点击输入框
            # self.click_left(353, 150)  # 点击输入框
            for VK in goods:
                self.open_vk(VK, sleep=sleep)
            self.open_vk('spacebar', sleep=0.07)
            self.click_left(825 + r_num, 145 + r_num)  # 搜索
            SetCursorPos((x, y))
            time.sleep(0.01)
            return r_num

        total = 0
        if func_type == self.price_putong:
            x_axis = 785
        if func_type == self.price_juanzi:
            x_axis = 420

        for goods_data in Price.GOODS_DATA:
            self.image_path = 'image/%s.png' % goods_data[0]
            if goods_data[2] == '0':
                continue
            r_num = search_input(goods_data[0], sleep, x_axis)
            info1 = func_type(goods_data[2], goods_data[1])
            INFO.append(info1)
            try:
                if self.total:
                    total += self.total
                    self.total = 0
                    self.click_left(825 + r_num, 145 + r_num)  # 搜索
                    SetCursorPos((x_axis, 201))
                    if x_axis == 785:
                        time.sleep(0.6)
                    else:
                        time.sleep(0.15)
                    info2 = func_type(goods_data[2], goods_data[1])
                    INFO.append(info2)
                    if self.total:
                        total += self.total
                        self.total = 0
            except Exception as e:
                pass
        return total

    # 判断卷子价格
    def price_juanzi(self, appoint, name):
        appoint = int(appoint)
        price = self.check(([783, 188, 853, 203], 140, 30))
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if price == 1:
            return '无法识别'

        if appoint < price:
            return '%s %s价格:%s大于设定价格:%d,不购买' % (now_time, name, price, appoint)

        if appoint > price > 1:
            # 价格符合获得物品名字,物品天数
            goods_name = self.compare_cv2(self.image_path, [488, 193, 638, 213])
            day = self.compare_cv2('image/30day.png', [375, 315, 403, 328])
            if (goods_name >= 95) and (day >= 95):
                # 名字和天数都符合,购买
                self.buy_juanzi()
                time.sleep(0.1)
                info = self.write_info(price, name)
                return info
            else:
                if goods_name < 95:
                    # 名字不符合
                    return '不是同一个物品'
                elif day < 95:
                    # 天数不符合
                    return '%s:%s小于%s天数不符合' % (name, price, appoint)

    # 购买卷子
    def buy_juanzi(self):
        """购买"""
        self.click_left(785, 201)  # 点击购买
        self.click_left(785 + 30, 201 + 10)  # 点击一口价
        self.click_left(599, 378)  # 点击确定
        self.click_left(606, 395)  # 再次点击确定
        self.click_left(654, 413)  # 点击确认购买

    # 判断普通物品价格区间
    def check_putong(self, appoint):
        shi = ([690, 195, 708, 210], 40, 30)
        bai = ([688, 195, 710, 210], 50, 30)

        qian = ([682, 195, 720, 210], 80, 30)
        wan = ([681, 195, 721, 210], 100, 30)
        shi_wan = ([682, 195, 720, 210], 100, 30)
        bai_wan = ([673, 195, 727, 210], 120, 30)
        if 9 < appoint < 100:
            price = self.check(shi)

            return price
        elif 99 < appoint < 1000:
            price = self.check(bai)

            return price
        elif 999 < appoint < 10000:

            price = self.check(qian)

            return price
        elif 9999 < appoint < 100000:
            price = self.check(wan)

            return price
        elif 99999 < appoint < 1000000:
            price = self.check(shi_wan)

            return price
        elif 999999 < appoint:
            price = self.check(bai_wan)
            return price

    # 判断普通物品价格
    def price_putong(self, appoint, name):
        """appoint设定价格
            goods物品"""
        appoint = int(appoint)
        # 获得总价
        price = self.check_putong(appoint)
        # name = self.name_dict[goods]
        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if price == 1:
            return '无法识别'

        if appoint < price:
            time.sleep(0.1)
            return '%s %s价格:%s大于设定价格:%d,不购买' % (now_time, name, price, appoint)

        if appoint >= price > 1:  # 价格合适
            # 获得单价
            price_total = self.check(([783, 188, 853, 203], 140, 30))

            # 确认是否是这个物品
            ret = self.compare_cv2(self.image_path, [488, 193, 638, 213])
            # if (price_total / price) < 100 and price >= appoint:
            #     return '%s数量小于100' % name

            if ret >= 90:
                # 是同一个物品购买
                self.buy_putong()
                num = int(price_total / price)
                time.sleep(0.1)
                # 记录信息
                info = self.write_info(price, name, num)
                return info
            else:
                return '不是同一个物品'

    # 判断是否购买完成
    def complete_buy(self):
        """是否购买完成"""
        ret = self.compare_cv2('image/goumaiwancheng.png', [561, 322, 618, 340])
        if ret > 95:
            return 1
        else:
            return False

    # 购买普通物品
    def buy_putong(self):
        self.click_left(785, 201)  # 点击购买
        self.click_left(785 + 30, 201 + 10)  # 点击一口价
        time.sleep(0.1)
        # self.total_price = self.check(([830, 197, 895, 212], 120, 30))
        self.click_left(828, 224)  # 点击确定数量
        self.click_left(879, 244)  # 点击确定