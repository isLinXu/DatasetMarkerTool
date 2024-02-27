import os
import shutil

from tqdm import tqdm

def extract_classes(src_dataset_path, new_dataset_path, classes_to_extract, original_classes, splits=['train','test']):
    # 计算类别标签
    classes_to_extract_ids = [original_classes.index(cls) for cls in classes_to_extract]

    # 创建新数据集的目录结构
    for split in splits:
        os.makedirs(os.path.join(new_dataset_path, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(new_dataset_path, 'labels', split), exist_ok=True)

    # 遍历源数据集的标签文件
    for split in splits:
        split_dir = os.path.join(src_dataset_path, 'labels', split)
        if not os.path.exists(split_dir):
            continue
        for label_file in tqdm(os.listdir(split_dir), desc=f'Processing {split} data'):
            with open(os.path.join(src_dataset_path, 'labels', split, label_file), 'r') as f:
                lines = f.readlines()

            # 检查并提取包含指定类别的标签，同时更新类别索引
            new_lines = []
            for line in lines:
                cls_id = int(line.split()[0])
                if cls_id in classes_to_extract_ids:
                    new_cls_id = classes_to_extract_ids.index(cls_id)
                    new_line = line.replace(str(cls_id), str(new_cls_id), 1)
                    new_lines.append(new_line)

            if new_lines:
                # 复制相关的图像文件到新数据集
                image_file = label_file.replace('.txt', '.jpg')
                src_image_path = os.path.join(src_dataset_path, 'images', split, image_file)
                if os.path.exists(src_image_path):
                    dst_image_path = os.path.join(new_dataset_path, 'images', split, image_file)
                    shutil.copy(src_image_path, dst_image_path)

                # 将新的标签文件写入新数据集
                with open(os.path.join(new_dataset_path, 'labels', split, label_file), 'w') as f:
                    f.writelines(new_lines)

    print("提取完成！新数据集已保存到：", new_dataset_path)

if __name__ == '__main__':
    # 指定源数据集路径和新数据集路径
    src_dataset_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128'
    new_dataset_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/data6'
    # 原始数据集的类别列表
    coco_classes = [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
        'fire hydrant','stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
        'zebra','giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass',
        'cup','fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
        'pizza','donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
        'remote','keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
        'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]
    original_classes = coco_classes
    # 指定要提取的类别
    classes_to_extract = ['person', 'car', 'bus', 'truck', 'motorcycle', 'bicycle']
    extract_classes(src_dataset_path, new_dataset_path, classes_to_extract, original_classes)