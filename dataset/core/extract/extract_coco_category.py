import json
import os
import shutil

import cv2
from tqdm import tqdm

def extract_coco_data(coco_file, img_file, output_dir, category_dict):
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
            if annotation['image_id'] == image['id']:
                if coco_data['categories'][annotation['category_id']]['name'] in category_dict.keys():
                    has_category = True
                    break

        # 如果图像中包含指定的类别，则复制图像和标注数据到输出目录
        if has_category:
            image_file = os.path.join(img_file, image['file_name'] + '.jpg')
            if 'train' in coco_file:
                output_image_dir = os.path.join(output_dir, 'images', 'train')
                output_label_dir = os.path.join(output_dir, 'labels', 'train')
            elif 'val' in coco_file:
                output_image_dir = os.path.join(output_dir, 'images', 'val')
                output_label_dir = os.path.join(output_dir, 'labels', 'val')
            # image_file = os.path.join(coco_data['images_dir'], image['file_name'])
            # output_image_dir = os.path.join(output_dir, 'images', 'train' if image['split'] == 'train' else 'val')
            # output_image_dir = os.path.join(output_dir, 'images', 'train')
            output_image_file = os.path.join(output_image_dir, image['file_name'] + '.jpg')
            print("output_image_file:", output_image_file)
            shutil.copy(image_file, output_image_file)

            # 读取图片文件并获取其宽度和高度
            img = cv2.imread(image_file)
            img_height, img_width, _ = img.shape

            # output_label_dir = os.path.join(output_dir, 'labels', 'train')
            # output_label_dir = os.path.join(output_dir, 'labels', 'train' if image['split'] == 'train' else 'val')
            output_label_file = os.path.join(output_label_dir, os.path.splitext(image['file_name'])[0] + '.txt')
            with open(output_label_file, 'w') as f:
                for annotation in coco_data['annotations']:
                    if annotation['image_id'] == image['id']:
                        category = coco_data['categories'][annotation['category_id']]['name']
                        if category in category_dict.keys():
                            category_index = category_dict[category]
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
                            f.write('{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}\n'.format(category_index, x, y, w, h))

    print('数据集提取完成！')

# 测试代码
coco_file = 'coco/annotations/instances_train2017.json'
img_file = 'coco/train2017/'
output_dir = 'datasets/search_dataset/coco'
category_dict = {'person': 0, 'car': 1, 'bus': 2, 'truck': 3}  # 指定要抽取的类别和对应的类别索引
extract_coco_data(coco_file, img_file, output_dir, category_dict)