import json
import os
import shutil

import cv2
from tqdm import tqdm

'''
coco_classes:
  0: person
  1: bicycle
  2: car
  3: motorcycle
  4: airplane
  5: bus
  6: train
  7: truck
  8: boat
  9: traffic light
  10: fire hydrant
  11: stop sign
  12: parking meter
  13: bench
  14: bird
  15: cat
  16: dog
  17: horse
  18: sheep
  19: cow
  20: elephant
  21: bear
  22: zebra
  23: giraffe
  24: backpack
  25: umbrella
  26: handbag
  27: tie
  28: suitcase
  29: frisbee
  30: skis
  31: snowboard
  32: sports ball
  33: kite
  34: baseball bat
  35: baseball glove
  36: skateboard
  37: surfboard
  38: tennis racket
  39: bottle
  40: wine glass
  41: cup
  42: fork
  43: knife
  44: spoon
  45: bowl
  46: banana
  47: apple
  48: sandwich
  49: orange
  50: broccoli
  51: carrot
  52: hot dog
  53: pizza
  54: donut
  55: cake
  56: chair
  57: couch
  58: potted plant
  59: bed
  60: dining table
  61: toilet
  62: tv
  63: laptop
  64: mouse
  65: remote
  66: keyboard
  67: cell phone
  68: microwave
  69: oven
  70: toaster
  71: sink
  72: refrigerator
  73: book
  74: clock
  75: vase
  76: scissors
  77: teddy bear
  78: hair drier
  79: toothbrush
'''


def extract_coco_data(coco_file, coco_img_dir, output_dir, category_dict):
    # 读取COCO数据集文件
    with open(coco_file, 'r') as f:
        coco_data = json.load(f)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)

    # 遍历所有的图像
    for image in tqdm(coco_data['images'], desc='Processing images'):
        # 判断图像中是否包含指定的类别
        has_category = False
        for annotation in coco_data['annotations']:
            # try:
            if annotation['image_id'] == image['id']:
                try:
                    # print("annotation:", annotation)
                    category_name = coco_data['categories'][annotation['category_id']]['name']
                    if category_name in category_dict.keys():
                        print("annotation:", annotation)
                        # print("image['id']:", image['id'])
                        has_category = True
                        print("category_name:{}".format(category_name), "category_dict.keys():", category_dict.keys())
                        # 如果图像中包含指定的类别，则复制图像和标注数据到输出目录
                        dir_name = 'train'
                        images_dir = coco_img_dir + '/train2017'
                        # if coco_file.find('train') != -1:
                        #     dir_name = 'train'
                        #     images_dir = coco_img_dir + '/train2017'
                        # else:
                        #     dir_name = 'val'
                        #     images_dir = coco_img_dir + '/val2017'
                        image_file = os.path.join(images_dir, image['file_name'])
                        output_image_dir = os.path.join(output_dir, 'images', dir_name)
                        output_image_file = os.path.join(output_image_dir, image['file_name'])
                        print("image['id']:", image['id'])
                        print("image_file:{}".format(image_file))
                        print("output_image_file:{}".format(output_image_file))

                        # 读取图片文件并获取其宽度和高度
                        img = cv2.imread(image_file)
                        img_height, img_width, _ = img.shape

                        if not os.path.exists(output_image_dir):
                            os.makedirs(output_image_dir)
                        if not os.path.exists(output_image_file):
                            shutil.copy(image_file, output_image_file)
                        output_label_dir = os.path.join(output_dir, 'labels', dir_name)
                        output_label_file = os.path.join(output_label_dir,
                                                         os.path.splitext(image['file_name'])[0] + '.txt')
                        print("output_label_file:{}".format(output_label_file))
                        print("output_label_dir:{}".format(output_label_dir))
                        if not os.path.exists(output_label_dir):
                            os.makedirs(output_label_dir)
                        if not os.path.exists(output_label_file):
                            with open(output_label_file, 'w') as f:
                                for annotation in coco_data['annotations']:
                                    if annotation['image_id'] == image['id']:
                                        try:
                                            # category = coco_data['categories'][annotation['category_id']]['name']
                                            if category_name in category_dict.keys():
                                                category_index = category_dict[category_name]
                                                bbox = annotation['bbox']
                                                x_center = bbox[0] + bbox[2] / 2
                                                y_center = bbox[1] + bbox[3] / 2
                                                width = bbox[2]
                                                height = bbox[3]
                                                # 归一化yolo格式
                                                x = float(x_center) / img_width
                                                y = float(y_center) / img_height
                                                w = float(width) / img_width
                                                h = float(height) / img_height
                                                f.write(
                                                    '{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}\n'.format(category_index, x, y,
                                                                                                   w, h))
                                        except Exception as e:
                                            print("e:{}".format(e))
                                            continue
                except Exception as e:
                    print("e:{}".format(e))
                    continue

    print('数据集提取完成！')


# 测试代码
# /media/linxu/LXWorkShop1/Dataset/coco数据集
coco_json_file = '/media/linxu/LXWorkShop1/Dataset/coco数据集/annotations_trainval2017/annotations/instances_train2017.json'
coco_img_dir = '/media/linxu/LXWorkShop1/Dataset'
# output_dir = '/media/linxu/LXWorkShop1/Dataset/coco数据集/COCO_YOLO2017'
# output_dir = '/media/linxu/MobilePan/2-Data/COCO_YOLO2017_nomotor'
output_dir = '/media/linxu/MobilePan/2-Data/COCO_YOLO2017_nomotor1'

# category_dict = {'person': 1, 'car': 0}  # 指定要抽取的类别和对应的类别索引
category_dict = {'bicycle': 1, 'motorcycle': 0}  # 指定要抽取的类别和对应的类别索引
extract_coco_data(coco_json_file, coco_img_dir, output_dir, category_dict)
