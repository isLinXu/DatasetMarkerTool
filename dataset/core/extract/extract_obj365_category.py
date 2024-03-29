import json
import os
import shutil
from tqdm import tqdm

def extract_object365_data(object365_dir, output_dir, category_dict):
    # 读取Object365数据集文件
    with open(os.path.join(object365_dir, 'objects365_train.json'), 'r') as f:
        object365_data = json.load(f)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)

    # 遍历所有的图像
    for image in tqdm(object365_data['images'], desc='Processing images'):
        # 判断图像中是否包含指定的类别
        has_category = False
        for annotation in image['objects']:
            if annotation['class'] in category_dict.keys():
                has_category = True
                break

        # 如果图像中包含指定的类别，则复制图像和标注数据到输出目录
        if has_category:
            image_file = os.path.join(object365_dir, 'train', image['file_name'])
            output_image_file = os.path.join(output_dir, 'images', image['file_name'])
            shutil.copy(image_file, output_image_file)

            output_label_file = os.path.join(output_dir, 'labels', os.path.splitext(image['file_name'])[0] + '.txt')
            with open(output_label_file, 'w') as f:
                for annotation in image['objects']:
                    if annotation['class'] in category_dict.keys():
                        category_index = category_dict[annotation['class']]
                        bbox = annotation['bbox']
                        x_center = bbox[0] + bbox[2] / 2
                        y_center = bbox[1] + bbox[3] / 2
                        width = bbox[2]
                        height = bbox[3]
                        f.write('{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}\n'.format(category_index, x_center, y_center, width, height))

    print('数据集提取完成！')

# 测试代码
object365_dir = 'path/to/object365'
output_dir = 'path/to/output'
category_dict = {'person': 0, 'car': 1, 'bus': 2, 'truck': 3}  # 指定要抽取的类别和对应的类别索引
extract_object365_data(object365_dir, output_dir, category_dict)