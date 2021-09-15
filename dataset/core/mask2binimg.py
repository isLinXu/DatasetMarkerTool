'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-08-21 上午11:54
@desc: 将多通道mask图像批量转换为单通道二值化图像并存放到指定位置
'''
import cv2
import numpy as np
import os

from utils.fileHelper import os_mkdir


def mask2binimg(path,show=False):
    for root, dirs, files in os.walk(path):
        print('################################################################')
        for name in files:
            # 遍历label生成的{x}_json目录
            if len(dirs) == 0:
                # print('root', root)
                # 字符分割,得到label排序序号
                filepath = os.path.split(root)[0]
                numname = os.path.split(root)[1]
                n_name = numname.replace('_json','')

                # 处理原图img
                if name == 'img.png':
                    fname = os.path.join(root, name)
                    print('INFO[img]', fname)
                    img = cv2.imread(fname)
                    img_dst = cv2.resize(img, (640, 480))
                    # img = cv2.resize(img, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_NEAREST)
                    if show:
                        cv2.imshow('img', img)
                        cv2.waitKey()
                    # 根据指定路径存取二值化图片
                    img_path = filepath + '/imgs/'
                    os_mkdir(img_path)
                    cv2.imwrite(img_path + str(n_name) + '.png', img_dst)

                # 处理label标签图
                if name == 'label.png':
                    fname = os.path.join(root, name)
                    print('INFO[label]', fname)
                    label = cv2.imread(fname)
                    label = cv2.resize(label, (640, 480))
                    gray = cv2.cvtColor(label, cv2.COLOR_BGR2GRAY)
                    retVal, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
                    # 显示图片
                    if show:
                        cv2.imshow('label', label)
                        cv2.imshow('dst', dst)
                        if cv2.waitKey(1) & 0xff == ord("q"):
                            break
                    # 根据指定路径存取二值化图片
                    mask_path = filepath + '/masks/'
                    os_mkdir(mask_path)
                    cv2.imwrite(mask_path + str(n_name) + '.png', dst)

        print('当前图片转换完成...')
    pass

if __name__ == '__main__':
    # path = '/home/hxzh02/文档/defectDetect/金属锈蚀(复件)/test'
    # path = '/home/hxzh02/文档/defectDetect/金属锈蚀(复件)'
    # path = '/home/hxzh02/下载/flow_dataset/image/'
    path = '/home/hxzh02/下载/PPLTA航拍输电线路数据集/data_original_size'
    mask2binimg(path,False)

