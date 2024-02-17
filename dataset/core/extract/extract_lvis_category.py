import csv
import json
import os
import shutil
from tqdm import tqdm
from urllib.parse import urlparse


def extract_filename(url):
    parsed_url = urlparse(url)
    return parsed_url.path.split('/')[-1]


def extract_lvis_data(lvis_file, img_dir, output_dir, category_dict):
    with open(lvis_file, 'r') as f:
        lvis_data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)

    # 创建一个字典，将category_id映射到类别名称
    category_id_to_name = {}
    for category in lvis_data['categories']:
        category_id_to_name[category['id']] = category['name']

    for image in tqdm(lvis_data['images'], desc='Processing images'):
        has_category = False
        for annotation in lvis_data['annotations']:
            category_id = annotation['category_id']
            if category_id in category_id_to_name:
                category = category_id_to_name[category_id]
                if category in category_dict.keys():
                    has_category = True
                    break
            else:
                print(f"Category ID {category_id} is out of range.")

        if has_category:
            # dir_name = 'train'
            # images_dir = img_dir + '/train2017'
            dir_name = 'val'
            images_dir = img_dir + '/val2017'
            file_name = extract_filename(image['coco_url'])
            image_file = os.path.join(images_dir, file_name)
            output_image_dir = os.path.join(output_dir, 'images', dir_name)
            output_image_file = os.path.join(output_image_dir, file_name)

            # shutil.copy(image_file, output_image_file)
            # 检查 image_file 是否存在
            if os.path.exists(image_file):
                # 检查 output_image_file 是否存在
                if os.path.exists(output_image_file):
                    print("Both files exist. Copying...")
                    shutil.copy(image_file, output_image_file)
                else:
                    print("output_image_file does not exist.")
            else:
                print("image_file does not exist.")
            output_label_dir = os.path.join(output_dir, 'labels', dir_name)
            output_label_file = os.path.join(output_label_dir, os.path.splitext(file_name)[0] + '.txt')

            with open(output_label_file, 'w') as f:
                for annotation in lvis_data['annotations']:
                    if annotation['image_id'] == image['id']:
                        category = category_id_to_name[annotation['category_id']]
                        if category in category_dict.keys():
                            category_index = category_dict[category]
                            bbox = annotation['bbox']
                            x_center = bbox[0] + bbox[2] / 2
                            y_center = bbox[1] + bbox[3] / 2
                            width = bbox[2]
                            height = bbox[3]
                            x_center_normalized = x_center / image['width']
                            y_center_normalized = y_center / image['height']
                            width_normalized = width / image['width']
                            height_normalized = height / image['height']
                            f.write('{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}\n'.format(category_index, x_center_normalized,
                                                                                   y_center_normalized,
                                                                                   width_normalized, height_normalized))

    print('数据集提取完成！')


def read_csv(file_name):
    result = {}
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            result[row[0].strip()] = int(row[1].strip())
    return result


# lvis_file = '/svap_storage/dataset/SVAP_Research_Datasets/opendatalab/OpenDataLab___LVIS_v1_dot_0/raw/annotations/lvis_v1_train.json'
lvis_file = '/svap_storage/dataset/SVAP_Research_Datasets/opendatalab/OpenDataLab___LVIS_v1_dot_0/raw/annotations/lvis_v1_val.json'
img_dir = '/svap_storage/dataset/SVAP_Research_Datasets/opendatalab/OpenDataLab___LVIS_v1_dot_0/raw/'
output_dir = '/svap_storage/dataset/SVAP_Research_Datasets/lvis_datasets_v1_yolo'

category_dict = read_csv('/svap_storage/gatilin/workspaces/toolbox/extract/lvis_v1_data_csv.csv')
print(category_dict)

extract_lvis_data(lvis_file, img_dir, output_dir, category_dict)