import numpy as np
import pandas as pd
from xml.dom import minidom
import os
import csv
import ast

xml_dir = 'VOCdevkit/VOC2007/Annotations'
# xml_dir = 'tmp'
csv_filename = os.path.join('data/', 'train.csv')

def create_xml(filename, bboxs):
    width = 1024
    height = 1024
    depth = 3
    # 1.创建DOM树对象
    dom = minidom.Document()
    # 2.创建根节点。每次都要用DOM对象来创建任何节点。
    root_node = dom.createElement('annotation')
    # 3.用DOM对象添加根节点
    dom.appendChild(root_node)

    filename_node = dom.createElement('filename')
    root_node.appendChild(filename_node)
    # 也用DOM创建文本节点，把文本节点（文字内容）看成子节点
    name_text = dom.createTextNode(filename)
    # 用添加了文本的节点对象（看成文本节点的父节点）添加文本节点
    filename_node.appendChild(name_text)

    # size
    size_node = dom.createElement('size')
    root_node.appendChild(size_node)
    width_node = dom.createElement('width')
    height_node = dom.createElement('height')
    depth_node = dom.createElement('depth')
    # width
    size_node.appendChild(width_node)
    width_text = dom.createTextNode(str(width))
    width_node.appendChild(width_text)
    # height
    size_node.appendChild(height_node)
    height_text = dom.createTextNode(str(height))
    height_node.appendChild(height_text)
    # depth
    size_node.appendChild(depth_node)
    depth_text = dom.createTextNode(str(depth))
    depth_node.appendChild(depth_text)

    for bbox in bboxs:
        # 创建obejct
        object_node = dom.createElement('object')
        root_node.appendChild(object_node)
        # 创建类别name
        name_node = dom.createElement('name')
        name_text = dom.createTextNode('Wheat')
        name_node.appendChild(name_text)
        object_node.appendChild(name_node)
        # 创建bndbox
        # bbox [xmin, ymin, width, height]
        bbox = ast.literal_eval(bbox)
        xmin, ymin = int(float(bbox[0])), int(float(bbox[1]))
        xmax, ymax = xmin + int(float(bbox[2])), ymin + int(float(bbox[3]))

        bndbox = dom.createElement('bndbox')
        object_node.appendChild(bndbox)
        # xmin
        xmin_node = dom.createElement('xmin')
        xmin_text = dom.createTextNode(str(xmin))
        xmin_node.appendChild(xmin_text)
        bndbox.appendChild(xmin_node)
        # ymin
        ymin_node = dom.createElement('ymin')
        ymin_text = dom.createTextNode(str(ymin))
        ymin_node.appendChild(ymin_text)
        bndbox.appendChild(ymin_node)
        # xmax
        xmax_node = dom.createElement('xmax')
        xmax_text = dom.createTextNode(str(xmax))
        xmax_node.appendChild(xmax_text)
        bndbox.appendChild(xmax_node)
        # ymax
        ymax_node = dom.createElement('ymax')
        ymax_text = dom.createTextNode(str(ymax))
        ymax_node.appendChild(ymax_text)
        bndbox.appendChild(ymax_node)

    # 每一个结点对象（包括dom对象本身）都有输出XML内容的方法，如：toxml()--字符串, toprettyxml()--美化树形格式。
    try:
        with open(os.path.join(xml_dir, filename) + '.xml', 'w', encoding='UTF-8') as fh:
            # 4.writexml()第一个参数是目标文件对象，第二个参数是根节点的缩进格式，第三个参数是其他子节点的缩进格式，
            # 第四个参数制定了换行格式，第五个参数制定了xml内容的编码。
            dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
            #print('写入xml OK!')
    except Exception as err:
        print('错误信息：{0}'.format(err))


def main():
    with open(csv_filename, 'r', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        # 自动获取第一张照片的文件名，并设置为last_image
        last_image = 'b6ab77fd7'
        img_num = 1
        bboxs = []
        for row in reader:
            if row['image_id'] == last_image:
                # 叠加bbox [xmin, ymin, width, height]
                bboxs.append(row['bbox'])
            elif row['image_id'] != last_image:
                # 创建xml文件
                create_xml(last_image, bboxs)
                last_image = row['image_id']
                img_num += 1
                # 重置bbox
                bboxs.clear()
                bboxs.append(row['bbox'])
        print(img_num)
        print('写入xml OK!')


if __name__ == '__main__':
    main()
