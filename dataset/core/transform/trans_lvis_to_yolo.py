import json
import os
from lvis import LVIS

def convert_lvis_to_yolo(lvis_ann_file, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 加载LVIS注释
    lvis = LVIS(lvis_ann_file)

    # 遍历每个图像
    for img_id in lvis.get_img_ids():
        img_info = lvis.load_imgs([img_id])[0]
        img_file_name = img_info['file_name']
        img_width = img_info['width']
        img_height = img_info['height']

        # 获取图像的所有注释
        ann_ids = lvis.get_ann_ids(img_ids=[img_id])
        anns = lvis.load_anns(ann_ids)

        # 创建YOLO格式的标签文件
        yolo_label_file = os.path.join(output_dir, os.path.splitext(img_file_name)[0] + '.txt')

        with open(yolo_label_file, 'w') as f:
            for ann in anns:
                # 获取边界框信息
                bbox = ann['bbox']
                x, y, w, h = bbox

                # 将边界框坐标转换为YOLO格式
                x_center = (x + w / 2) / img_width
                y_center = (y + h / 2) / img_height
                w = w / img_width
                h = h / img_height

                # 写入YOLO格式的标签文件
                f.write(f"{ann['category_id']} {x_center} {y_center} {w} {h}\n")


if __name__ == '__main__':
    lvis_ann_file = 'path/to/lvis/annotations.json'
    output_dir = 'path/to/output/yolo/labels'
    convert_lvis_to_yolo(lvis_ann_file, output_dir)