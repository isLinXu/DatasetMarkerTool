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

                # write写入新的文件中
                tree.write(new_ann_path)


if __name__ == '__main__':
    # 设置原始标签路径为 Annos
    origin_ann_dir = r'/media/hxzh02/SB@home/hxzh/Dataset/变电站异物数据集/母线构架鸟巢/Annotations/'
    # 设置新标签路径 Annotations
    new_ann_dir = r'/media/hxzh02/SB@home/hxzh/Dataset/变电站异物数据集/母线构架鸟巢/Annotations1/'

    # 设置清除标签
    remove_list = ['tower_foot','tower_body','tower_body_down','tree_branch']
    # 更新标签名称
    update_label_list = ['bird_nest']
    new_name = 'nest'

    # 更新xml标签：清除/修改xml文件中label
    update_xml_label(origin_ann_dir, new_ann_dir, remove_list, update_label_list, new_name)
