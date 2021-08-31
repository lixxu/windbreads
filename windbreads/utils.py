#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import os.path
import pickle
import platform
import subprocess
import sys
from functools import partial

try:
    import chardet
except ImportError:
    pass

import six

import windbreads.common_i18n as common_i18n

NEW_LINE = bytes(os.linesep, "utf-8") if six.PY3 else os.linesep


def detect_encoding(text):
    return chardet.detect(text)


def get_app_dir():
    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    fs_encoding = sys.getfilesystemencoding()
    if not isinstance(app_dir, six.text_type):
        app_dir = app_dir.decode(fs_encoding)

    return app_dir


def get_startupinfo():
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return si


def call_cmd(args):
    """Run 'command' windowless and waits until finished."""
    return subprocess.Popen(args, startupinfo=get_startupinfo()).wait()


def run_cmd(cmd):
    subprocess.call(cmd, startupinfo=get_startupinfo())


def update_t(self, lang=None, zh=None, en=None):
    czh = common_i18n.zh.copy()
    if zh:
        czh.update(zh)

    cen = common_i18n.en.copy()
    if en:
        cen.update(en)

    self.t = partial(tt, lang=lang, po=dict(zh=czh, en=cen))


def tt(text, lang=None, po={}):
    if lang:
        mo = po.get(lang, {})
        if mo:
            if text in mo:
                return mo[text]

            return mo.get(text.lower(), text)

    return text


def ttt(text, t=None):
    """Try Translate Text."""
    return t(text) if t else text


def get_lang_list(names=["en", "zh"]):
    return [get_lang_name(lang) for lang in names]


def get_lang_name(lang):
    if lang == "zh":
        return "Chinese - 简体中文"
    else:
        return "English"


def get_lang_key(name):
    if "Chinese" in name or "Simplied" in name:
        return "zh"

    return "en"


def get_copy_right(text=None):
    return text if text else "(C) Jabil Shanghai TE Support"


def get_platform_info():
    return "{} ({})\n- {}".format(
        platform.platform(), platform.machine(), platform.processor()
    )


def dump_pickle(data, pk_file, silent=True):
    try:
        with open(pk_file, "wb") as f:
            pickle.dump(data, f, protocol=2)

    except Exception:
        if not silent:
            raise


def load_pickle(pk_file, silent=True, **kwargs):
    try:
        with open(pk_file, "rb") as f:
            return pickle.load(f, **kwargs)

    except Exception:
        if silent:
            return {}

        raise


def make_shortcut(lnk_path, target, w_dir, icon=None):
    from win32com.client import Dispatch

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(lnk_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = w_dir
    if not icon:
        icon = target

    shortcut.IconLocation = icon
    shortcut.save()


def get_users_startup_folders():
    release = platform.release()
    if release in ("7", "8", "10"):
        subs = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    elif release in ("XP", "2003Server"):
        subs = r"Start Menu\Programs\Startup"
    else:
        return []

    root_folder = os.path.dirname(os.environ["USERPROFILE"])
    users = [
        fd
        for fd in os.listdir(root_folder)
        if os.path.isdir(os.path.join(root_folder, fd))
    ]
    return [os.path.join(root_folder, user, subs) for user in users]


def get_startup_folder(all_user=False):
    release = platform.release()
    if release in ("7", "8", "10"):  # win7, win2008, ...
        return get_win7_startup(all_user)
    elif release == "XP":
        return get_xp_startup(all_user)
    elif release == "2003Server":
        return get_win2k3_startup(all_user)
    else:
        return "Not implemented"


def get_xp_startup(all_user=False):
    folder = os.environ["ALLUSERSPROFILE" if all_user else "USERPROFILE"]
    return os.path.join(folder, "Start Menu", "Programs", "Startup")


def get_win7_startup(all_user=False):
    if all_user:
        folder = os.environ["ALLUSERSPROFILE"]
        subs = r"Microsoft\Windows\Start Menu\Programs\Startup"
    else:
        folder = os.environ["USERPROFILE"]
        subs = r"AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

    return os.path.join(folder, subs)


def get_win2k3_startup(all_user=False):
    return get_xp_startup(all_user)


def get_processes(name=None, attrs=["pid", "name"]):
    processes = []
    try:
        import psutil
    except ImportError:
        return processes

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=attrs)
        except psutil.NoSuchProcess:
            pass
        else:
            if name:
                if pinfo["name"] == name:
                    processes.append(pinfo)

                continue

            processes.append(pinfo)

    return processes
