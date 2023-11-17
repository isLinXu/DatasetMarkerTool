import os
import json
import cv2
from tqdm import tqdm

def lvis_to_yolo(lvis_path, images_path, output_path):
    # 读取LVIS数据集的标注文件
    with open(lvis_path, 'r') as f:
        lvis_data = json.load(f)

    image_list = list(lvis_data['images'])
    # print("image_list:",image_list)
    for image_data in tqdm(image_list):
        # image_data = image_list[i]
    # 遍历每个图像及其对应的标注
    # for image_data in lvis_data['images']:
        image_id = image_data['id']
        image_width = image_data['width']
        image_height = image_data['height']
        print("image_data:", image_data)
        # 读取图像
        file_name = image_data["coco_url"].split("/")[-1]
        print("file_name:", file_name)
        image_path = os.path.join(images_path, file_name)
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
        output_file = os.path.join(output_path, os.path.splitext(file_name)[0] + '.txt')
        with open(output_file, 'w') as f:
            f.write('\n'.join(yolo_annotations))

if __name__ == "__main__":
    #lvis_path = "/media/linxu/mobileSSD/datasets/LVIS_v1.0/annotations/lvis_v1_val.json"
    #images_path = "/media/linxu/mobileSSD/datasets/LVIS_v1.0/images"
    #output_path = "/media/linxu/ImportPan/outputs_data"
    # /media/linxu/ImportPan/lvis_train_yolo
    lvis_path = "/media/linxu/mobileSSD/datasets/LVIS_v1.0/annotations/lvis_v1_train.json"
    images_path = "/media/linxu/mobileSSD/datasets/LVIS_v1.0/images"
    output_path = "/media/linxu/ImportPan/lvis_train_yolo"
    lvis_to_yolo(lvis_path, images_path, output_path)
