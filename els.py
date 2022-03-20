# 俄罗斯钓鱼脚本
import pyautogui
import win32api, win32con, win32gui
import time
import random
import cv2
import numpy
import baihe_map
import laoao_map
import els_config
from threading import Thread, Timer
import threading
from PIL import Image, ImageGrab
from colorsys import rgb_to_hsv
from skimage.measure import compare_ssim

class obj:
    lock = threading.Lock()  # 线程锁
    run_status = 0 # 锁，1.执行中，0.没有执行
    run_start = 0 # 是否放杆，0.放，1.不放
    jianpan_s = 0 # 键盘收的状态，1.执行中，0.没有执行
    yugan_lock = 0 # 鱼竿状态，0.没有放杆，1.已经放杆
    zhongyu_lock = 0 # 中鱼锁
    zouwei_status = 0 # 是否走位
    jietuimg = None # 截图数据
    jietuimg_v = 0 # 截图版本
    zhunbeihaole_img = None # 准备好了图片
    yangguang_img = None # 阳光图片
    canju_img = None # 餐具图片
    space_img = None # 空格图片
    kg_img = None # 千克图片
    mocha_num = 0 # 摩擦数
    mocha_arr = {} # 摩擦数
    map_status = 1 # 默认白河
    ganzi_key = 0 # 杆子id
    xy = None
    setting_type = 0 # 1.路亚。2.海竿、3.换图操作
    luya_paogan_num = 0 # 路亚抛竿

    run_jianpan = 0
    shift = 0
    xiegang = 0
    obj_arr = {
        'shangyu_num': 0,
        'ext_time': 0,
        'ganzi': 0
    }

    colors = dict((
        ((196, 2, 51), "RED"),  # 红
        ((255, 165, 0), "ORANGE"),  # 橙色
        ((255, 205, 0), "YELLOW"),  # 黄色
        ((0, 128, 0), "GREEN"),  # 绿色
        ((0, 0, 255), "BLUE"),  # 蓝色
        ((127, 0, 255), "VIOLET"),  # 紫色
        ((0, 0, 0), "BLACK"),  # 黑色
        ((255, 255, 255), "WHITE"),))  # 白色

    # 获取句柄
    def get_window_pos(self,name):
        # 获取句柄
        handle = win32gui.FindWindow(None, name)
        # handle = 67650
        return win32gui.GetWindowRect(handle), handle

    def callback(self,x):
        print(x)

    def to_hsv(self, color):
        return rgb_to_hsv(*[x / 255.0 for x in color])  # rgb_to_hsv wants floats!

    def color_dist(self,c1, c2):
        return sum((a - b) ** 2 for a, b in zip(self.to_hsv(c1), self.to_hsv(c2)))

    def min_color_diff(self, color_to_match, colors):
        return min((self.color_dist(color_to_match, test), colors[test])for test in colors)

    """
        判断是否存在字典中
    """
    def class_dict(self, name):
        if name is None:
            print('不存在的字符串',name)
            return 0
        if name is not self.obj_arr.keys():
            print('没有字符串,赋值为0',name)
            self.obj_arr[name] = 0
        return self.obj_arr[name]

    """
        键盘弹起
    """
    def jianpanup(self):
        temp_arr = [els_config.keyboard_right, els_config.keyboard_shift, els_config.keyboard_left]
        # print('初始化所有键位，弹起操作')
        for v in temp_arr:
            pyautogui.keyUp(v)
        self.print('初始化所有键位，弹起操作完毕')
        pass

    """
        摩擦设置
    """
    def mocha_init(self,i):
        i = int(i)
        if i not in self.mocha_arr.keys():
            self.mocha_arr[i] = 0
        if self.mocha_arr[i] == 0:
            return False
        self.print('正在重置摩擦{}'.format(self.mocha_arr[i]))
        if self.mocha_arr[i] > 0:
            if self.mocha_arr[i] == 9 and random.randint(1, 10) > 5:
                self.mocha_arr[i] = 8 # 有概率缩小一下摩擦
            # 需要减下来
            pyautogui.keyDown('alt')
            for v in range(self.mocha_arr[i]):
                pyautogui.press('-')
                time.sleep(1)
            pyautogui.keyUp('alt')
        else:
            # 需要加上去
            pyautogui.keyDown('alt')
            for v in range(abs(self.mocha_arr[i])):
                pyautogui.press('+')
                time.sleep(1)
            pyautogui.keyUp('plus')
            pass
        self.mocha_arr[i] = 0
        pass

    # 图片提取信息
    def img_analysis(self):
        img_file = "../img_els_file/1647242994.2881403.jpg"
        # img_file = "../img_els_file/1645169699.jpg"

        img = Image.open(img_file)  # 打开图像
        # img = img_data
        box = (529, 354, 592, 385)
        roi = img.crop(box)
        data = numpy.asarray(roi)

        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'error_img' not in self.__dict__.keys():
            self.print('打开准备好图像')
            img = Image.open('els_duibi_img/error_.jpg')  # 打开图像
            self.error_img = numpy.asarray(img)
        (score, diff) = compare_ssim(binary, self.error_img, full=True)
        if score >= 0.8:
            # print('准备好抛竿',score)
            return True
        image = Image.fromarray(data)
        # image.save('els_duibi_img/space.jpg','JPEG')
        image.show()
        exit()
        pass

    """
        解析数据，判断是否中鱼
    """
    def img_analysis_zhongyu(self, img_data):
        img = img_data
        box = (985, 725, 1183, 750)
        roi = img.crop(box)
        # 截取图片
        data = numpy.asarray(roi)
        # 图片二值化
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'zhongyu_img' not in self.__dict__.keys():
            self.print('打开中鱼图像')
            img_ = Image.open('els_duibi_img/zhongyu.jpg')  # 打开图像
            self.zhongyu_img = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.zhongyu_img, full=True)
        if score > 0.8:
            print("中鱼", score)
            pass
            return True

    """
        解析数据，中鱼进度
    """
    def img_analysis_jindu(self, img_data):
        img = img_data

        # box = (855, 735, 883, 766)
        # roi = img.crop(box)
        # data = numpy.asarray(roi)
        # gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        # ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # if 'kg_img' not in self.__dict__.keys():
        #     print('打开杆准备好图像 kg')
        #     img_ = Image.open('els_duibi_img/kg.jpg')  # 打开图像
        #     self.kg_img = numpy.asarray(img_)
        # (score, diff) = compare_ssim(binary, self.kg_img, full=True)
        # if score < 0.8:
        #     # print('未看到杆子')
        #     return None

        box = (420, 774, 886, 784)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        html = ""
        color_arr = {
            'h': 0,  # 红色
            'q': 0,  # 青色
            'c': 0,  # 橙色
            'o': 0,  # 其他颜色
        }

        for v in data:
            for v1 in v:
                (r, g, b) = v1
                temp_data = self.min_color_diff(v1, self.colors)
                if temp_data[1] == 'YELLOW':
                    color_arr['q'] += 1
                if temp_data[1] == 'ORANGE':
                    color_arr['h'] += 1
                if temp_data[1] == 'GREEN':
                    color_arr['q'] += 1
        return color_arr

    """
        解析数据，判断是否需要吃饭
    """
    def img_analysis_chifan(self, img_data):
        img = img_data
        box = (165, 705, 192, 729)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if self.canju_img is None:
            self.print('打开餐具图像')
            img_ = Image.open('els_duibi_img/chanju.jpg')  # 打开图像
            self.canju_img = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.canju_img, full=True)
        if score < 0.8:
            self.print('未在主页')
            return False

        box = (193, 710, 252, 722)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        color_len = 0
        # 最多1491个
        red_len = 0
        for v in data:
            for v1 in v:
                temp_data = self.min_color_diff(v1, self.colors)
                if temp_data[1] == 'YELLOW':
                    color_len += 1
                if temp_data[1] == 'ORANGE':
                    red_len += 1
                    color_len += 1
                if temp_data[1] == 'GREEN':
                    color_len += 1
        if color_len < 450 or red_len > 100:
            self.print('需要吃饭')
            return True
        return False

    """
            解析数据，判断是否需要加力量
    """
    def img_analysis_liliang(self, img_data):
        img = img_data
        # img = img_data
        box = (165, 675, 192, 700)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'liliang' not in self.__dict__.keys():
            self.print('打开力量图像')
            img_ = Image.open('els_duibi_img/liliang.jpg')  # 打开图像
            self.liliang = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.liliang, full=True)
        if score < 0.8:
            self.print('未在主页')
            return False

        box = (193, 678, 282, 692)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        color_len = 0
        # 最多1491个
        red_len = 0
        for v in data:
            for v1 in v:
                temp_data = self.min_color_diff(v1, self.colors)
                if temp_data[1] == 'YELLOW':
                    color_len += 1
                if temp_data[1] == 'ORANGE':
                    red_len += 1
                    color_len += 1
                if temp_data[1] == 'GREEN':
                    color_len += 1
        if color_len < 800 or red_len > 100:
            self.print('需要喝水加力量 {}'.format(color_len))
            return True
        return False

    """
        解析数据，判断是否需要喝水
    """
    def img_analysis_heshui(self, img_data):
        img = img_data
        box = (165, 766, 192, 790)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if self.yangguang_img is None:
            self.print('打开阳光图像')
            img_ = Image.open('els_duibi_img/yangguang.jpg')  # 打开图像
            self.yangguang_img = numpy.asarray(img_)
        # if self.yangguang_img is None:
        #     print('打开阳光图像')
        #     img_ = Image.open('els_duibi_img/yangguang.jpg')  # 打开图像
        #     self.yangguang_img = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.yangguang_img, full=True)
        if score < 0.8:
            self.print('未在主页')
            return False
        box = (193, 772, 252, 784)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        color_len = 0
        # 最多494个
        red_len = 0
        for v in data:
            for v1 in v:
                temp_data = self.min_color_diff(v1, self.colors)
                if temp_data[1] == 'YELLOW':
                    color_len += 1
                if temp_data[1] == 'ORANGE':
                    red_len += 1
                    color_len += 1
                if temp_data[1] == 'GREEN':
                    color_len += 1
        if color_len < 450 or red_len > 100:
            self.print('需要喝水')
            return True
        return False

    """
        解析数据，判断是否需要放杆
    """
    def img_analysis_paogan(self, img_data):
        img = img_data
        box = (379, 744, 552, 765)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if self.zhunbeihaole_img is None:
            self.print('打开准备好图像')
            img = Image.open('els_duibi_img/zhunbeihaole.jpg')  # 打开图像
            self.zhunbeihaole_img = numpy.asarray(img)
        (score, diff) = compare_ssim(binary, self.zhunbeihaole_img, full=True)
        if score >= 0.8:
            # print('准备好抛竿',score)
            return True
        return False

    """
        未准备好，需要添加饵
    """
    def img_analysis_weizhunbei(self, img_data):
        img = img_data
        box = (379, 744, 552, 765)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'weizhuzhuang_img' not in self.__dict__.keys():
            self.print('打开未准备好图像')
            img = Image.open('els_duibi_img/weizhuzhuang.jpg')  # 打开图像
            self.weizhuzhuang_img = numpy.asarray(img)
        (score, diff) = compare_ssim(binary, self.weizhuzhuang_img, full=True)
        if score >= 0.8:
            # print('未准备好抛竿',score)
            return True
        return False

    """
        解析数据，判断是否需要收鱼
    """
    def img_analysis_shouyu(self, img_data):
        img = img_data
        box = (449, 744, 552, 765)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if self.space_img is None:
            self.print('打开空格图像')
            img = Image.open('els_duibi_img/space.jpg')  # 打开图像
            self.space_img = numpy.asarray(img)

        (score, diff) = compare_ssim(binary, self.space_img, full=True)
        if score >= 0.8:
            print('准备好收鱼', score)
            return True
        return False

    """
        执行吃饭喝水操作
    """
    def run_other(self):
        print('启动吃饭喝水线程')
        v = self.jietuimg_v
        while True:
            # 判断版本是否被操作过，如果操作过，则不能执行
            if v == self.jietuimg_v:
                continue
            if self.jietuimg is None:
                continue
            v = self.jietuimg_v
            time_sleep = random.randint(20, 40)
            self.obj_arr['ext_time'] = int(time.time())+time_sleep
            time.sleep(time_sleep)
            res = self.img_analysis_heshui(self.jietuimg)
            if res is True:
                # 执行喝水
                self.print('正在执行喝水操作')
                pyautogui.press(els_config.heshui_key)
                pass
            # time.sleep(random.randint(10, 100))
            res = self.img_analysis_chifan(self.jietuimg)
            if res is True:
                # 执行吃饭
                self.print('正在执行吃饭操作')
                pyautogui.press(els_config.chifan_key)
                pass
            pass
            res = self.img_analysis_liliang(self.jietuimg)
            if res is True:
                # 执行吃饭
                self.print('正在执行喝水操作')
                pyautogui.press(els_config.heshui_key)
                pass
            pass
            res = self.is_error()
            if res is True:
                self.print('正在执行错误提示框操作')
                time.sleep(1)
                win32api.SetCursorPos((self.xy[0] + 700, self.xy[1] + 450))
                time.sleep(1)
                pyautogui.click()

        pass

    """
        执行放杆收杆操作，路亚
    """
    def run_fanggan(self):
        self.print('启动路亚线程')
        v = self.jietuimg_v
        i = 0
        i_right = 0

        while True:
            # 判断版本是否被操作过，如果操作过，则不能执行
            if v == self.jietuimg_v:
                continue
            if self.jietuimg is None:
                continue
            if self.map_status != 1:
                time.sleep(1)
                continue
            v = self.jietuimg_v
            if self.run_status != 0:
                continue
            if self.setting_type == 3:
                tm_min = time.localtime().tm_min
                if tm_min >= els_config.laoao_start_m:
                    # 去老奥
                    continue
            self.lock.acquire()
            pyautogui.press('1')
            self.run_status = 1
            time.sleep(0.3)
            res = self.img_analysis_weizhunbei(self.jietuimg)
            if res is True:
                # 需要换饵
                self.jianpanup()
                self.print('正在换饵')
                time.sleep(1)
                baihe_map.baihe_map().huaner(self.xy)
                self.print('换饵完成')
            res = self.img_analysis_paogan(self.jietuimg)
            self.ganzi_key = 1
            i += 1
            self.luya_paogan_num += 1
            if res is True:
                self.print('进入抛竿环节')
                # 可以执行抛竿
                # 几杆未中，需要换个位置
                if self.obj_arr['ganzi'] != 0 and self.obj_arr['ganzi'] % 3 == 0 and (self.zouwei_status == 1 or els_config.luya_zouwei_status == 1):
                    # 位移
                    if 'weiyi_' not in self.__dict__.keys():
                        self.weiyi_ = 0
                    pyautogui.press(els_config.keyboard_shift)
                    if self.weiyi_ == 0:
                        rand_key_int = random.randint(4, 10)
                        self.print('正在向左移动{}格'.format(rand_key_int))
                        # 往左
                        pyautogui.keyDown('a')
                        time.sleep(rand_key_int)
                        pyautogui.keyUp('a')
                        pyautogui.keyDown('w')
                        time.sleep(3)
                        pyautogui.keyUp('w')
                        self.weiyi_ = rand_key_int
                        pass
                    else:
                        # 往右
                        self.print('正在向右移动{}格'.format(self.weiyi_))
                        pyautogui.keyDown('d')
                        time.sleep(self.weiyi_)
                        pyautogui.keyUp('d')
                        pyautogui.keyDown('w')
                        time.sleep(3)
                        pyautogui.keyUp('w')
                        self.weiyi_ = 0
                        pass
                    pass
                self.luya_paogan_num = 0
                self.zhongyu_lock = 0
                # if random.randint(1, 10) <= 2:
                #     random_int = random.randint(10, 20)
                #     self.print('命中20%，停止放杆，停止{}秒'.format(random_int))
                #     time.sleep(random_int)
                #     self.run_status = 0
                #     try:
                #         self.lock.release()
                #     except BaseException as e:
                #         print("错误信息：",e)
                #     continue
                self.mocha_init('1') # 重置摩擦
                self.run_jianpan = 0
                self.jianpanup()
                self.print('正在进行抛竿动作')
                if self.jianpan_s == 1:
                    # 需要先弹起
                    pyautogui.keyUp(els_config.keyboard_left)
                    time.sleep(0.2)
                pyautogui.keyUp(els_config.keyboard_shift)
                pyautogui.press(els_config.keyboard_shift)
                self.shift = 0
                time.sleep(0.2)
                pyautogui.keyUp(els_config.keyboard_right)
                pyautogui.press(els_config.keyboard_right)
                self.xiegang = 0

                pyautogui.keyDown(els_config.keyboard_shift)
                pyautogui.keyDown(els_config.keyboard_left)
                time.sleep(0.5)
                pyautogui.keyUp(els_config.keyboard_left)
                pyautogui.keyUp(els_config.keyboard_shift)
                time.sleep(random.uniform(2, 3))
                pyautogui.keyDown(els_config.keyboard_left)
                # time.sleep(0.3)
                # pyautogui.keyUp(els_config.keyboard_left)
                self.jianpan_s = 1
                self.obj_arr['ganzi'] += 1
                self.print('抛竿动作完成')
                self.yugan_lock = 1
                self.run_status = 0
                i_right = 0

                try:
                    self.lock.release()
                except BaseException as e:
                    pass
                    # print("错误信息：", e)
                continue
                pass
            elif self.luya_paogan_num > 6 and self.is_fanggan(): # 在首页
                self.yugan_lock = 1
                i_right += 1
                pyautogui.keyDown(els_config.keyboard_left)
                if i % 100 == 0 and i != 0: # 每100秒重置一下键盘
                    pyautogui.press(els_config.keyboard_left)
                    pyautogui.keyUp(els_config.keyboard_left)
                    time.sleep(0.5)
                    pyautogui.keyDown(els_config.keyboard_left)
                if i_right >= 120: # 强制提竿
                    i_right = 0
                    pyautogui.keyDown(els_config.keyboard_right)
            try:
                self.lock.release()
            except BaseException as e:
                pass
                # print("错误信息：", e)
            self.run_status = 0
            # 判断是否点击，没有则直接按下
            if self.jianpan_s == 0:
                pyautogui.keyDown(els_config.keyboard_left)
                # 需要先弹起
                self.jianpan_s = 1
                time.sleep(0.3)
            # if self.jianpan_s == 0 and self.run_status == 0:
                # 需要先弹起
                # pyautogui.keyDown(els_config.keyboard_left)
                # self.jianpan_s = 1
        pass

    """
        海杆
    """
    def run_haigan(self):
        print('啓動海竿進程')
        arr = els_config.haigan_key
        v = self.jietuimg_v
        while True:
            if v == self.jietuimg_v:
                continue
            if self.jietuimg is None:
                continue
            if self.run_status != 0:
                continue
            if self.map_status != 2:
                time.sleep(1)
                continue
            if self.setting_type == 3:
                tm_min = time.localtime().tm_min
                if tm_min >= els_config.baihe_start_m and tm_min < els_config.laoao_start_m:
                    # 去白河
                    continue
            v = self.jietuimg_v
            time.sleep(0.3)
            self.run_status = 1
            self.lock.acquire()
            for v in arr:
                if self.map_status != 2:
                    continue
                self.print('操作{}杆子'.format(v))
                self.zhongyu_lock = 0 # 重置数据
                self.ganzi_key = int(v)
                pyautogui.press(els_config.keyboard_left)
                pyautogui.press(els_config.keyboard_right)
                pyautogui.press(els_config.keyboard_shift)
                time.sleep(0.5)
                # 提起
                pyautogui.press(v)
                self.yugan_lock = 1
                # 点击一次
                pyautogui.press(els_config.keyboard_left)
                time.sleep(10)
                paogan = 0
                while True:
                    # 沒有中魚
                    if self.zhongyu_lock == 0:
                        break
                    # pyautogui.keyDown(els_config.keyboard_left)
                    # 判斷是否已經準備好
                    paogan = 1
                    res = self.img_analysis_paogan(self.jietuimg)
                    if res is True:
                        break
                    # pyautogui.press(els_config.keyboard_left)
                time.sleep(1)
                res = self.img_analysis_paogan(self.jietuimg)
                if paogan == 1 or self.zhongyu_lock == 1 or res is True:
                    # 加入窝子再放杆
                    if els_config.haigan_wozi_status == 1 and self.img_analysis_paogan(self.jietuimg) is True:
                        self.jianpanup()
                        time.sleep(0.5)
                        laoao_map.laoao_map().wozi(self.xy)
                        while True:
                            time.sleep(2)
                            res = self.img_analysis_paogan(self.jietuimg)
                            shouye = self.is_shouye()
                            if shouye is True or res is True:
                                break
                            self.print('杆子未准备好')
                            pyautogui.press('esc')
                    # 需要放杆
                    self.jianpanup()
                    time.sleep(0.5)
                    pyautogui.keyDown(els_config.keyboard_left)
                    time.sleep(1)
                    pyautogui.keyDown(els_config.keyboard_shift)
                    time.sleep(1)
                    pyautogui.keyUp(els_config.keyboard_left)
                    time.sleep(0.3)
                    pyautogui.keyUp(els_config.keyboard_shift)
                    time.sleep(random.uniform(3, 4))
                    pyautogui.press(els_config.keyboard_left)
                    time.sleep(0.5)
                    print('完成状态',paogan)
                self.yugan_lock = 0
                self.mocha_init(v) # 重置摩擦
                pyautogui.press('0')
                self.zhongyu_lock = 0
            if self.map_status != 2:
                time.sleep(1)
                continue
            pass
            try:
                self.lock.release()
            except BaseException as e:
                pass
            time.sleep(1)
            pyautogui.press('0')
            time.sleep(1)
            self.print('往左边走')
            pyautogui.keyDown('a')
            time_sleep_ttl = (len(els_config.haigan_key)-1) * 0.2 # 3根的量
            time.sleep(time_sleep_ttl)
            pyautogui.keyUp('a')
            self.run_status = 0
            time_s = random.randint(20, 40)
            self.print("等待{}秒".format(time_s))
            time.sleep(time_s)
        pass

    """
        收鱼线程
    """
    def run_shouyu(self):
        self.print('启动收鱼线程')
        v = self.jietuimg_v
        while True:
            # 判断版本是否被操作过，如果操作过，则不能执行
            if v == self.jietuimg_v:
                continue
            if self.jietuimg is None:
                continue
            v = self.jietuimg_v
            time.sleep(0.3)
            res = self.img_analysis_shouyu(self.jietuimg)
            if res is True:
                self.luya_paogan_num = 0
                self.yugan_lock = 0
                # 执行收鱼动作
                self.print('正在进行收鱼动作')
                pyautogui.keyUp(els_config.keyboard_shift)
                pyautogui.press(els_config.keyboard_shift)
                self.shift = 0
                time.sleep(0.3)
                pyautogui.keyUp(els_config.keyboard_right)
                pyautogui.press(els_config.keyboard_right)
                self.xiegang = 0
                self.jianpanup()
                time.sleep(1)

                pyautogui.press('space')
                # time.sleep(0.3)
                # pyautogui.keyUp('space')
                self.print('收鱼动作完成')
                self.obj_arr['ganzi'] = 0
                self.obj_arr['shangyu_num'] += 1
                # self.zhongyu_lock = 0
                self.yugan_lock = 0
                time.sleep(4)

                try:
                    self.lock.release()
                except BaseException as e:
                    # print("错误信息：", e)
                    pass
        pass

    # 展示信息
    def print(self, data):
        pass
        if self.obj_arr['ext_time'] == 0:
            print(data)
            return False
        time_ttl = self.obj_arr['ext_time'] - int(time.time())
        str = "已有{}杆未中鱼，剩余{}秒判定喝水吃饭".format(self.obj_arr['ganzi'], time_ttl)
        print(data, str)

    """
        执行中鱼操作
    """
    def run_zhongyu(self):
        print('启动中鱼线程')
        v = self.jietuimg_v
        zhongyu_num = 0
        while True:
            # 判断版本是否被操作过，如果操作过，则不能执行
            if v == self.jietuimg_v:
                continue
            if self.jietuimg is None:
                continue
            if self.yugan_lock == 0:
                continue
            v = self.jietuimg_v
            time.sleep(0.2)
            if self.zhongyu_lock != 0:
                res = self.img_analysis_jindu(self.jietuimg)
                if res is not None:
                    try:
                        self.lock.release()
                    except BaseException as e:
                        pass
                    zhongyu_num += 1
                    if zhongyu_num >= 15 and zhongyu_num % 2 == 0:
                        if self.ganzi_key not in self.mocha_arr.keys():
                            self.mocha_arr[self.ganzi_key] = 0
                        # 可以進入增加或減少摩擦操作
                        if res['h'] > 4350:
                            self.mocha_arr[self.ganzi_key] -= 1
                            pyautogui.keyDown('alt')
                            pyautogui.keyDown('-')
                            time.sleep(0.5)
                            pyautogui.keyUp('-')
                            pyautogui.keyUp('alt')
                        else:
                            if self.mocha_arr[self.ganzi_key] < 9 and res['q'] > 1300:
                                self.mocha_arr[self.ganzi_key] += 1
                                pyautogui.keyDown('alt')
                                pyautogui.keyDown('+')
                                time.sleep(0.5)
                                pyautogui.keyUp('+')
                                pyautogui.keyUp('alt')
                    if zhongyu_num >= 60 and (zhongyu_num % 8 == 3 or zhongyu_num % 8 == 0) and zhongyu_num % 20 <= 3:
                        # 打开空格
                        pyautogui.press('space')
                        pass
                    print('中鱼进度', res)
                continue
            time.sleep(1)
            pyautogui.press('r')
            # pyautogui.press('r')
            time.sleep(0.3)
            res = self.img_analysis_zhongyu(self.jietuimg)
            if res is True and self.yugan_lock == 1:
                zhongyu_num = 0
                # 执行拖鱼动作
                pyautogui.press(els_config.keyboard_shift)
                pyautogui.press(els_config.keyboard_right)
                time.sleep(0.3)

                pyautogui.keyDown(els_config.keyboard_left)
                self.zhongyu_lock = 1
                self.print('正在进行中鱼动作')
                pyautogui.keyDown(els_config.keyboard_shift)
                if self.shift == 0:
                    self.shift = 1
                time.sleep(0.5)
                pyautogui.keyDown(els_config.keyboard_right)
                if self.xiegang == 0:
                    self.xiegang = 1
                continue
                pass
            else:
                pass
                # 没中鱼，收起
                # if self.shift == 1:
                #     pyautogui.keyUp(els_config.keyboard_shift)
                #     self.shift = 0
                # time.sleep(0.3)
                # if self.xiegang == 1:
                #     pyautogui.keyUp(els_config.keyboard_right)
                #     self.xiegang = 0
        pass

    """
        判断是否在首页
    """
    def is_shouye(self):
        if self.jietuimg is None:
            return False
        box = (165, 766, 192, 790)
        img = self.jietuimg
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if self.yangguang_img is None:
            print('打开阳光图像')
            img_ = Image.open('els_duibi_img/yangguang.jpg')  # 打开图像
            self.yangguang_img = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.yangguang_img, full=True)
        if score < 0.8:
            self.print('不在首页')
            return False
        self.print('在首页')
        return True

    """
            判断是否已经放杆
    """
    def is_fanggan(self):
        if self.jietuimg is None:
            return False
        img = self.jietuimg
        box = (855, 735, 883, 766)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'kg_img' not in self.__dict__.keys():
            self.print('打开杆准备好图像 kg')
            img_ = Image.open('els_duibi_img/kg.jpg')  # 打开图像
            self.kg_img = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.kg_img, full=True)
        if score < 0.8:
            # print('未看到杆子')
            return False
        return True

    """
        判断是否在设置页面
    """
    def is_setting(self):
        if self.jietuimg is None:
            return False
        box = (1065, 275, 1162, 370)
        img = self.jietuimg
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'help_img' not in self.__dict__.keys():
            self.print('打开帮助图像')
            img_ = Image.open('els_duibi_img/help.jpg')  # 打开图像
            self.help_img = numpy.asarray(img_)
        (score, diff) = compare_ssim(binary, self.help_img, full=True)
        if score < 0.8:
            self.print('未在设置页面')
            return False
        self.print('在设置页面')
        return True

    """
        判断错误
    """
    def is_error(self):
        if self.jietuimg is None:
            return False
        img = self.jietuimg
        box = (529, 354, 592, 385)
        roi = img.crop(box)
        data = numpy.asarray(roi)
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        if 'error_img' not in self.__dict__.keys():
            self.print('打开错误图像')
            img = Image.open('els_duibi_img/error_.jpg')  # 打开图像
            self.error_img = numpy.asarray(img)
        (score, diff) = compare_ssim(binary, self.error_img, full=True)
        if score >= 0.8:
            return True
        return False

    """
        执行换图操作
    """
    def run_time(self):
        print('启动换图操作')
        v = self.jietuimg_v
        while True:
            if v == self.jietuimg_v:
                continue
            if self.jietuimg is None:
                continue
            v = self.jietuimg_v
            time.sleep(0.2)
            if self.run_status != 0:
                continue
            time.sleep(1)
            # self.print('能否换图')
            self.lock.acquire()
            self.run_status = 1
            tm_min = time.localtime().tm_min
            if (tm_min >= els_config.laoao_start_m or tm_min < els_config.laoao_end_m) and self.map_status == 1:
            # if True and self.map_status == 1:
                self.yugan_lock = 0
                self.jianpanup()
                time.sleep(1)
                self.print('换图去老奥')
                # 去老奥
                self.map_status = 2
                pyautogui.press('esc')
                while True:
                    time.sleep(1)
                    res = self.is_setting()
                    if res is True:
                        break
                    time.sleep(1)
                    pyautogui.press('esc')

                time.sleep(5)
                win32api.SetCursorPos((self.xy[0] + 750, self.xy[1] + 300))
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                win32api.SetCursorPos((self.xy[0] + 330, self.xy[1] + 700))
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                win32api.SetCursorPos((self.xy[0] + 880, self.xy[1] + 520))
                time.sleep(1)
                pyautogui.click()
                self.jianpanup()
                time.sleep(1)
                while True:
                    if self.is_shouye() is True:
                        self.print('在首页')
                        break
                    time.sleep(1)
                    pyautogui.click() # 继续点击鼠标现有的地方
                time.sleep(1)
                laoao_map.laoao_map().run(self.xy)
                self.yugan_lock = 1
            if tm_min >= els_config.baihe_start_m and tm_min < els_config.baihe_end_m and self.map_status == 2:
            # if True and self.map_status == 2:
                self.yugan_lock = 0
                self.jianpanup()
                time.sleep(1)
                self.print('换图去白河')
                # 去白河
                self.map_status = 1
                pyautogui.press('esc')
                while True:
                    time.sleep(1)
                    res = self.is_setting()
                    if res is True:
                        break
                    time.sleep(1)
                    pyautogui.press('esc')
                time.sleep(5)
                win32api.SetCursorPos((self.xy[0] + 750, self.xy[1] + 300))
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                win32api.SetCursorPos((self.xy[0] + 1230, self.xy[1] + 700))
                time.sleep(1)
                pyautogui.click()
                time.sleep(1)
                win32api.SetCursorPos((self.xy[0] + 880, self.xy[1] + 520))
                time.sleep(1)
                pyautogui.click()
                self.jianpanup()
                time.sleep(1)
                while True:
                    if self.is_shouye() is True:
                        break
                    time.sleep(1)
                    pyautogui.click()  # 继续点击鼠标现有的地方
                time.sleep(1)
                baihe_map.baihe_map().run(self.xy)
                self.yugan_lock = 1
                self.run_status = 0
            self.run_status = 0
            try:
                self.lock.release()
            except BaseException as e:
                print("错误信息：", e)
            # time.sleep(630)
            pass
        pass

    """
        操作截图
    """
    def jietu(self):
        # self.jietuimg = ImageGrab.grab((x1, y1, x2, y2))
        # self.jietuimg_v = time.time()
        pass

    """
        执行命令
    """
    def run(self):
        pass
        # self.img_analysis()
        # exit()
        # run_jianpan = Thread(target=self.jianpan)
        # run_shubiao = Thread(target=self.jiantingshubiao)
        # run_jianpan.start()
        # run_shubiao.start()
        # """
        run_other = Thread(target=self.run_other) # 吃饭喝水
        run_zhongyu = Thread(target=self.run_zhongyu) # 中鱼动作
        run_shouyu = Thread(target=self.run_shouyu) # 收鱼动作
        run_other.start()
        run_zhongyu.start()
        run_shouyu.start()

        type = input("路线：1.路亚，2.海竿，3.换图操作:")
        if str(type) == '1':
            zouwei = input("是否走位，1.是，2，不是：")
            if str(zouwei) == '1':
                self.zouwei_status = 1
            else:
                self.zouwei_status = 0
            run_fanggan = Thread(target=self.run_fanggan)  # 路亚
            run_fanggan.start()
            self.map_status = 1
            self.setting_type = 1
        if str(type) == '2':
            run_haigan = Thread(target=self.run_haigan)  # 海竿r
            run_haigan.start()
            self.setting_type = 2
            self.map_status = 2
        if str(type) == '3':
            self.setting_type = 3
            run_time = Thread(target=self.run_time)  # 换图
            run_time.start()
            run_fanggan = Thread(target=self.run_fanggan)  # 路亚
            run_fanggan.start()
            run_haigan = Thread(target=self.run_haigan)  # 海竿r
            run_haigan.start()
            self.map_status = 1
# """
        self.jianpanup() # 弹起所有键
        (x1, y1, x2, y2), handle = self.get_window_pos('Russian Fishing 4')
        win32gui.SetForegroundWindow(handle)
        self.xy = (x1, y1, x2, y2)
        arr = [
            'dianwei_7348', 'dianwei_7263'
        ]
        # baihe_map.baihe_map().huaner(self.xy)
        # exit()
        # win32api.SetCursorPos((self.xy[0]+700, self.xy[1]+450))
        # exit()
        while True:
            # print("shift键：",self.shift,'斜杠：',self.xiegang,'点：',self.jianpan_s)
            time.sleep(0.3)
            self.jietuimg_v = time.time()
            self.jietuimg = ImageGrab.grab((x1, y1, x2, y2))
            # self.jietuimg.save('../img_els_file/{}.jpg'.format(time.time()),'JPEG')
            # exit()


if __name__ == '__main__':
    obj().run()

