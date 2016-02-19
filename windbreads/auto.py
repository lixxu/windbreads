#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import win32gui
import win32con


FS_CODING = sys.getfilesystemencoding()


def get_child(parent=0, child=None, cls_name=None, window_name=None):
    return win32gui.FindWindowEx(parent, child, cls_name, window_name)


def get_text(hwnd):
    buf_size = 1 + win32gui.SendMessage(hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
    buf = win32gui.PyMakeBuffer(buf_size)
    win32gui.SendMessage(hwnd, win32con.WM_GETTEXT, buf_size, buf)
    return buf[:buf_size - 1]


def compare_text(src, dst, rule='=', re_rule=None):
    if rule == 'startswith':
        return src.startswith(dst)
    elif rule == 'endswith':
        return src.endswith(dst)
    elif rule == 're':
        return re_rule.match(src)
    else:
        return src == dst


def find_handler(dst, max_try=10000, rule='=', re_rule=None, debug=False):
    hwnd = get_child()
    i = 0
    while i <= max_try:
        i += 1
        text = get_text(hwnd).decode(FS_CODING)
        if debug:
            print(type(text), text)

        if text and compare_text(text, dst, rule, re_rule):
            return hwnd

        hwnd = get_child(child=hwnd)

    return None


def is_visible(hwnd):
    return win32gui.IsWindowVisible(hwnd)


def press_button(hwnd):
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)


def close_window(hwnd, force=False):
    if force or is_visible(hwnd):
        win32gui.SendMessage(hwnd, win32con.WM_CLOSE, 0, 0)
