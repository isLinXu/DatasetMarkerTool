# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np


def parse_obj(xml_path, filename):
    '''
    解析对象属性
    :param xml_path:
    :param filename:
    :return:
    '''
    tree = ET.parse(xml_path + filename)
    objects = []

    for obj in tree.findall('object'):
        obj_struct = {}
    obj_struct['name'] = obj.find('name').text
    objects.append(obj_struct)
    return objects


def update_xml(xml_path, find_):
    # 查找节点并更新
    root = ET.parse(xml_path)
    for node in root.findall(".//folder"):
        if node.text == "/home":
            node.tag = "path"
    ET.dump(root)  # 打印xml
    root.write("output.xml")


def Analysis_statistics_dataset(xml_path):
    filenamess = os.listdir(xml_path)
    filenames = []
    print('filenamess', filenamess)
    print('len', len(filenamess))
    # ---------------------------------------------------#
    #   整理xml信息
    # ---------------------------------------------------#
    # 分割xml的名称
    for name in filenamess:
        print('name', name)
        if name.endswith('.xml'):
            name = name.split('.xml')[0]
            # print('nname',name)
            filenames.append(name)
    # print('ss', len(filenames))
    recs = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}

    for i, nm in enumerate(filenames):
        try:
            # print('name', nm)
            recs[nm] = parse_obj(xml_path, nm + '.xml')
        except:
            print('error')
    for name in filenames:
        # print('name', name)
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
        if object['name'] not in classnames:
            classnames.append(object['name'])

    # ---------------------------------------------------#
    #   打印统计信息
    # ---------------------------------------------------#
    print('classnames:', classnames)
    for name in classnames:
        print('{}:{}个'.format(name, num_objs[name]))
    print('信息统计完毕。')


if __name__ == '__main__':
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/7-输电线路绝缘子数据集VOC/dataset_insulator/VOC2007/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/3-输电线路异物数据集（VOC）/foreignbody_dataset_part1/VOC2007/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/1-火焰数据集/fire_dataset/VOC2007/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/5-安全帽数据集5000张/dataset_safetyHat/VOC2007/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/6-井盖电箱线杆标石头2400张/D0009/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/8-输电线路金具VOC/2511bwb_5/Annotations/'
    # xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机杆塔航拍数据集/杆塔主体/VOCdevkit_tower_part/Annotations/'
    xml_path = '/media/hxzh02/TU100Pro/Insulator/train/voc labels/'
    Analysis_statistics_dataset(xml_path=xml_path)
