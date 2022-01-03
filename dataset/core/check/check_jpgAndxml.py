# -*- coding:utf-8 -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-11-01 上午11:56
@desc: 检查jpeg图片与标注文件是否对应
'''
import os

from tqdm import *


def checkJpgXml(jpeg_dir, annot_dir,if_clear = False):
    """
    dir1 是图片所在文件夹
    dir2 是标注文件所在文件夹
    """
    cnt = 0
    xnt = 0
    error_FILE_list = []
    error_XML_list = []
    jpeg_dir_list = os.listdir(jpeg_dir)
    xml_dir_list = os.listdir(annot_dir)

    for i in tqdm(range(0, len(jpeg_dir_list))):
        # ---------------------------------------------------#
        #   根据JPEG名称在Annotations中寻找对应的XML文件
        # ---------------------------------------------------#
        jpeg_file = jpeg_dir_list[i]
        f_name, f_ext = jpeg_file.split(".")
        # print('f_name', f_name, ',f_ext', f_ext)
        # ---------------------------------------------------#
        #   检查统计对应文件
        # ---------------------------------------------------#
        if not os.path.exists(os.path.join(annot_dir, f_name + ".xml")):
            error_FILE_list.append(f_name)
            cnt += 1

    for i in tqdm(range(0, len(xml_dir_list))):
        # ---------------------------------------------------#
        #   根据XML名称在JPEGImages中寻找对应的JPEG文件
        # ---------------------------------------------------#
        xml_file = xml_dir_list[i]
        # print('xml_file',xml_file)
        x_name, x_ext = xml_file.split(".")
        # print('f_name', f_name, ',f_ext', f_ext)
        # ---------------------------------------------------#
        #   检查统计对应文件
         # ---------------------------------------------------#
        JPGxml = os.path.join(jpeg_dir, x_name + ".JPG")
        # JPEGxml = os.path.join(jpeg_dir, x_name + ".JPEG")
        jpgxml = os.path.join(jpeg_dir, x_name + ".jpg")
        # print('File', JPEGxml,JPGxml,jpgxml)
        if not os.path.exists(JPGxml) and not os.path.exists(jpgxml):
            error_XML_list.append(x_name)
            print('JPG',JPGxml)
            xnt += 1

    # ---------------------------------------------------#
    #   整理xml信息
    # ---------------------------------------------------#
    print("=====检查完毕=====")
    # print('xnt',xnt)
    if cnt > 0 or xnt > 0:
        print("有%d个文件不符合要求。" % (cnt))
        errorfile_list = sorted(error_FILE_list)
        errorXml_list = sorted(error_XML_list)
        for jpeg_error in errorfile_list:
            # print('errorJPGFile:', jpeg_error)
            errorJPGFile = jpeg_dir + jpeg_error + '.JPG'
            if not os.path.exists(errorJPGFile):
                errorJPGFile = jpeg_dir + jpeg_error + '.jpg'
            # print('remove_file:', errorJPGFile)
            if if_clear:
                os.remove(errorJPGFile)
        for xml_error in errorXml_list:
            # print('errorXMLFile:', xml_error)
            errorXMLFile = annot_dir + xml_error + '.xml'
            # print('remove_file:', errorXMLFile)
            if if_clear:
                os.remove(errorXMLFile)
    else:
        print("检查无误：所有图片和对应的xml文件都是一一对应的。")


if __name__ == "__main__":
    # jpeg_dir = r"/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/JPEGImages/"
    # annot_dir = r"/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/Annotations/"
    # jpeg_dir = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_towerhead_detect/VOC2007/JPEGImages/'
    # annot_dir = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_towerhead_detect/VOC2007/Annotations/'
    # jpeg_dir = '/media/hxzh02/SB@home/hxzh/Dataset/变电站异物数据集/母线构架鸟巢/JPEGImages/'
    # annot_dir = '/media/hxzh02/SB@home/hxzh/Dataset/变电站异物数据集/母线构架鸟巢/Annotations/'
    jpeg_dir = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_foreignbody_detect/VOC2007/JPEGImages/'
    annot_dir = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_foreignbody_detect/VOC2007/Annotations/'
    checkJpgXml(jpeg_dir, annot_dir,if_clear = False)
