import pyautogui
import time
import win32api, win32con, win32gui
import random
import els_config

# 老奥地图
class laoao_map:

    # 窝子
    def wozi(self,data):
        time.sleep(1)
        pyautogui.press('v')
        time.sleep(1)
        win32api.SetCursorPos((data[0]+850, data[1]+430))
        time.sleep(0.5)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -22)
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, -22)
        time.sleep(0.5)
        win32api.SetCursorPos((data[0]+850, data[3]-80))
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.3)
        win32api.SetCursorPos((data[0]+200, data[1]+200))
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        win32api.SetCursorPos((data[0]+540, data[3]-80))
        time.sleep(0.3)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.press('esc')

        pass

    # 走路
    def run(self, data):
        # exit()
        print('进入操作老奥')
        print(data)
        # exit()
        time.sleep(10)
        pyautogui.keyDown('shift')
        pyautogui.keyDown('a')
        time.sleep(0.3)
        pyautogui.keyUp('a')

        pyautogui.keyDown('w')
        time.sleep(5)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -700, 0)
        time.sleep(12)
        # win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -100, 80)
        time.sleep(9)
        pyautogui.keyUp('w')
        pyautogui.keyUp('shift')

        time.sleep(1)
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 300, 0)

        pyautogui.keyDown('s')
        time.sleep(0.5)
        pyautogui.keyUp('s')

        pyautogui.keyDown('d')
        time.sleep(0.5)
        pyautogui.keyUp('d')
        time.sleep(1)
        for v in els_config.haigan_key:
            print('放第{}杆'.format(v))
            pyautogui.press(v)
            time.sleep(1)
            pyautogui.keyDown(els_config.keyboard_left)
            time.sleep(1)
            pyautogui.keyDown(els_config.keyboard_shift)
            time.sleep(1)
            pyautogui.keyUp(els_config.keyboard_left)
            time.sleep(0.3)
            pyautogui.keyUp(els_config.keyboard_shift)
            time.sleep(random.uniform(2, 3))
            pyautogui.press(els_config.keyboard_left)
            pyautogui.press('0')
            time.sleep(0.5)
            pyautogui.keyDown('d')
            time.sleep(0.2)
            pyautogui.keyUp('d')
            time.sleep(1)

        time.sleep(0.5)
        pyautogui.keyDown('a')
        time.sleep(0.3)
        pyautogui.keyUp('a')
        print('放杆完成')
        pass
    pass


if __name__ == '__main__':
    pass