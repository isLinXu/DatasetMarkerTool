"""
根据xml文件的类别信息和位置坐标信息，将对应的类别对象crop出来，并存入到以类别信息命名的文件夹中
目的：便于标图后重新审核标图质量。

输入：包含图片的文件夹imgs，包含xml信息的文件夹xmls
输出：文件夹crop_img，crop_img下的以标签类别命名的子文件夹，以及crop的子图
"""

import cv2
import os
import xml.etree.ElementTree as ET

def crop_for_classify(img_file_dir, xml_file_dir, crop_img_dir):
    xmls = os.listdir(xml_file_dir)
    for xml in xmls:
        # 解析xml
        tree = ET.parse(os.path.join(xml_file_dir,xml))
        root = tree.getroot()

        img_name = root.find("filename").text
        img = cv2.imread(os.path.join(img_file_dir,img_name))

        objects = root.findall('object')
        for i, obj in enumerate(objects):
            id = 0
            label = obj.find('name').text
            if label == ":":
                label = "colon"

            bb = obj.find('bndbox')
            xmin = bb.find('xmin').text
            ymin = bb.find('ymin').text
            xmax = bb.find('xmax').text
            ymax = bb.find('ymax').text

            try:

                # 保存crop img
                crop_img = img[int(ymin):int(ymax), int(xmin):int(xmax)]

                # crop_img_name的命名方式：img_name+"_"+label+"_"+i
                crop_img_name = os.path.splitext(img_name)[0] + "_" + label+"_"+str(i)+".jpg"

                crop_img_save_dir = os.path.join(crop_img_dir,label)
                # crop_img_save_dir =
                print(crop_img_save_dir)
                if os.path.exists(crop_img_save_dir) == 0:
                    os.makedirs(crop_img_save_dir)
                crop_img_save_path = os.path.join(crop_img_save_dir, crop_img_name)
                cv2.imwrite(crop_img_save_path, crop_img)
            except:
                print('error file:', xml)
                continue

if __name__ == '__main__':
    img_file_dir = '/home/linxu/Desktop/Datasets/配电站房/JPEGImages'
    xml_file_dir = '/home/linxu/Desktop/Datasets/配电站房/Annotations'
    crop_img_dir = '/home/linxu/Desktop/Datasets/配电站房/crop_img'
    crop_for_classify(img_file_dir, xml_file_dir, crop_img_dir)
