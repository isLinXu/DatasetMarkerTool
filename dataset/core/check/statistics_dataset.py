# -*- coding:utf-8 -*-
import os
import xml.etree.ElementTree as ET
import numpy as np

# np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib
from PIL import Image

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



def Analysis_statistics_dataset(xml_path):
    filenamess = os.listdir(xml_path)
    filenames = []
    print('filenamess', filenamess)
    print('len', len(filenamess))
    for name in filenamess:
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
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')

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
    print('信息统计算完毕。')

if __name__ == '__main__':
    xml_path = '/media/hxzh02/SB@home/hxzh/Dataset/Plane_detect_datasets/VOCdevkit_tower_part/VOC2007/Annotations/'
    Analysis_statistics_dataset(xml_path=xml_path)