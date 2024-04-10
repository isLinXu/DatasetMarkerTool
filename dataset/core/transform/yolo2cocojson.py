
import os
import json
from tqdm import tqdm
from PIL import Image

# 定义一些全局变量
label_map_path = 'path/to/label_map.txt'  # 标签映射文件的路径
output_file_path = 'path/to/output/coco_annotations.json'  # 输出JSON文件的完整路径
yolo_label_dir = 'path/to/yolo/labels'    # YOLO标签文件的目录
image_dir = 'path/to/images'              # 图片文件的目录

# 读取标签映射文件，建立类别名称与ID的映射
def read_label_map(label_map_file):
    label_map = {}
    with open(label_map_file, 'r') as f:
        for line in f:
            category, id = line.strip().split(',')
            label_map[id] = category
    return label_map


# 解析YOLO标签文件并转换为COCO格式
def convert_yolo_to_coco(yolo_label_dir, image_dir, label_map):
    coco_data = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    # image_id = 0
    # annotation_id = 0
    image_id = 1
    annotation_id = 1

    # 读取所有YOLO标签文件
    # for file in os.listdir(yolo_label_dir):
    files = os.listdir(yolo_label_dir)
    files = tqdm(files, desc='Processing files', unit='file')
    # 读取所有YOLO标签文件
    # for file in os.listdir(yolo_label_dir):
    for file in files:
        if file.endswith('.txt'):
            image_filename = os.path.splitext(file)[0] + '.jpg'  # 假设图片和标签文件同名
            image_path = os.path.join(image_dir, image_filename)
            yolo_path = os.path.join(yolo_label_dir, file)

            # 检查图片文件是否存在
            if not os.path.isfile(image_path):
                print(f"Warning: Image file {image_path} does not exist. Skipping this file.")
                continue

            # 使用Pillow获取图片尺寸
            try:
                with Image.open(image_path) as img:
                    width, height = img.size
            except IOError:
                print(f"Warning: Unable to open image file {image_path}. Skipping this file.")
                continue

            # 读取YOLO标签
            with open(yolo_path, 'r') as f:
                lines = f.readlines()

            for line in lines:
                if len(line.strip()) > 0:
                    values = line.strip().split(' ')
                    if len(values) == 5:  # 确保列表有5个值
                        category_id = int(values[0])
                        bbox = [float(values[1]), float(values[2]), float(values[3]), float(values[4])]
                        bbox[0] *= width
                        bbox[1] *= height
                        bbox[2] *= width
                        bbox[3] *= height
                        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                        annotation = {
                            "id": annotation_id,
                            "image_id": image_id,
                            "category_id": category_id,
                            "bbox": bbox,
                            "area": area,
                            "iscrowd": 0
                        }
                        coco_data["annotations"].append(annotation)
                        annotation_id += 1

            # 添加图片信息
            coco_data["images"].append({
                "id": image_id,
                "file_name": image_filename,
                "width": width,
                "height": height
            })
            image_id += 1

    # 添加类别信息
    for category_id, category_name in label_map.items():
        coco_data["categories"].append({
            "id": category_id,
            "name": category_name,
            "supercategory": "object"
        })

    return coco_data


# 主函数
def main():
    # 读取标签映射
    label_map = read_label_map(label_map_path)

    # 执行转换
    coco_data = convert_yolo_to_coco(yolo_label_dir, image_dir, label_map)

    # 保存为JSON文件
    with open(output_file_path, 'w') as f:
        json.dump(coco_data, f, indent=4)

    # 打印完成信息
    print(f"COCO annotations have been saved to {output_file_path}")


if __name__ == "__main__":
    main()