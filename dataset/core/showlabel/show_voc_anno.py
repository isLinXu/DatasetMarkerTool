import albumentations as A
import cv2
import os
import json
import numpy as np
import shutil
import xml.etree.ElementTree as ET


# 定义类
class VOCShow(object):

    def __init__(self,
                 image_path=None,
                 xml_path=None,
                 labels=None,
                 max_len=4,
                 is_show=False):
        """
        :param pre_image_path:
        :param pre_xml_path:
        :param aug_image_save_path:
        :param aug_xml_save_path:
        :param start_aug_id:
        :param labels: 标签列表, 展示增强后的图片用
        :param max_len:
        :param is_show:
        """
        self.image_path = image_path
        self.xml_path = xml_path
        self.labels = labels
        self.max_len = max_len
        self.is_show = is_show

        print(self.labels)
        assert self.labels is not None, "labels is None!!!"

        print('--------------*--------------')
        print("labels: ", self.labels)

    def get_xml_data(self, xml_filename):
        with open(os.path.join(self.xml_path, xml_filename), 'r') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            image_name = tree.find('filename').text
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            bboxes = []
            cls_id_list = []
            for obj in root.iter('object'):
                # difficult = obj.find('difficult').text
                difficult = obj.find('difficult').text
                cls_name = obj.find('name').text  # label
                if cls_name not in LABELS or int(difficult) == 1:
                    continue
                xml_box = obj.find('bndbox')

                xmin = int(xml_box.find('xmin').text)
                ymin = int(xml_box.find('ymin').text)
                xmax = int(xml_box.find('xmax').text)
                ymax = int(xml_box.find('ymax').text)

                # 标注越界修正
                if xmax > w:
                    xmax = w
                if ymax > h:
                    ymax = h
                bbox = [xmin, ymin, xmax, ymax]
                bboxes.append(bbox)
                cls_id_list.append(self.labels.index(cls_name))

            # 读取图片
            image = cv2.imread(os.path.join(self.image_path, image_name))

        return bboxes, cls_id_list, image, image_name

    def show_image(self):
        xml_list = os.listdir(self.xml_path)
        cnt = 0
        flag = True
        for xml in xml_list:
            file_suffix = xml.split('.')[-1]
            if file_suffix not in ['xml']:
                continue
            bboxes, cls_id_list, image, image_name = self.get_xml_data(xml)

            anno_dict = {'image': image, 'bboxes': bboxes, 'category_id': cls_id_list}
            try:

                # 显示数据
                flag = self.show_voc_data(anno_dict, image_name, cnt)
            except:
                pass
            if flag:
                cnt += 1
            else:
                continue


    def show_voc_data(self, augmented, image_name, cnt):
        _image = augmented['image']
        _bboxes = augmented['bboxes']
        _category_id = augmented['category_id']

        name = '0' * self.max_len
        # 获取图片的后缀名
        image_suffix = image_name.split(".")[-1]

        # 对应的xml文件名
        _xml_name = image_name.replace(image_suffix, 'xml')

        # 深拷贝图片
        _image_copy = _image.copy()

        # # 在对应的原始xml上进行修改, 获得增强后的xml文本
        with open(os.path.join(self.xml_path, _xml_name), 'r') as pre_xml:
            aug_tree = ET.parse(pre_xml)

        root = aug_tree.getroot()
        try:
            # 修改每一个标注框
            for index, obj in enumerate(root.iter('object')):
                obj.find('name').text = self.labels[_category_id[index]]
                xmin, ymin, xmax, ymax = _bboxes[index]
                xml_box = obj.find('bndbox')
                xml_box.find('xmin').text = str(int(xmin))
                xml_box.find('ymin').text = str(int(ymin))
                xml_box.find('xmax').text = str(int(xmax))
                xml_box.find('ymax').text = str(int(ymax))
                if self.is_show:
                    tl = 2
                    text = f"{LABELS[_category_id[index]]}"
                    t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tl)[0]
                    cv2.rectangle(_image_copy, (int(xmin), int(ymin) - 3),
                                  (int(xmin) + t_size[0], int(ymin) - t_size[1] - 3),
                                  (0, 0, 255), -1, cv2.LINE_AA)  # filled
                    cv2.putText(_image_copy, text, (int(xmin), int(ymin) - 2), 0, tl / 3, (255, 255, 255), tl,cv2.LINE_AA)
                    # cv2.putText(aug_image_copy, text, (20, 20), 0, 0.5, (255, 255, 255), 0.5,cv2.LINE_AA)
                    cv2.rectangle(_image_copy, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 255, 0), 2)
            print('image_name', _xml_name)
        except:
            pass
        if self.is_show:
            show_title = 'voc_show'
            cv2.imshow(str(show_title), _image_copy)
            # 按下s键保存
            key = cv2.waitKey(0)
            if key & 0xff == ord('s'):
                pass
            else:
                return False

        return True

if __name__ == '__main__':
    # xml路径和图片路径
    IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/JPEGImages'
    XML_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/Annotations'

    # 标签列表
    LABELS = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
              'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
              'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
              'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
              'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
              'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
              'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
              'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
              'teddy bear','hair drier', 'toothbrush']

    aug = VOCShow(
        image_path=IMAGE_PATH,
        xml_path=XML_PATH,
        labels=LABELS,
        is_show=True,
    )

    aug.show_image()
