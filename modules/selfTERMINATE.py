import os
import winreg as reg
from winreg import *


def run(*args):
    pth2win = "C:\\WINDOWS\\windowsSysdll.exe"
    key = HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
    open1 = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
    try:
        reg.DeleteValue(open1,"systemdll")
    except:
        pass
    try:
        os.remove(pth2win)
    except:
        pass
    reg.CloseKey(open1)
    return "removed"
