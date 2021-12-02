# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np


def parse_obj(xml_path, filename):
    '''
    解析对象属性
    :param xml_path: xml文件根路径
    :param filename: xml文件名称
    :return:
    '''
    tree = ET.parse(xml_path + filename)
    objects = []

    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        objects.append(obj_struct)
    return objects


def update_xml(root_name, element='object', search_name='name', result=''):
    '''
    读取xml并更新label名称name
    :param root_name: xml文件根路径
    :param element: 搜索元素名称
    :param search_name: 名称
    :param result:
    :return:
    '''
    # 查找节点并更新
    root_dir = root_name + '.xml'
    root = ET.parse(root_dir)
    for node in root.findall(element):
        name = node.find('name').text
        # print('nname', name)
        # print('node.text',node.text)
        if name != search_name:
            node.find('name').text = result
            # print('result', result)
            # node.tag = 'object'
    # ET.dump(root)  #打印xml
    root.write(root_dir)

def Analysis_statistics_dataset(xml_root_dir):
    filenamess = os.listdir(xml_root_dir)
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

    recs = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}

    for i, nm in enumerate(filenames):
        try:
            # print('name', nm)
            recs[nm] = parse_obj(xml_root_dir, nm + '.xml')
        except:
            print('error')
        # print('更新xml..')

        # ---------------------------------------------------#
        #   更新xml-object中label标签
        # ---------------------------------------------------#
        root_name = xml_root_dir + nm
        element = 'object'
        search_name = 'name'
        result = 'insulator'
        update_xml(root_name, element, search_name, result)

    # ---------------------------------------------------#
    #   根据keys进行object信息的整理统计
    # ---------------------------------------------------#
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
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/7-输电线路绝缘子数据集VOC/dataset_insulator/VOC2007/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/3-输电线路异物数据集（VOC）/foreignbody_dataset_part1/VOC2007/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/1-火焰数据集/fire_dataset/VOC2007/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/5-安全帽数据集5000张/dataset_safetyHat/VOC2007/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/6-井盖电箱线杆标石头2400张/D0009/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/8-输电线路金具VOC/2511bwb_5/Annotations/'
    # xml_root_dir = '/media/hxzh02/SB@home/hxzh/Dataset/无人机杆塔航拍数据集/杆塔主体/VOCdevkit_tower_part/Annotations/'
    xml_root_dir = '/media/hxzh02/TU100Pro/Insulator/train/voc labels/'
    Analysis_statistics_dataset(xml_root_dir=xml_root_dir)