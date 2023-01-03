import os, sys, time, random, datetime
import threading

import threadpool

from game_tools import WindowsTool


def fire(game, times=1, interval=0.01):

    for i in range(0, times):
        if game.is_mouse_in_window():
            game.mouse_left_click()
        time.sleep(interval)


def special_fire(game, times=1, interval=0.01):
    for i in range(0, times):
        if game.is_mouse_in_window():
            game.mouse_right_click()
        time.sleep(interval)


def move_left(game, duration=1.0):
    if game.is_mouse_in_window():
        game.key_press("a", duration=duration)


def move_right(game, duration=1.0):
    if game.is_mouse_in_window():
        game.key_press("d", duration=duration)


def move_front(game, duration=1.0):
    if game.is_mouse_in_window():
        game.key_press("w", duration=duration)


def move_back(game, duration=1.0):
    if game.is_mouse_in_window():
        game.key_press("s", duration=duration)


def switch_weapon(game):
    if game.is_mouse_in_window():
        game.key_press("q")


def do_action():
    # 找到窗口: 逆战
    game = WindowsTool(name="逆战")
    # 显示宫
    game.show_window()
    # 等待窗口显示
    time.sleep(1)
    # 移动鼠标
    # start = time.time()
    # game.mouse_move_to(0, 0)
    # stop = time.time()
    # print(start, stop, stop - start)
    # win.mouse_left_drag_to(100, 100, 300, 300)
    #move_left(game, duration=1.00)
    game.mouse_reset()
    time.sleep(0.2)

    def m():
        move_left(game, duration=1.00)
        move_front(game, duration=1.00)
        move_right(game, duration=1.00)
        move_back(game, duration=1.00)

    def f():
        fire(game, times=6, interval=1)
        time.sleep(1)
        game.key_press('q')

    def h():
        if game.is_mouse_in_window():
            game.mouse_move_horizontal(10, speed=1.0)
            game.mouse_reset()  # 鼠标重置位置
            time.sleep(1)
            game.mouse_move_horizontal(-10, speed=1.0)
            time.sleep(1)

    def mm():
        game.mouse_reset()
        x, y = game.get_window_center()
        game.mouse_move_to(x + 100, y, step=16)
        time.sleep(1)
        # game.mouse_reset()
        # x, y = game.get_window_center()
        game.mouse_move_to(x - 100, y, step=16)
        time.sleep(1)

    def v():
        if game.is_mouse_in_window():
            game.mouse_move_vertical(5, speed=1.00)
            time.sleep(1)
            game.mouse_move_vertical(-2, speed=1.00)

    t_f = threading.Thread(target=f)
    t_m = threading.Thread(target=m)
    t_h = threading.Thread(target=h)
    t_v = threading.Thread(target=v)

    # t_f.start()
    # t_m.start()
    # t_h.start()
    # mm()
    h()
    f()
    # t_v.start()
    # game.mouse_reset()
    #game.mouse_reset()
    #game.mouse_move_horizontal(distance=-1)
    #move_front(game, duration=1.00)
    #game.mouse_move_horizontal(distance=-200, speed=0.1)
    #move_right(game, duration=1.00)
    #game.mouse_move_horizontal(distance=200, speed=0.1)
    #move_back(game, duration=1.00)
    #game.mouse_move_horizontal(distance=-200, speed=0.1)
    #fire(game, times=100, interval=0.02)


do_action()