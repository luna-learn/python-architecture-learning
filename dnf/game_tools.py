import ctypes
import os, sys, time, random, datetime, math
import numpy as np
import threading
from win32api import SetCursorPos, GetCursorPos, GetSystemMetrics, \
    GetCurrentThreadId, \
    mouse_event, keybd_event
from win32gui import SetWindowPos, SetForegroundWindow, GetForegroundWindow, GetWindowRect, \
    EnumWindows, FindWindow, GetClassName, GetWindowText, \
    GetDC, ClientToScreen, \
    GetMessage
from win32print import GetDeviceCaps
from win32con import LOGPIXELSX, HORZRES, VERTRES, DESKTOPHORZRES, DESKTOPVERTRES, \
    SWP_SHOWWINDOW, \
    MOUSEEVENTF_MOVE, MOUSEEVENTF_ABSOLUTE, \
    MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP, MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP, \
    KEYEVENTF_KEYUP, \
    SM_CXSCREEN, SM_CYSCREEN, \
    HC_ACTION, WH_KEYBOARD_LL
from ctypes import windll, cast, Structure, CFUNCTYPE, POINTER, pointer, sizeof, \
    c_void_p, c_int, c_uint, c_long, c_ulong

from ctypes.wintypes import HWND, LPARAM, UINT, WPARAM, DWORD, LONG, ULONG, LPDWORD

# from pymouse import *
# from pykeyboard import PyKeyboard

from PIL import Image, ImageGrab
# from cv2 import imread, cvtColor, COLOR_BGR2GRAY, matchTemplate, TM_CCORR_NORMED, minMaxLoc

GetWindowThreadProcessId = windll.user32.GetWindowThreadProcessId
MapVirtualKey = windll.user32.MapVirtualKeyA
SetWindowsHookEx = windll.user32.SetWindowsHookExA
UnhookWindowsHookEx = windll.user32.UnhookWindowsHookEx
CallNextHookEx = windll.user32.CallNextHookEx
# GetMessage = windll.user32.GetMessageW
GetModuleHandle = windll.kernel32.GetModuleHandleW


VK_CODE = {
    'backspace': 0x08,
    'tab': 0x09,
    'clear': 0x0C,
    'enter': 0x0D,
    'shift': 0x10,
    'ctrl': 0x11,
    'alt': 0x12,
    'pause': 0x13,
    'caps_lock': 0x14,
    'esc': 0x1B,
    'space': 0x20,
    'page_up': 0x21,
    'page_down': 0x22,
    'end': 0x23,
    'home': 0x24,
    'left_arrow': 0x25,
    'up_arrow': 0x26,
    'right_arrow': 0x27,
    'down_arrow': 0x28,
    '←': 0x25,
    '↑': 0x26,
    '→': 0x27,
    '↓': 0x28,
    'select': 0x29,
    'print': 0x2A,
    'execute': 0x2B,
    'print_screen': 0x2C,
    'ins': 0x2D,
    'del': 0x2E,
    'help': 0x2F,
    '0': 0x30,
    '1': 0x31,
    '2': 0x32,
    '3': 0x33,
    '4': 0x34,
    '5': 0x35,
    '6': 0x36,
    '7': 0x37,
    '8': 0x38,
    '9': 0x39,
    'a': 0x41,
    'b': 0x42,
    'c': 0x43,
    'd': 0x44,
    'e': 0x45,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'i': 0x49,
    'j': 0x4A,
    'k': 0x4B,
    'l': 0x4C,
    'm': 0x4D,
    'n': 0x4E,
    'o': 0x4F,
    'p': 0x50,
    'q': 0x51,
    'r': 0x52,
    's': 0x53,
    't': 0x54,
    'u': 0x55,
    'v': 0x56,
    'w': 0x57,
    'x': 0x58,
    'y': 0x59,
    'z': 0x5A,
    'numpad_0': 0x60,
    'numpad_1': 0x61,
    'numpad_2': 0x62,
    'numpad_3': 0x63,
    'numpad_4': 0x64,
    'numpad_5': 0x65,
    'numpad_6': 0x66,
    'numpad_7': 0x67,
    'numpad_8': 0x68,
    'numpad_9': 0x69,
    'multiply_key': 0x6A,
    'add_key': 0x6B,
    'separator_key': 0x6C,
    'subtract_key': 0x6D,
    'decimal_key': 0x6E,
    'divide_key': 0x6F,
    'F1': 0x70,
    'F2': 0x71,
    'F3': 0x72,
    'F4': 0x73,
    'F5': 0x74,
    'F6': 0x75,
    'F7': 0x76,
    'F8': 0x77,
    'F9': 0x78,
    'F10': 0x79,
    'F11': 0x7A,
    'F12': 0x7B,
    'F13': 0x7C,
    'F14': 0x7D,
    'F15': 0x7E,
    'F16': 0x7F,
    'F17': 0x80,
    'F18': 0x81,
    'F19': 0x82,
    'F20': 0x83,
    'F21': 0x84,
    'F22': 0x85,
    'F23': 0x86,
    'F24': 0x87,
    'num_lock': 0x90,
    'scroll_lock': 0x91,
    'left_shift': 0xA0,
    'right_shift ': 0xA1,
    'left_control': 0xA2,
    'right_control': 0xA3,
    'left_menu': 0xA4,
    'right_menu': 0xA5,
    'browser_back': 0xA6,
    'browser_forward': 0xA7,
    'browser_refresh': 0xA8,
    'browser_stop': 0xA9,
    'browser_search': 0xAA,
    'browser_favorites': 0xAB,
    'browser_start_and_home': 0xAC,
    'volume_mute': 0xAD,
    'volume_Down': 0xAE,
    'volume_up': 0xAF,
    'next_track': 0xB0,
    'previous_track': 0xB1,
    'stop_media': 0xB2,
    'play/pause_media': 0xB3,
    'start_mail': 0xB4,
    'select_media': 0xB5,
    'start_application_1': 0xB6,
    'start_application_2': 0xB7,
    'attn_key': 0xF6,
    'crsel_key': 0xF7,
    'exsel_key': 0xF8,
    'play_key': 0xFA,
    'zoom_key': 0xFB,
    'clear_key': 0xFE,
    '+': 0xBB,
    ',': 0xBC,
    '-': 0xBD,
    '.': 0xBE,
    '/': 0xBF,
    '`': 0xC0,
    ';': 0xBA,
    '[': 0xDB,
    '\\': 0xDC,
    ']': 0xDD,
    "'": 0xDE
}


ULONG_PTR = POINTER(ULONG)

HOOKPROTYPE = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))


class POINT(Structure):
    """
    typedef struct tagPOINT {
        LONG x;
        LONG y;
    } POINT,POINTL,*PPOINT,*LPPOINT,*PPOINTL,*LPPOINTL;
    """
    _fields_ = [
        ('x', LONG),
        ('y', LONG)
    ]


class MSG(Structure):
    """
    typedef struct tagMSG {
        HWND   hwnd;
        UINT   message;
        WPARAM wParam;
        LPARAM lParam;
        DWORD  time;
        POINT  pt;
        DWORD  lPrivate;
    } MSG, *PMSG, *NPMSG, *LPMSG;
    """
    _fields_ = [
        ('hwnd', HWND),
        ('message', UINT),
        ('wParam', WPARAM),
        ('lParam', LPARAM),
        ('time', DWORD),
        ('pt', POINT),
        ('lPrivate', DWORD)
    ]


class KBDLLHOOKSTRUCT(Structure):
    """
    see https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-kbdllhookstruct
    typedef struct tagKBDLLHOOKSTRUCT {
        DWORD     vkCode;
        DWORD     scanCode;
        DWORD     flags;
        DWORD     time;
        ULONG_PTR dwExtraInfo;
    } KBDLLHOOKSTRUCT, *LPKBDLLHOOKSTRUCT, *PKBDLLHOOKSTRUCT;
    """
    _fields_ = [
        ('vkCode', DWORD),
        ('scanCode', DWORD),
        ('flags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ULONG_PTR)
    ]


class MSLLHOOKSTRUCT(Structure):
    """
    :see https://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-msllhookstruct
    typedef struct tagMSLLHOOKSTRUCT {
        POINT     pt;
        DWORD     mouseData;
        DWORD     flags;
        DWORD     time;
        ULONG_PTR dwExtraInfo;
    } MSLLHOOKSTRUCT, *LPMSLLHOOKSTRUCT, *PMSLLHOOKSTRUCT;
    """
    _fields_ = [
        ('pt', POINT),
        ('mouseData', DWORD),
        ('flags', DWORD),
        ('time', DWORD),
        ('dwExtraInfo', ULONG_PTR)
    ]


def get_screen_rect():
    return GetSystemMetrics(SM_CXSCREEN), GetSystemMetrics(SM_CYSCREEN)


def get_dpi():
    # 获取windows的缩方比例
    hdc = GetDC(0)
    dpi_a = GetDeviceCaps(hdc, DESKTOPHORZRES)/GetDeviceCaps(hdc, HORZRES)
    dpi_b = GetDeviceCaps(hdc, LOGPIXELSX)/0.96/100

    dpi = dpi_b if dpi_a == 1 else dpi_a
    print("get dpi", dpi_a, dpi_b)
    return dpi


def list_windows():
    def callback(hwnd, extra):
        process_id = DWORD(0)
        thread_id = GetWindowThreadProcessId(hwnd, LPDWORD(process_id))
        extra[hwnd] = {
            "handle": hwnd,
            "className": GetClassName(hwnd),
            "title": GetWindowText(hwnd),
            "processId": process_id.value,
            "threadId": thread_id
        }
    result = {}
    EnumWindows(callback, result)
    return result


class WindowsTool(object):

    __enable_debug = True
    __cur_mouse_move = False
    __cur_mouse_thread = None
    __cur_mouse_proc = []
    __keyboard_handle = None

    def __init__(self, name: str = None, hwnd: int = None):
        wins = list_windows()
        win = None
        if hwnd is not None and wins.keys().__contains__(hwnd):
            win = wins[hwnd]
            print("从窗口句柄获取窗口: ", win)
        elif name is not None:
            matched = list(filter(lambda x: x["title"] == name, wins.values()))
            if len(matched) > 0:
                win = matched[0]
            print("从窗口标题获取窗口: ", win)
        else:
            raise WindowsError("require parameter one of name or hwnd")
        if win is None:
            raise WindowsError("Window not found by %s or %s" % (name, hwnd))
        self.handle = win["handle"]
        self.className = win["className"]
        self.title = win["title"]
        self.process_id = win["processId"]
        self.thread_id = win["threadId"]
        print("选取窗口句柄", self.handle)
        # 获取窗口上下左右顶点坐标
        self.left, self.top, self.right, self.bottom = GetWindowRect(self.handle)
        # 计算窗口大小
        self.width, self.height = self.right - self.left, self.bottom - self.top
        # 定位鼠标相对坐标
        self.client_x, self.client_y = GetCursorPos()
        # 鼠标相对坐标对应的屏幕坐标
        self.mouse_x, self.mouse_y = ClientToScreen(self.handle, (self.client_x, self.client_y))
        # 获取分辨率缩放比
        self.dpi = get_dpi()
        # 获取桌面分辨率
        self.screen_x, self.screen_y = get_screen_rect()

    def __refresh_dpi(self):
        self.dpi = get_dpi()

    def enable_debug(self, enable=False):
        self.__enable_debug = enable

    def show_window(self):
        # 设置窗口位置
        # SetWindowPos(self.handle, None, 0, 0, self.width, self.height, SWP_SHOWWINDOW)
        # 设置窗口位于前台
        SetForegroundWindow(self.handle)

    def compute_mouse_screen_coordinate(self, x, y):
        return math.floor(x / self.screen_x * 65535), math.floor(y / self.screen_y * 65535)

    def pixel_to_screen_resolution(self, px, py):
        self.__refresh_dpi()
        return math.floor(px / self.dpi), math.floor(py / self.dpi)

    def screen_resolution_to_pixel(self, x, y):
        self.__refresh_dpi()
        return math.floor(x * self.dpi), math.floor(y * self.dpi)

    def compute_mouse(self):
        # 定位鼠标相对坐标
        self.client_x, self.client_y = GetCursorPos()
        # 鼠标相对坐标对应的屏幕坐标
        self.mouse_x, self.mouse_y = ClientToScreen(self.handle, (self.client_x, self.client_y))
        # if self.__enable_debug:
        # print("compute_mouse: client_x=%d, client_y=%d, mouse_x=%d, mouse_y=%d"
        #       % (self.client_x, self.client_y, self.mouse_x, self.mouse_y))

    def compute_window_rect(self):
        # 获取窗口上下左右顶点坐标
        self.left, self.top, self.right, self.bottom = GetWindowRect(self.handle)
        # 计算窗口大小
        self.width, self.height = self.right - self.left, self.bottom - self.top
        # print("compute_window_rect: left=%d, top=%d, right=%d, bottom=%d, width=%d, height=%d"
        #       % (self.left, self.top, self.right, self.bottom, self.width, self.height))

    def is_mouse_in_window(self):
        """判断鼠标是否在窗口"""
        self.compute_window_rect()
        self.compute_mouse()
        return self.left <= self.mouse_x <= self.right and self.top <= self.mouse_y <= self.bottom

    def is_window_active(self):
        """判断窗口是否激活。激活的窗口会获得焦点，可以执行输入操作。"""
        return self.handle == GetForegroundWindow()

    def get_window_center(self):
        """获取窗口中心坐标点"""
        self.compute_window_rect()
        return self.width / 2, self.height / 2

    def mouse_reset(self):
        """鼠标复位到窗口中心位置，该操作不会触发鼠标移动事件"""
        x, y = self.get_window_center()
        self.mouse_to(x, y)

    def mouse_reset_move(self, step=16, speed=1.00):
        """鼠标复位并移动到窗口中心位置，该操作会触发鼠标移动事件"""
        x, y = self.get_window_center()
        self.mouse_move_to(x, y, step=step, speed=speed)

    def mouse_to(self, x, y):
        """鼠标跳到指定位置，该操作不会触鼠标移动事件"""
        if self.is_window_active():
            SetCursorPos((int(self.left + x), int(self.top + y)))

    def __mouse_move_thread_proc(self):
        while self.__cur_mouse_move:
            if len(self.__cur_mouse_proc) > 0:
                mouse_move_proc = self.__cur_mouse_proc.pop()
                mouse_move_proc()
            else:
                time.sleep(0.100)
            """
            x0, y0 = self.__cur_mouse_x, self.__cur_mouse_y
            if self.__cur_mouse_move_x_step > 0:
                x0 += self.__cur_mouse_x_offset
            if self.__cur_mouse_move_y_step > 0:
                y0 += self.__cur_mouse_y_offset
            if (self.__cur_mouse_move_x_step > 0 or self.__cur_mouse_move_y_step > 0) and self.is_window_active():
                x, y = self.compute_mouse_screen_coordinate(x0, y0)
                mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x, y)
                if self.__cur_mouse_speed > 0.00:  # 如果定义了移动速度，则尝试模拟移动
                    time.sleep(0.001 * self.__cur_mouse_speed)
                else:
                    time.sleep(0.001)
                print("__mouse_move_thread_proc, (x0=%d, y0=%d), (x=%d, y=%d)" % (x0, y0, x, y), GetCursorPos())
            else:
                time.sleep(0.100)
            """

    def __mouse_move_thread_init(self):
        if self.__cur_mouse_thread is None:
            self.__cur_mouse_thread = threading.Thread(target=self.__mouse_move_thread_proc, name="mouse_move_thread")
        if not self.__cur_mouse_move:
            self.__cur_mouse_move = True
            self.__cur_mouse_thread.start()

    def mouse_move_to(self, x, y, step=1, speed=1.0):
        """
        鼠标移动到指定位置，该操作会触发鼠标移动事件
        :param x 移动点x坐标
        :param y 移动点y坐标
        :param step 步数，表示总让会触发的鼠标移动事件，默认为1次
        :param speed 速度，表示鼠标移动的速度，值大于0，越小越快，默认1.0

        # 计算x和y的相对位移
        x0, y0 = x - self.left - self.mouse_x, y - self.top - self.mouse_y
        self.__cur_mouse_x_offset += x0 / step
        self.__cur_mouse_y_offset += y0 / step
        self.__cur_mouse_move_x_step += step
        self.__cur_mouse_move_y_step -= step
        """
        def mouse_move_to_proc():
            self.compute_window_rect()
            self.compute_mouse()
            # 计算x和y的相对位移
            x0, y0 = self.mouse_x, self.mouse_y
            offset_x, offset_y = x + (self.left - self.mouse_x), y + (self.top - self.mouse_y)
            for i in range(0, step):
                if self.is_window_active():
                    x1, y1 = self.compute_mouse_screen_coordinate(self.mouse_x + offset_x * (i + 1) / step,
                                                                  self.mouse_y + offset_y * (i + 1) / step)
                    # cx0, cy0 = GetCursorPos()
                    mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x1, y1)
                    # cx1, cy1 = GetCursorPos()
                    if self.__enable_debug:
                        print("mouse_move_to, (x0=%d, y0=%d), (x=%d, y=%d), (x=%d, y=%d)"
                              % (x0, y0, x1, y1, offset_x, offset_y), GetCursorPos())
                if speed > 0.00:  # 如果定义了移动速度，则尝试模拟移动
                    time.sleep(0.001 * speed)
                else:
                    time.sleep(0.001)
        self.__cur_mouse_proc.append(mouse_move_to_proc)
        self.__mouse_move_thread_init()

    def mouse_move_offset(self, offset_x, offset_y, step=1, speed=1.0):
        """
        鼠标位移，该操作会触发鼠标移动事件
        """
        def mouse_move_offset_proc():
            self.compute_window_rect()
            self.compute_mouse()
            # 计算x和y的相对位移
            x0, y0 = self.mouse_x, self.mouse_y
            for i in range(0, step):
                if self.is_window_active():
                    x1, y1 = self.compute_mouse_screen_coordinate(self.mouse_x + offset_x * (i + 1) / step,
                                                                  self.mouse_y + offset_y * (i + 1) / step)
                    # cx0, cy0 = GetCursorPos()
                    mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, x1, y1)
                    # cx1, cy1 = GetCursorPos()
                    if self.__enable_debug:
                        print("mouse_move_offset, (x0=%d, y0=%d), (x=%d, y=%d), (x=%d, y=%d)"
                              % (x0, y0, x1, y1, offset_x, offset_y), GetCursorPos())
                if speed > 0.00:  # 如果定义了移动速度，则尝试模拟移动
                    time.sleep(0.001 * speed)
                else:
                    time.sleep(0.001)
        self.__cur_mouse_proc.append(mouse_move_offset_proc)
        self.__mouse_move_thread_init()

    def mouse_move_horizontal(self, offset, step=16, speed=1.00):
        """
        鼠标模向位移，该操作会触发鼠标移动事件
        """
        self.mouse_move_offset(offset, 0, step=step, speed=speed)

    def mouse_move_vertical(self, offset, step=16, speed=1.00):
        """
        鼠标纵向位移，该操作会触发鼠标移动事件
        """
        self.mouse_move_offset(0, offset, step=step, speed=speed)

    def mouse_left_click(self, duration=0.02):
        """鼠标左键单击，该操作会触发鼠标左击事件"""
        if self.is_window_active():
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(duration)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_right_click(self, duration=0.02):
        """鼠标右键单击，该操作会触发鼠标右击事件"""
        if self.is_window_active():
            mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            time.sleep(duration)
            mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

    def mouse_left_double_click(self, duration=0.02):
        """鼠标左键双击"""
        if self.is_window_active():
            self.mouse_left_click(duration=duration)
            time.sleep(duration)
            self.mouse_left_click(duration=duration)

    def mouse_right_double_click(self, duration=0.02):
        """鼠标右键双击"""
        if self.is_window_active():
            self.mouse_right_click(duration=duration)
            time.sleep(duration)
            self.mouse_right_click(duration=duration)

    def mouse_left_click_at(self, x, y, duration=0.02):
        """鼠标左键单击指定位置"""
        if self.is_window_active():
            self.mouse_to(x, y)
            self.mouse_left_click(duration=duration)

    def mouse_right_click_at(self, x, y, duration=0.02):
        """鼠标右键单击指定位置"""
        if self.is_window_active():
            self.mouse_to(x, y)
            self.mouse_right_click(duration=duration)

    def mouse_left_drag_to(self, x1, y1, x2, y2, duration=0.1):
        """鼠标左键拖拽至指定位置"""
        if self.is_window_active():
            self.mouse_move_to(x1, y1, speed=duration)
            mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            self.mouse_move_to(x2, y2, speed=duration)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_right_drag_to(self, x1, y1, x2, y2, duration=0.1):
        """鼠标右键拖拽至指定位置"""
        if self.is_window_active():
            self.mouse_move_to(x1, y1, speed=duration)
            mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
            self.mouse_move_to(x2, y2, speed=duration)
            mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def key_down(self, key):
        try:
            if self.is_window_active():
                keybd_event(VK_CODE[str(key)], MapVirtualKey(VK_CODE[str(key)], 0), 0, 0)
        except Exception as ex:
            print("key down  %s occur error." % key)
            print(ex)
            raise ex

    def key_up(self, key):
        try:
            if self.is_window_active():
                keybd_event(VK_CODE[str(key)], MapVirtualKey(VK_CODE[str(key)], 0), KEYEVENTF_KEYUP, 0)
        except Exception as ex:
            print("key up  %s occur error." % key)
            print(ex)
            raise ex

    def key_press(self, *key, duration=0.02):
        """模拟键盘"""
        for k in key:
            try:
                if self.is_window_active():
                    keybd_event(VK_CODE[str(k)], MapVirtualKey(VK_CODE[str(k)], 0), 0, 0)
                    time.sleep(duration)
                    keybd_event(VK_CODE[str(k)], MapVirtualKey(VK_CODE[str(k)], 0), KEYEVENTF_KEYUP, 0)
            except Exception as ex:
                print("key press  %s occur error." % k)
                print(ex)
                raise ex

    def add_keyboard_listen(self):
        def __keyboard_listener_proc(nCode, wParam, lParam):
            pKBDLLHOOKSTRUCT = POINTER(KBDLLHOOKSTRUCT)
            param = cast(lParam, pKBDLLHOOKSTRUCT)
            print("keyboard_listener_proc", nCode, param.contents.vkCode)
            # if nCode == HC_ACTION:
            return CallNextHookEx(self.__keyboard_handle, nCode, wParam, lParam)

        p_hook_type = HOOKPROTYPE(__keyboard_listener_proc)
        self.__keyboard_handle = SetWindowsHookEx(WH_KEYBOARD_LL, p_hook_type, 0, 0)
        if not self.__keyboard_handle:
            raise WindowsError("无法启动监听键盘程序")
        print("启动监听键盘程序, handle=%d" % self.__keyboard_handle)


    def remove_keyboard_listen(self):
        pass

    def screenshot(self, seat=None, save_path: str = None):
        """截屏"""
        if seat is None:
            self.__refresh_dpi()  # 刷新dpi
            seat = [
                self.left * self.dpi,
                self.top * self.dpi,
                (self.left + self.width) * self.dpi,
                (self.top + self.height) * self.dpi
            ]
            # seat = [0, 0, self.width * dpi, self.height * dpi]
            # print(seat)
        if self.is_window_active():
            if save_path is None:
                save_path = "images/screenshot_%d.png" % int(time.time()*1000)
            img = ImageGrab.grab(seat)
            img.save(save_path)
            return save_path
        else:
            return None





