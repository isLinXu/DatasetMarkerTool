# -*- coding:utf-8 -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-12-06 上午10:00
@desc: 数据集xml标注文件label修改与更新
'''

import os
import xml.etree.ElementTree as ET

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
            print("process...")
            if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):
                origin_ann_path = os.path.join(r'%s%s' % (origin_ann_dir, filename))
                new_ann_path = os.path.join(r'%s%s' % (new_ann_dir, filename))
                print('origin_ann_path',origin_ann_path)

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


if __name__ == '__main__':
    # 设置原始标签路径为 Annos
    origin_ann_dir = r'/home/linxu/Desktop/龙岩_标注图像/xml/'
    # 设置新标签路径 Annotations
    new_ann_dir = r'/home/linxu/Desktop/龙岩_标注图像/Annotations/'

    # 设置清除标签
    remove_list = ['refrigerator','potted plant','keyboard','skateboard','suitcase','boat','refrigerator','baseball glove','bench','laptop','baseball bat','truck','refrigerator']

    # 更新标签名称
    update_label_list = ['1_0_6_21_42_0']
    new_name = 'Status indicator'

    # 更新xml标签：清除/修改xml文件中label
    update_xml_label(origin_ann_dir, new_ann_dir, remove_list, update_label_list, new_name)
