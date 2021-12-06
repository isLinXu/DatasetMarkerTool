# -*- coding:utf-8 -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-12-06 上午10:00
@desc: 数据集xml标注文件label修改与更新
'''

import os
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    # 设置原始标签路径为 Annos
    origin_ann_dir = r'D:\Yuqian_Yang\project_yolov4\yolo\data\smokephone\annotation/'
    # 设置新标签路径 Annotations
    new_ann_dir = r'D:\Yuqian_Yang\project_yolov4\yolo\data\smokephone\Annotations/'

    remove_list = []
    
    # os.walk游走遍历目录名
    for dirpaths, dirnames, filenames in os.walk(origin_ann_dir):
        for filename in filenames:
            print("process...")
            if os.path.isfile(r'%s%s' % (origin_ann_dir, filename)):
                origin_ann_path = os.path.join(r'%s%s' % (origin_ann_dir, filename))
                new_ann_path = os.path.join(r'%s%s' % (new_ann_dir, filename))
                tree = ET.parse(origin_ann_path)
                root = tree.getroot()
                for object in root.findall('object'):
                    name = str(object.find('name').text)

                    # 如果name等于str，则删除该节点
                    if (name in ["phone"]):
                        root.remove(object)
                    if (name in ["normal"]):
                        root.remove(object)

                    # 如果name等于str，则修改name
                    if (name in ["smoke"]):
                        object.find('name').text = "xy"

                tree.write(new_ann_path)  # write写入新的文件中。
