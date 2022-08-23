# -*- coding:utf-8 -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-12-06 上午10:00
@desc: 数据集xml标注文件label修改与更新
'''

import os
import xml.etree.ElementTree as ET
from os.path import exists

from tqdm import tqdm


def update_xml_label(origin_ann_dir, new_ann_dir, remove_list, update_label_list, new_name):
    '''
    更新xml_label
    :param origin_ann_dir:原始标签路径
    :param new_ann_dir:生成标签路径
    :param remove_list:清除标签列表
    :param update_label_list:更新标签列表
    :param new_name:新修改标签名称
    :return:
    '''
    # 判断是否存在新目录，若不存在则进行创建
    global tree
    if not os.path.exists(new_ann_dir):
        os.makedirs(new_ann_dir)

    # os.walk游走遍历目录名
    for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):
        for i in tqdm(range(0, len(filenames))):
            filename = filenames[i]
            print("process...", filename)
            origin_ann_path = origin_ann_dir + '/' + filename
            print('origin_ann_path', origin_ann_path)
            if exists(origin_ann_path):
                # if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):
                # origin_ann_path = os.path.join(r'%s%s' % (origin_ann_dir, filename))
                new_ann_path = os.path.join(r'%s%s' % (new_ann_dir, filename))
                print('origin_ann_path', origin_ann_path)

                # 判断xml内容是否为空
                labelread = open(origin_ann_path, 'r')  # 读取标注信息文件
                contens = labelread.readlines()  # 一次性全读出

                if contens:
                    tree = ET.parse(origin_ann_path)
                    root = tree.getroot()
                    for object in root.findall('object'):
                        name = str(object.find('name').text)
                        print('name', name)
                        # 如果name等于str，则删除该节点
                        if (name in remove_list):
                            root.remove(object)

                        # 如果name等于str，则修改name
                        if (name in update_label_list):
                            object.find('name').text = new_name
                else:
                    labelread.close()  # 将读的文件关闭，这里必须关闭
                    os.remove(origin_ann_path)  # 移除空标注文件
                # write写入新的文件中
                tree.write(new_ann_path)


####################################################################################
'''
功能：1、保留、修改xml文件某标签内容
     2、修改xml文件存放路径,文件名，照片来源等
     3、本方法采用字符串方式解析打开,删除/保存xml文件
'''


####################################################################################
def change_xml(path, save_path, imgpath):
    """
    功能: 1、保留、修改xml文件某标签内容
         2、修改xml文件存放路径,文件名，照片来源等
         3、本方法采用字符串方式解析打开,删除/保存xml文件
         4、方法是在Windows系统下运行的，方法中的路径请根据不同系统自行更改
         path = "/Annotations/"  # xml文件存放路径
         save_path = "/Annotations/xml"  # 修改后的xml文件存放路径
         imgpath = "/JPEGImages/"  # 新的照片path路径
    """
    files = os.listdir(path)  # 读取路径下所有文件名
    for xmlFile in files:
        if xmlFile.endswith('.xml'):
            tree = ET.ElementTree(file=path + xmlFile)  # 打开xml文件，送到tree解析
            root = tree.getroot()  # 得到文档元素对象
            root[0].text = 'pic'  # root[0].text是annotation下第一个子节点中内容，直接赋值替换文本内容
            root[1].text = xmlFile
            root[1].text = root[1].text.replace('xml', 'jpg')  # 修改根节点下的内容
            # root[1].text = root[1].text.split('.')[0] #根据需求决定要不要文件名后缀
            root[2].text = imgpath + xmlFile
            for object in root.findall('object'):
                name = object.find('name').text  # 获取每一个object节点下name节点的内容
                if name == 'plate':
                    object.find('name').text = str('pb')  # 修改指定标签的内容
                else:
                    root.remove(object)  # 删除除了name属性值为'plate'之外object节点的所有object节点
            tree.write(save_path + xmlFile)  # 替换后的内容保存在内存中需要将其写出


if __name__ == '__main__':
    # 设置原始标签路径为 Annos
    origin_ann_dir = r'/home/linxu/Desktop/xml/'
    # 设置新标签路径 Annotations
    new_ann_dir = r'/home/linxu/Desktop/xml1/'

    # 设置清除标签
    remove_list = ['apple']

    # 更新标签名称
    update_label_list = ['_0_0_30_?_1']
    new_name = '0_0_0_30_2_1'

    # 更新xml标签：清除/修改xml文件中label
    update_xml_label(origin_ann_dir, new_ann_dir, remove_list, update_label_list, new_name)

    # change_xml(path, save_path, imgpath)
