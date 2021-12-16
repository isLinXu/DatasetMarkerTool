import os
import sys
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from PIL import Image

def fix_xml(filename):
    filepath = filename + ".xml"
    xmlFilePath = os.path.abspath(filepath)
    print(xmlFilePath)
    try:
        tree = ET.parse(xmlFilePath)
        root = tree.getroot()
    except Exception as e:
        print("parse xml fail!")
        sys.exit()

    size = root.find("size")
    if size==None: #查看size是否存在
        img_width,img_height,img_depth = find_image_size(filename) 
        #若不存在，查找图片size
        size_element = Element('size')
        width_element = Element('width')
        width_element.text = str(img_width)
        height_element = Element('height')
        height_element.text = str(img_height)
        depth_element = Element('depth')
        depth_element.text = str(img_depth)
        size_element.append(width_element)
        size_element.append(height_element)
        size_element.append(depth_element)
        root.append(size_element)
    else: #若存在，检查width和height是否为0
        width = size.find("width")
        text_width = width.text
        height = size.find("height")
        text_height = height.text
        if text_width == '0' or text_height == '0':
            print("width or height is 0!\n")
            img_width, img_height, img_depth = find_image_size(filename)
            width.text = str(img_width)
            height.text = str(img_height)
            depth = size.find("depth")
            depth.text = str(img_depth)

    tree.write(filepath,encoding='utf-8',xml_declaration=True)

def find_image_size(filename):
    filepath = filename + ".jpg"
    with Image.open(os.path.join(filepath)) as img:
        img_width = img.size[0]
        img_height = img.size[1]
        img_mode = img.mode
        if img_mode == "RGB":
            img_depth = 3
        elif img_mode == "RGBA":
            img_depth = 3
        elif img_mode == "L":
            img_depth = 1
        else:
            print("img_mode = %s is neither RGB or L" % img_mode)
            exit(0)

        print("image : weight = %d, height =%d depth =%d " % (img_width, img_height, img_depth))
        return img_width, img_height, img_depth

imagedir = 'D:\\fix_face_mask\\'
img_list = sorted(os.listdir(imagedir))

for image in img_list: #遍历文件
    fields = image.split(".")
    filename_wo_extension = fields[0]
    extention = fields[1]

    if extention == 'xml': #分析xml文件恢复数据
        fix_xml(filename_wo_extension)
