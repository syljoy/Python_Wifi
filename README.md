# Python_Wifi
暴力破解WiFi密码。

## 目录

- [环境](#环境)
- [使用说明](#使用说明)



## 环境

软件：PyCharm 2021.2 (Community Edition)

运行环境：

```
python==3.7.10
tqdm==4.61.2
pywifi==1.1.12
```



## 使用说明



1. 下载密码本，或者自己生成密码本。（可在[Weakpass](https://weakpass.com/)下载）

2. 直接修改```Crack_Wifi.py```或者```Crack_Wifi_tqdm.py```文件的```wifi_name```的值，修改为待破解WiFi的SSID。

3. 运行```Crack_Wifi.py```或者```Crack_Wifi_tqdm.py```文件

   ```python Crack_Wifi.py```

   注：```tqdm```是Python进度条库。

