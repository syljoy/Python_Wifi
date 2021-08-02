# -*- coding: utf-8 -*-
#
# @Time    : 2021-08-02 11:55:31
# @Author  : Yunlong Shi
# @Email   : syljoy@163.com
# @FileName: test.py.py
# @Software: PyCharm
# @Github    ：https://github.com/syljoy

import pywifi
import time
from pywifi import const


def check_state():
    # 常见一个无线对象
    wifi = pywifi.PyWiFi()
    # 取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 显卡名称
    print(ifaces.name())
    if ifaces.status() == 4:
        print('电脑已连接无线')
    else:
        print('电脑未连接无线')
    if ifaces.status() in [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]:
        print('电脑未连接无线')
    else:
        print('电脑已连接无线')



AKMS = {
    const.AKM_TYPE_NONE: 'AKM_TYPE_NONE',
    const.AKM_TYPE_WPA: 'AKM_TYPE_WPA',
    const.AKM_TYPE_WPAPSK: 'AKM_TYPE_WPAPSK',
    const.AKM_TYPE_WPA2: 'AKM_TYPE_WPA2',
    const.AKM_TYPE_WPA2PSK: 'AKM_TYPE_WPA2PSK',
    const.AKM_TYPE_UNKNOWN: 'AKM_TYPE_UNKNOWN',
}
def get_wireless():
    # 常见一个无线对象
    wifi = pywifi.PyWiFi()
    # 取第一个无线网卡
    ifaces = wifi.interfaces()[0]
    # 扫描AP
    ifaces.scan()
    time.sleep(1)

    wireless = ifaces.scan_results()
    print(wireless)
    for data in wireless:
        print(data.ssid)
        print(AKMS[data.akm[0]])


def test_connected():
    pass


if __name__ == '__main__':
    print(const.IFACE_DISCONNECTED, const.AKM_TYPE_NONE)
    check_state()
    get_wireless()

