# import json
# import os
# from lvis import LVIS
#
# def convert_lvis_to_yolo(lvis_ann_file, output_dir):
#     # 创建输出目录
#     os.makedirs(output_dir, exist_ok=True)
#
#     # 加载LVIS注释
#     lvis = LVIS(lvis_ann_file)
#
#     # 遍历每个图像
#     for img_id in lvis.get_img_ids():
#         img_info = lvis.load_imgs([img_id])[0]
#         img_file_name = img_info['file_name']
#         img_width = img_info['width']
#         img_height = img_info['height']
#
#         # 获取图像的所有注释
#         ann_ids = lvis.get_ann_ids(img_ids=[img_id])
#         anns = lvis.load_anns(ann_ids)
#
#         # 创建YOLO格式的标签文件
#         yolo_label_file = os.path.join(output_dir, os.path.splitext(img_file_name)[0] + '.txt')
#
#         with open(yolo_label_file, 'w') as f:
#             for ann in anns:
#                 # 获取边界框信息
#                 bbox = ann['bbox']
#                 x, y, w, h = bbox
#
#                 # 将边界框坐标转换为YOLO格式
#                 x_center = (x + w / 2) / img_width
#                 y_center = (y + h / 2) / img_height
#                 w = w / img_width
#                 h = h / img_height
#
#                 # 写入YOLO格式的标签文件
#                 f.write(f"{ann['category_id']} {x_center} {y_center} {w} {h}\n")
#
#
# if __name__ == '__main__':
#     lvis_ann_file = 'path/to/lvis/annotations.json'
#     output_dir = 'path/to/output/yolo/labels'
#     convert_lvis_to_yolo(lvis_ann_file, output_dir)

import os
import json
import cv2

def lvis_to_yolo(lvis_path, images_path, output_path):
    # 读取LVIS数据集的标注文件
    with open(lvis_path, 'r') as f:
        lvis_data = json.load(f)

    # 遍历每个图像及其对应的标注
    for image_data in lvis_data['images']:
        image_id = image_data['id']
        image_width = image_data['width']
        image_height = image_data['height']

        # 读取图像
        image_path = os.path.join(images_path, image_data['file_name'])
        image = cv2.imread(image_path)

        # 获取当前图像的标注
        annotations = [ann for ann in lvis_data['annotations'] if ann['image_id'] == image_id]

        # 将标注转换为YOLO格式
        yolo_annotations = []
        for annotation in annotations:
            bbox = annotation['bbox']
            x_center = (bbox[0] + bbox[2] / 2) / image_width
            y_center = (bbox[1] + bbox[3] / 2) / image_height
            width = bbox[2] / image_width
            height = bbox[3] / image_height

            yolo_annotation = f"{annotation['category_id']} {x_center} {y_center} {width} {height}"
            yolo_annotations.append(yolo_annotation)

        # 将转换后的标注写入对应的TXT文件
        output_file = os.path.join(output_path, os.path.splitext(image_data['file_name'])[0] + '.txt')
        with open(output_file, 'w') as f:
            f.write('\n'.join(yolo_annotations))

if __name__ == "__main__":
    lvis_path = "path/to/lvis/annotations/lvis_v1_val.json"
    images_path = "path/to/lvis/val"
    output_path = "path/to/yolo/annotations"

    lvis_to_yolo(lvis_path, images_path, output_path)