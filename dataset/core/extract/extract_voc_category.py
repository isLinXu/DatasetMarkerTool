import os
import shutil
from tqdm import tqdm
from xml.etree import ElementTree

def extract_voc_data(voc_dir, output_dir, category_dict):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'images', 'val'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'train'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels', 'val'), exist_ok=True)

    # 遍历所有的图像
    for image_file in tqdm(os.listdir(os.path.join(voc_dir, 'JPEGImages')), desc='Processing images'):
        # 读取图像文件和对应的标注文件
        image_id = os.path.splitext(image_file)[0]
        image_file = os.path.join(voc_dir, 'JPEGImages', image_file)
        annotation_file = os.path.join(voc_dir, 'Annotations', image_id + '.xml')

        # 解析标注文件，获取物体的类别、边界框等信息
        tree = ElementTree.parse(annotation_file)
        root = tree.getroot()
        objects = root.findall('object')
        bboxes = []
        for obj in objects:
            name = obj.find('name').text
            if name in category_dict.keys():
                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                bboxes.append((category_dict[name], xmin, ymin, xmax, ymax))

        # 如果图像中包含指定的类别，则复制图像和标注数据到输出目录
        if len(bboxes) > 0:
            output_image_dir = os.path.join(output_dir, 'images', 'train' if root.find('split').text == 'train' else 'val')
            output_image_file = os.path.join(output_image_dir, image_file.split('/')[-1])
            shutil.copy(image_file, output_image_file)

            output_label_dir = os.path.join(output_dir, 'labels', 'train' if root.find('split').text == 'train' else 'val')
            output_label_file = os.path.join(output_label_dir, os.path.splitext(image_id)[0] + '.txt')
            with open(output_label_file, 'w') as f:
                for bbox in bboxes:
                    f.write('{0} {1:.6f} {2:.6f} {3:.6f} {4:.6f}\n'.format(*bbox_to_yolo(bbox, root.find('size'))))

    print('数据集提取完成！')

# 将VOC格式的边界框转换为yolo格式的边界框
def bbox_to_yolo(bbox, size):
    category_index, xmin, ymin, xmax, ymax = bbox
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    x_center = (xmin + xmax) / 2 / width
    y_center = (ymin + ymax) / 2 / height
    bbox_width = (xmax - xmin) / width
    bbox_height = (ymax - ymin) / height
    return (category_index, x_center, y_center, bbox_width, bbox_height)

# 测试代码
voc_dir = 'path/to/voc2012'
output_dir = 'path/to/output'
category_dict = {'person': 0, 'car': 1, 'bus': 2, 'truck': 3}  # 指定要抽取的类别和对应的类别索引
extract_voc_data(voc_dir, output_dir, category_dict)