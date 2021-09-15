#!/usr/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from PIL import Image
import numpy as np


num_to_class = {
  "1": "1",
  "2": "2",
  "3": "3"}


def write_xml(sh, sw, imgname, filepath, labeldicts):
    root = ET.Element('Annotation')
    ET.SubElement(root, 'filename').text = str(imgname)
    sizes = ET.SubElement(root, 'size')
    ET.SubElement(sizes, 'width').text = str(sw)
    ET.SubElement(sizes, 'height').text = str(sh)
    ET.SubElement(sizes, 'depth').text = '3'
    for labeldict in labeldicts:
        objects = ET.SubElement(root, 'object')
        ET.SubElement(objects, 'name').text = labeldict['name']
        ET.SubElement(objects, 'pose').text = 'Unspecified'
        ET.SubElement(objects, 'truncated').text = '0'
        ET.SubElement(objects, 'difficult').text = '0'
        bndbox = ET.SubElement(objects, 'bndbox')
        if labeldict['xmin'] < 0:
            labeldict['xmin'] = 0
        if labeldict['ymin'] < 0:
            labeldict['ymin'] = 0
        if labeldict['xmax'] > sw:
            labeldict['xmax'] = sw
        if labeldict['ymax'] > sh:
            labeldict['ymax'] = sh
        ET.SubElement(bndbox, 'xmin').text = str(int(labeldict['xmin']))
        ET.SubElement(bndbox, 'ymin').text = str(int(labeldict['ymin']))
        ET.SubElement(bndbox, 'xmax').text = str(int(labeldict['xmax']))
        ET.SubElement(bndbox, 'ymax').text = str(int(labeldict['ymax']))
    tree = ET.ElementTree(root)
    tree.write(filepath, encoding='utf-8')


def my_xml(file_name, annotations_path):
    # file_name = "train.json"
    # annotations_path = "xml/"
    with open(file_name, 'r', encoding='utf-8') as fr:
        load_dict = json.load(fr)
        imgToAnns = defaultdict(list)
        imgs = {}
        idToName = defaultdict(list)
        for ann in load_dict['annotations']:
            imgToAnns[str(ann['image_id'])].append(ann)
        for img in load_dict['images']:
            imgs[str(img['id'])] = img
            idToName[str(img['id'])] = img['file_name']
        for key, values in imgToAnns.items():
            label_dicts = []
            for value in values:
                category_id = value["category_id"]
                new_dict = {'name': num_to_class[str(category_id)],
                            # 'name': load_dict["categories"][category_id]["name"],
                            'difficult': '0',
                            'xmin': value["bbox"][0],
                            'ymin': value["bbox"][1],
                            'xmax': value["bbox"][0] + value["bbox"][2],
                            'ymax': value["bbox"][1] + value["bbox"][3]
                            }
                label_dicts.append(new_dict)
            write_xml(imgs[key]["height"], imgs[key]["width"], idToName[key],
                      annotations_path + idToName[key][0:-4] + '.xml', label_dicts)


if __name__ == '__main__':
    my_xml('train.json', './traffic_voc/Annotations/')
