
import win32process
import win32con
import win32api
import ctypes
import win32gui

class process():

    # 获取句柄
    def get_window_pos(self, name):
        # 获取句柄
        handle = win32gui.FindWindow(None, name)
        # handle = 67650
        return win32gui.GetWindowRect(handle), handle

    def run(self):
        pid = ctypes.c_ulong()
        (x1, y1, x2, y2), handle = self.get_window_pos('Russian Fishing 4')
        print(pid)

        kernel32 = ctypes.windll.LoadLibrary("kernel32.dll")
        # print(dir(kernel32))


        hProcess = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, False, pid)
        addr = ctypes.c_ulong()
        kernel32.ReadProcessMemory(int(hProcess), 0xD0DF1C, ctypes.byref(addr), 4, None)
        win32api.CloseHandle(hProcess)
        print(addr.value)
        # return addr.value

        pass
    pass

if __name__ == '__main__':
    process().run()