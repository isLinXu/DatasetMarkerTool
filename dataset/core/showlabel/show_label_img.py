# -*- coding:utf-8 -*-

"""
@ Author: LinXu
@ Contact: 17746071609@163.com
@ Date: 2022/01/13 下午19:29
@ Software: PyCharm
@ File: show_label_img.py
@ Desc: 读取xml文件信息画在原图上进行显示并保存结果
"""

import xml.dom.minidom
from xml.dom import minidom

import cv2
import os

from tqdm import tqdm


class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        # 十六进制格式颜色
        hex = ('FF3838', 'FF9D97', 'FF701F', 'FFB21D', 'CFD231', '48F90A', '92CC17', '3DDB86', '1A9334', '00D4BB',
               '2C99A8', '00C2FF', '344593', '6473FF', '0018EC', '8438FF', '520085', 'CB38FF', 'FF95C8', 'FF37C7')
        self.palette = [self.hex2rgb('#' + c) for c in hex]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        # 返回对应颜色
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        # 16进制的颜色格式转为RGB格式
        return tuple(int(h[1 + i:1 + i + 2], 16) for i in (0, 2, 4))


colors = Colors()  # create instance for 'from utils.plots import colors'


def show_label_from_images(xml_path, jpg_path, root_path, is_show=False):
    '''
    将xml的框体信息与label名称在原图进行绘制
    :param xml_path:
    :param jpg_path:
    :param root_path:
    :param is_show:
    :return:
    '''
    # 根据路径获取图片列表
    xmlfilelist = os.listdir(xml_path)
    jpgfilelist = os.listdir(jpg_path)

    # 对文件列表名称进行排序
    jpgfilelist.sort(reverse=False)
    xmlfilelist.sort(reverse=False)
    print(len(jpgfilelist))
    print('xml_list', xmlfilelist)
    print('jpg_list', jpgfilelist)
    for i in tqdm(range(0, len(xmlfilelist))):
        # 读取文件名
        xmlfilename = os.path.splitext(xmlfilelist[i])[0]
        jpgfilename = os.path.splitext(jpgfilelist[i])[0]
        # 读取所有xml文件
        xml_path = root_path + 'Annotations/' + xmlfilename + '.xml'
        # 读取所有图片文件
        jpg_path = root_path + 'JPEGImages/' + jpgfilename + ".jpg"

        # 解析json格式的xml文件
        file = minidom.parse(xml_path)
        fname = file.getElementsByTagName('filename')
        sname = fname[0].firstChild.data

        objkt = file.getElementsByTagName('name')
        objec = [i.firstChild.data for i in objkt]

        # 根据名称匹配结果
        if xmlfilename == jpgfilename:
            print(xmlfilename + '.xml', jpgfilename + ',jpg')
            dom = xml.dom.minidom.parse(xml_path)
            name = dom.getElementsByTagName('name')
            print('name', name, 'sname', sname)
            xleft = dom.getElementsByTagName('xmin')
            xright = dom.getElementsByTagName('xmax')
            ytop = dom.getElementsByTagName('ymin')
            ybutton = dom.getElementsByTagName('ymax')

            # 计算所有label的个数
            label_num = len(xleft)
            print('lable_num:', label_num)

            img = cv2.imread(jpg_path)
            for i in range(label_num):
                x_left = xleft[i].firstChild.data
                x_right = xright[i].firstChild.data
                y_top = ytop[i].firstChild.data
                y_button = ybutton[i].firstChild.data
                # 设置rectangle左上角、右下角坐标
                start_point = (int(x_left), int(y_top))
                end_point = (int(x_right), int(y_button))
                # 计算字体位置坐标
                org = (int(int(x_left) - 20), int(int(y_top) - 20))
                # 设置颜色
                color = colors(i, True)
                print('boxx', x_left, y_top, x_right, y_button)

                # 标签名称
                label_name = objec[i]

                # 设置字体格式
                font = cv2.FONT_HERSHEY_SIMPLEX
                # 设置字体参数
                fontscale = 1

                thickness = 2

                # 将bbox的参数以rectangle的形式画在原图上
                cv2.rectangle(img, start_point, end_point, (0, 255, 0), thickness)
                # xml中的标签名称以Text的形式画在原图上
                image = cv2.putText(img, label_name, org, font, fontscale, color, thickness, cv2.LINE_AA)

                # 保存结果
                cv2.imwrite(root_path + "output/" + jpgfilename + '.jpg', img)
                if is_show:
                    cv2.imshow("img", image)
                    cv2.waitKey()


def show_label_from_img(xml_path, jpg_path, root_path, is_show=False):
    '''
    将xml的框体信息与label名称在原图进行绘制
    :param xml_path:
    :param jpg_path:
    :param root_path:
    :param is_show:
    :return:
    '''

    # 读取文件名
    xmlfilename = os.path.splitext(xml_path)[0]
    jpgfilename = os.path.splitext(jpg_path)[0]
    print('xmlfilename', xmlfilename)
    # 读取所有xml文件
    # xml_path = root_path + 'Annotations/' + xmlfilename + '.xml'
    # 读取所有图片文件
    # jpg_path = root_path + 'JPEGImages/' + jpgfilename + ".jpg"

    # 解析json格式的xml文件
    file = minidom.parse(xml_path)
    fname = file.getElementsByTagName('filename')
    sname = fname[0].firstChild.data

    objkt = file.getElementsByTagName('name')
    objec = [i.firstChild.data for i in objkt]

    # 根据名称匹配结果
    print(xmlfilename + '.xml', jpgfilename + ',jpg')
    dom = xml.dom.minidom.parse(xml_path)
    name = dom.getElementsByTagName('name')
    print('name', name, 'sname', sname)
    xleft = dom.getElementsByTagName('xmin')
    xright = dom.getElementsByTagName('xmax')
    ytop = dom.getElementsByTagName('ymin')
    ybutton = dom.getElementsByTagName('ymax')

    # 计算所有label的个数
    label_num = len(xleft)
    print('lable_num:', label_num)

    img = cv2.imread(jpg_path)
    for i in range(label_num):
        x_left = xleft[i].firstChild.data
        x_right = xright[i].firstChild.data
        y_top = ytop[i].firstChild.data
        y_button = ybutton[i].firstChild.data
        # 设置rectangle左上角、右下角坐标
        start_point = (int(x_left), int(y_top))
        end_point = (int(x_right), int(y_button))
        # 计算字体位置坐标
        org = (int(int(x_left) - 20), int(int(y_top) - 20))
        # 设置颜色
        color = colors(i, True)
        print('boxx', x_left, y_top, x_right, y_button)

        # 标签名称
        label_name = objec[i]

        # 设置字体格式
        font = cv2.FONT_HERSHEY_SIMPLEX
        # 设置字体参数
        fontscale = 1

        thickness = 2

        # 将bbox的参数以rectangle的形式画在原图上
        cv2.rectangle(img, start_point, end_point, (0, 255, 0), thickness)
        # xml中的标签名称以Text的形式画在原图上
        image = cv2.putText(img, label_name, org, font, fontscale, color, thickness, cv2.LINE_AA)

        # 保存结果
        cv2.imwrite(root_path + "output/" + jpgfilename + '.jpg', img)
        if is_show:
            cv2.imshow("img", image)
            cv2.waitKey()


if __name__ == '__main__':
    '''
    usage:传入xml_path,jpg_path,root_path
    目录结构参考：
    |-root/
    |--root/Annotations
    |--root/JPEGImages
    '''
    # xml_path = "/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_lineextract_detect/VOC2007/Annotations/"  # windows系统用双斜线
    # jpg_path = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_lineextract_detect/VOC2007/JPEGImages/'
    # root_path = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_lineextract_detect/VOC2007/'
    # is_show = True
    # show_label_from_images(xml_path=xml_path, jpg_path=jpg_path, root_path=root_path,is_show=is_show)
    '''
    usage:传入xml_path,jpg_path,root_path
    目录结构参考：
    |-root/
    |--root/Annotations/017.xml"
    |--root/JPEGImages/017.jpg
    '''
    file_name = '017'
    xml_path = "/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_lineextract_detect/VOC2007/Annotations/" + file_name + ".xml"  # windows系统用双斜线
    jpg_path = "/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_lineextract_detect/VOC2007/JPEGImages/" + file_name + ".jpg"
    root_path = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_lineextract_detect/VOC2007/'
    is_show = True
    show_label_from_img(xml_path=xml_path, jpg_path=jpg_path, root_path=root_path, is_show=is_show)
