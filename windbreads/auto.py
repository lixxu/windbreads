#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import ctypes
import win32gui
import win32con
import win32process
import win32com.client

FS_CODING = sys.getfilesystemencoding()
EnumWindows = ctypes.windll.user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int,
                                     ctypes.POINTER(ctypes.c_int))
GetWindowText = ctypes.windll.user32.GetWindowTextW
GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
IsWindowVisible = ctypes.windll.user32.IsWindowVisible


def get_child(parent=0, child=None, cls_name=None, window_name=None):
    return win32gui.FindWindowEx(parent, child, cls_name, window_name)


def get_text(hwnd, safe=True, safe_text=None):
    try:
        buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH,
                                            0, 0)
        buf = win32gui.PyMakeBuffer(buf_size)
        win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buf)
        return buf[:buf_size - 1]
    except:
        if safe:
            return safe_text
        else:
            raise


def compare_text(src, dst, rule='=', re_rule=None):
    if rule == 'startswith':
        return src.startswith(dst)
    elif rule == 'endswith':
        return src.endswith(dst)
    elif rule == 're':
        return re_rule.match(src)
    else:
        return src == dst


def check_pid(hwnd, pid):
    if pid in win32process.GetWindowThreadProcessId(hwnd):
        bring_foreground(hwnd)


def show_window_by_pid(pid):
    return win32gui.EnumWindows(check_pid, pid)


def bring_foreground(hwnd):
    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


def find_handler2(dst, max_try=10000, rule='=', re_rule=None, debug=False):
    hwnd = get_child()
    i = 0
    while i <= max_try:
        i += 1
        text = get_text(hwnd)
        if text is not None:
            text = text.decode(FS_CODING)

        if debug:
            print(type(text), text)

        if text and compare_text(text, dst, rule, re_rule):
            return hwnd

        hwnd = get_child(child=hwnd)

    return None


def find_handler(dst, rule='=', re_rule=None, debug=False):
    handlers = []

    def foreach_window(hwnd, l_param):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            if compare_text(buff.value, dst, rule, re_rule):
                handlers.append(hwnd)

        return True

    EnumWindows(EnumWindowsProc(foreach_window), 0)
    return handlers[0] if handlers else None


def is_visible(hwnd):
    return win32gui.IsWindowVisible(hwnd)


def press_button(hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)


def close_window(hwnd, force=False):
    if force or is_visible(hwnd):
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)


def get_foreground_window():
    return win32gui.GetForegroundWindow()


def get_window_text(hwnd):
    return win32gui.GetWindowText(hwnd)


def get_window_pos_and_size(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]
    return x, y, rect[2] - x, rect[3] - y


def move_to(hwnd, x, y, w, h, repaint=True):
    win32gui.MoveWindow(hwnd, x, y, w, h, repaint)


def send_text(hwnd, text, enter=True):
    win32gui.SendMessage(hwnd, win32con.WM_SETTEXT, None, '{}'.format(text))
    if enter:
        win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
