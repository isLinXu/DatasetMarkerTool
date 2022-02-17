import re
import uuid
import requests
import os
import numpy
import imghdr
from PIL import Image

# 获取百度图片下载图片
def download_image(key_word, save_name, download_max):
    download_sum = 0
    # 把每个类别的图片存放在单独一个文件夹中
    save_path = 'images' + '/' + save_name
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    while download_sum < download_max:
        download_sum += 1
        str_pn = str(download_sum)
        # 定义百度图片的路径
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&' \
              'word=' + key_word + '&pn=' + str_pn + '&gsm=80&ct=&ic=0&lm=-1&width=0&height=0'
        try:
            s = requests.session()
            s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
            # 获取当前页面的源码
            result = s.get(url).content.decode('utf-8')
            # 获取当前页面的图片URL
            img_urls = re.findall('"objURL":"(.*?)",', result, re.S)
            if img_urls is None or len(img_urls) < 1:
                break
            # 开始下载图片
            for img_url in img_urls:
                # 获取图片内容
                img = requests.get(img_url, timeout=30)
                # 保存图片
                with open(save_path + '/' + str(uuid.uuid1()) + '.jpg', 'wb') as f:
                    f.write(img.content)
                print('正在下载 %s 的第 %d 张图片' % (key_word, download_sum))
                download_sum += 1
                # 下载次数超过指定值就停止下载
                if download_sum >= download_max:
                    break
        except Exception as e:
            print(e)
            continue
    print('下载完成')



