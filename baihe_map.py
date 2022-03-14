import pyautogui
import time
import win32api, win32con, win32gui
import els_config
import random

# 白河地图
class baihe_map:
    def run(self, data):
        time.sleep(10)
        print('进入操作白河')
        print(data)
        # exit()
        pyautogui.press('d')
        pyautogui.press('d')
        time.sleep(1)
        pyautogui.press('e')
        time.sleep(10)
        win32api.SetCursorPos((data[0]+150, data[1]+300))
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        win32api.SetCursorPos((data[0]+150, data[1]+430))
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)
        win32api.SetCursorPos((data[0]+1250, data[1]+80)) # 关闭
        time.sleep(1)
        pyautogui.click()
        pyautogui.click()
        pyautogui.click()

        time.sleep(1)
        arr = [
            'dianwei_7348', 'dianwei_7263'
        ]
        self.__getattribute__(random.choice(arr))()
        # self.dianwei_7348()
        pyautogui.press(els_config.luya_key)
        # pyautogui.dragRel(0, 200, duration=0.25)
        # while True:
        #     print(pyautogui.position())
        #     time.sleep(1)
        pass
    pass

    # 换饵动作
    def huaner(self,data):
        time.sleep(1)
        pyautogui.press('v')
        time.sleep(1)
        win32api.SetCursorPos((data[0]+850, data[1]+680))
        time.sleep(1)
        pyautogui.click()
        time.sleep(2)
        win32api.SetCursorPos((data[0]+200, data[1]+200))
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        win32api.SetCursorPos((data[0] + 540, data[3] - 80))
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.press('esc')
        pass

    def dianwei_7348(self):
        print('进入73:48')
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1200, 0)
        pyautogui.keyDown('shift')
        pyautogui.keyDown('w')
        time.sleep(3)
        pyautogui.keyUp('w')
        pyautogui.keyUp('shift')
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 200, 0)
        pyautogui.keyDown('d')
        time.sleep(4)
        pyautogui.keyUp('d')


        pass

    def dianwei_7263(self):
        print('进入72:63')
        pyautogui.keyDown('shift')
        pyautogui.keyDown('d')
        time.sleep(2)
        pyautogui.keyUp('d')

        pyautogui.keyDown('s')
        time.sleep(2)
        pyautogui.keyDown('d')
        time.sleep(5)
        pyautogui.keyUp('d')
        time.sleep(9)
        pyautogui.keyUp('s')
        pyautogui.keyUp('shift')
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -1000, 0)
        time.sleep(2)
        pass

if __name__ == '__main__':
    pass