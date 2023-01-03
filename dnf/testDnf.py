import os, sys, time, random, datetime
import threading


from game_tools import WindowsTool

"""
# 找到窗口: 地下城与勇士
tool = WindowsTool(name="地下城与勇士")
# 显示宫
tool.show_window()
# 等待窗口显示
time.sleep(1)
# 打开拍卖行
tool.key_press("b")                          # 拍卖行快键是b
tool.key_press("backspace", duration=2)      # 按住退格键2秒
# 搜索物品 (建议切换到五笔输入法)
tool.key_press("a", "k", "g", "f", "1")      # akgf 1 堇
tool.key_press("g", "e", "f", "1")           # gef 1 青
tool.key_press("d", "g", "t", "g", "space")  # dgtg 石
tool.key_press("enter")
time.sleep(1)
# 载图
tool.screenshot()
"""


class DnfTool(object):

    __name: str = "地下城与勇士"
    __game: WindowsTool = None

    def __init__(self):
        self.__game = WindowsTool(name="地下城与勇士")
        if self.__game is None:
            raise WindowsError("未找到游戏窗口: %s" % self.__name)
        self.__game.add_keyboard_listen()


dnf = DnfTool()
print(dnf)




