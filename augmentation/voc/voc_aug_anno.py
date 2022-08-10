import albumentations as A
import cv2
import os
import json
import numpy as np
import shutil
import xml.etree.ElementTree as ET

# 定义类
class VOCAug(object):

    def __init__(self,
                 pre_image_path=None,
                 pre_xml_path=None,
                 aug_image_save_path=None,
                 aug_xml_save_path=None,
                 start_aug_id=None,
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
        self.pre_image_path = pre_image_path
        self.pre_xml_path = pre_xml_path
        self.aug_image_save_path = aug_image_save_path
        self.aug_xml_save_path = aug_xml_save_path
        self.start_aug_id = start_aug_id
        self.labels = labels
        self.max_len = max_len
        self.is_show = is_show

        print(self.labels)
        assert self.labels is not None, "labels is None!!!"

        # 数据增强选项
        self.aug = A.Compose([
            A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=1),
            A.GaussianBlur(p=0.7),
            A.GaussNoise(p=0.7),
            A.CLAHE(clip_limit=2.0, tile_grid_size=(4, 4), p=0.5),  # 直方图均衡
            A.Equalize(p=0.5),  # 均衡图像直方图
            A.OneOf([
                # A.RGBShift(r_shift_limit=50, g_shift_limit=50, b_shift_limit=50, p=0.5),
                # A.ChannelShuffle(p=0.3),  # 随机排列通道
                # A.ColorJitter(p=0.3),  # 随机改变图像的亮度、对比度、饱和度、色调
                # A.ChannelDropout(p=0.3),  # 随机丢弃通道
            ], p=0.),
            # A.Downscale(p=0.1),  # 随机缩小和放大来降低图像质量
            A.Emboss(p=0.2),  # 压印输入图像并将结果与原始图像叠加
        ],
            # voc: [xmin, ymin, xmax, ymax]  # 经过归一化
            # min_area: 表示bbox占据的像素总个数, 当数据增强后, 若bbox小于这个值则从返回的bbox列表删除该bbox.
            # min_visibility: 值域为[0,1], 如果增强后的bbox面积和增强前的bbox面积比值小于该值, 则删除该bbox
            A.BboxParams(format='pascal_voc', min_area=0., min_visibility=0., label_fields=['category_id'])
        )
        print('--------------*--------------')
        print("labels: ", self.labels)
        if self.start_aug_id is None:
            self.start_aug_id = len(os.listdir(self.pre_xml_path))
            print("the start_aug_id is not set, default: len(images)", self.start_aug_id)
        print('--------------*--------------')

    def get_xml_data(self, xml_filename):
        with open(os.path.join(self.pre_xml_path, xml_filename), 'r') as f:
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
            image = cv2.imread(os.path.join(self.pre_image_path, image_name))

        return bboxes, cls_id_list, image, image_name

    def aug_image(self):
        xml_list = os.listdir(self.pre_xml_path)

        cnt = self.start_aug_id
        for xml in xml_list:
            # AI Studio下会存在.ipynb_checkpoints文件, 为了不报错, 根据文件后缀过滤
            file_suffix = xml.split('.')[-1]
            if file_suffix not in ['xml']:
                continue
            bboxes, cls_id_list, image, image_name = self.get_xml_data(xml)


            anno_dict = {'image': image, 'bboxes': bboxes, 'category_id': cls_id_list}
            # 获得增强后的数据 {"image", "bboxes", "category_id"}

            try:
                augmented = self.aug(**anno_dict)

                # 保存增强后的数据
                flag = self.save_aug_data(augmented, image_name, cnt)
            except:
                pass
            if flag:
                cnt += 1
            else:
                continue

    def save_aug_data(self, augmented, image_name, cnt):
        aug_image = augmented['image']
        aug_bboxes = augmented['bboxes']
        aug_category_id = augmented['category_id']
        # print(aug_bboxes)
        # print(aug_category_id)

        name = '0' * self.max_len
        # 获取图片的后缀名
        image_suffix = image_name.split(".")[-1]

        # 未增强对应的xml文件名
        pre_xml_name = image_name.replace(image_suffix, 'xml')

        # 获取新的增强图像的文件名
        cnt_str = str(cnt)
        length = len(cnt_str)
        new_image_name = name[:-length] + cnt_str + "." + image_suffix

        # 获取新的增强xml文本的文件名
        new_xml_name = new_image_name.replace(image_suffix, 'xml')

        # 获取增强后的图片新的宽和高
        new_image_height, new_image_width = aug_image.shape[:2]

        # 深拷贝图片
        aug_image_copy = aug_image.copy()

        # 在对应的原始xml上进行修改, 获得增强后的xml文本
        with open(os.path.join(self.pre_xml_path, pre_xml_name), 'r') as pre_xml:
            aug_tree = ET.parse(pre_xml)

        # 修改image_filename值
        root = aug_tree.getroot()
        aug_tree.find('filename').text = new_image_name

        # 修改变换后的图片大小
        size = root.find('size')
        size.find('width').text = str(new_image_width)
        size.find('height').text = str(new_image_height)

        # 修改每一个标注框
        for index, obj in enumerate(root.iter('object')):
            try:
                obj.find('name').text = self.labels[aug_category_id[index]]
                xmin, ymin, xmax, ymax = aug_bboxes[index]
                xml_box = obj.find('bndbox')
                xml_box.find('xmin').text = str(int(xmin))
                xml_box.find('ymin').text = str(int(ymin))
                xml_box.find('xmax').text = str(int(xmax))
                xml_box.find('ymax').text = str(int(ymax))
                if self.is_show:
                    tl = 2
                    text = f"{LABELS[aug_category_id[index]]}"
                    t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tl)[0]
                    cv2.rectangle(aug_image_copy, (int(xmin), int(ymin) - 3),
                                  (int(xmin) + t_size[0], int(ymin) - t_size[1] - 3),
                                  (0, 0, 255), -1, cv2.LINE_AA)  # filled
                    cv2.putText(aug_image_copy, text, (int(xmin), int(ymin) - 2), 0, tl / 3, (255, 255, 255), tl,
                                cv2.LINE_AA)
                    cv2.rectangle(aug_image_copy, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 255, 0), 2)
            except:
                pass
        if self.is_show:
            cv2.imshow('aug_image_show', aug_image_copy)
            # 按下s键保存增强，否则取消保存此次增强
            key = cv2.waitKey(0)
            if key & 0xff == ord('s'):
                pass
            else:
                return False
        # 保存增强后的图片
        cv2.imwrite(os.path.join(self.aug_image_save_path, new_image_name), aug_image)
        # 保存增强后的xml文件
        tree = ET.ElementTree(root)
        tree.write(os.path.join(self.aug_xml_save_path, new_xml_name))

        return True

if __name__ == '__main__':
    import albumentations as A
    import xml.etree.ElementTree as ET
    import matplotlib.pyplot as plt

    # 原始的xml路径和图片路径
    PRE_IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/JPEGImages'
    PRE_XML_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/Annotations'

    # 增强后保存的xml路径和图片路径
    AUG_SAVE_IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/aug/images'
    AUG_SAVE_XML_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/aug/labels'

    # 标签列表
    # LABELS = ['zu', 'pai', 'lan']
    # LABELS = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
    #           'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    #           'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    #           'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
    #           'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    #           'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    #           'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
    #           'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
    #           'teddy bear','hair drier', 'toothbrush']
    LABELS = ['0_0_0_20_0_0', '0_0_0_18_0_0', '0_0_0_50_0_0', '1_0_4_21_40_0',
              '0_0_0_40_1_0', '0_0_0_30_2_0', '1_0_0_1_8_1', '1_0_0_31_0_0',
              '0_0_0_30_3_0', '1_0_0_1_4_0', '0_0_0_16_0_0', '0_0_0_28_0_0',
              '1_0_0_2_30_0', '1_0_6_21_42_0', '1_0_3_22_41_0', '1_0_3_22_46_0',
              '0_0_0_30_4_0', '1_0_3_22_45_0', '1_0_0_1_6_0', '1_0_0_1_8_0',
              '1_0_0_1_53_0', '1_0_3_22_47_0', '1_0_0_30_3_0', '1_0_6_21_43_0']



    aug = VOCAug(
        pre_image_path=PRE_IMAGE_PATH,
        pre_xml_path=PRE_XML_PATH,
        aug_image_save_path=AUG_SAVE_IMAGE_PATH,
        aug_xml_save_path=AUG_SAVE_XML_PATH,
        start_aug_id=None,
        labels=LABELS,
        is_show=True,
    )

    aug.aug_image()