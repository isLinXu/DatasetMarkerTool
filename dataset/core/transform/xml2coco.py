# -*- coding:utf-8  -*-
'''
@author: linxu
@contact: 17746071609@163.com
@time: 2021-9-23 上午11:56
@desc: VOC(xml)格式转换为COCO(json)格式
'''
import os
import os.path as osp
import shutil
import xml.etree.ElementTree as ET

import json

from glob import glob
from tqdm import tqdm
from PIL import Image

#检测目标类别（不含background）
cls_classes = ['smoke']
label_ids = {name: i + 1 for i, name in enumerate(cls_classes)}

def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.mkdir(path)
    else:
        os.mkdir(path)

def get_segmentation(points):
    '''
    获得box角点
    :param points:
    :return:
    '''
    return [points[0], points[1], points[2] + points[0], points[1],
             points[2] + points[0], points[3] + points[1], points[0], points[3] + points[1]]

def parse_xml(xml_path, img_id, anno_id):
    '''
    xml解析
    :param xml_path: xml路径
    :param img_id: img id
    :param anno_id: 标注文件 id
    :return:
    '''
    tree = ET.parse(xml_path)
    root = tree.getroot()
    annotation = []
    for obj in root.findall('object'):
        try:
            name = obj.find('name').text       
            category_id = label_ids[name]
            bnd_box = obj.find('bndbox')   
            xmin = int(bnd_box.find('xmin').text)
            ymin = int(bnd_box.find('ymin').text)
            xmax = int(bnd_box.find('xmax').text)
            ymax = int(bnd_box.find('ymax').text)
            if xmin>=xmax or ymin>=ymax:
                continue
            w = xmax - xmin + 1
            h = ymax - ymin + 1
            area = w*h
            segmentation = get_segmentation([xmin, ymin, w, h])
            annotation.append({
                            "segmentation": segmentation,
                            "area": area,
                            "iscrowd": 0,
                            "image_id": img_id,
                            "bbox": [xmin, ymin, w, h],
                            "category_id": category_id,
                            "id": anno_id,
                            "ignore": 0})
            anno_id += 1
        except:
            continue
    return annotation, anno_id

def cvt_annotations(img_path, xml_path, out_file):
    '''
    转换标注格式
    :param img_path:
    :param xml_path:
    :param out_file:
    :return:
    '''
    images = []
    annotations = []
    img_id = 1
    anno_id = 1
    # 处理过程-进度条
    for img_path in tqdm(glob(img_path + '/*.jpg')):
        w, h = Image.open(img_path).size
        img_name = osp.basename(img_path)
        img = {"file_name": img_name, "height": int(h), "width": int(w), "id": img_id}
        images.append(img)

        xml_file_name = img_name.split('.')[0] + '.xml'
        xml_file_path = osp.join(xml_path, xml_file_name)
        annos, anno_id = parse_xml(xml_file_path, img_id, anno_id)
        annotations.extend(annos)
        img_id += 1

    categories = []
    for k,v in label_ids.items():
        categories.append({"name": k, "id": v})
    final_result = {"images": images, "annotations": annotations, "categories": categories} #COCO数据集格式
    #mmcv.dump(final_result, out_file) 需在mmdet环境下！
    with open(out_file, 'w') as f:
        json.dump(final_result, f, indent=4)
    return annotations


def main():
    # XML文件位置
    xml_path = "/home/hxzh02/文档/datasets_smoke/train"
    # Image文件位置
    img_path = "/home/hxzh02/文档/datasets_smoke/train"
    # COCO文件位置
    out_path = "/home/hxzh02/文档/datasets_smoke/annotations/instances_train.json"
    train_annotations = '/home/hxzh02/文档/datasets_smoke/annotations'


    mkr(train_annotations)

    # XML文件位置
    val_xml_path = "/home/hxzh02/文档/datasets_smoke/val/"
    # Image文件位置
    val_img_path = "/home/hxzh02/文档/datasets_smoke/val/"
    # COCO文件位置
    val_out_path = "/home/hxzh02/文档/datasets_smoke/annotations/instances_val.json"


    print('processing {} ...'.format("xml format annotations"))
    cvt_annotations(img_path, xml_path, out_path)
    cvt_annotations(val_img_path, val_xml_path, val_out_path)
    print('Done!')


if __name__ == '__main__':
    main()
