import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# 读取图像和标注文件
def read_yolo_dataset(image_dir, label_dir, class_names):
    data = []
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(image_dir, filename)
            label_path = os.path.join(label_dir, os.path.splitext(filename)[0] + ".txt")
            if os.path.exists(label_path):
                with open(label_path, "r") as f:
                    labels = [line.strip().split() for line in f.readlines()]
                    data.append({"image_path": img_path, "labels": labels})
    return data

# 将 YOLO 格式的边界框转换为 OpenCV 格式
def yolo_to_opencv_bbox(yolo_bbox, img_width, img_height):
    x_center, y_center, width, height = map(float, yolo_bbox)
    x_min = int((x_center - width / 2) * img_width)
    y_min = int((y_center - height / 2) * img_height)
    x_max = int((x_center + width / 2) * img_width)
    y_max = int((y_center + height / 2) * img_height)
    return [x_min, y_min, x_max, y_max]

# 可视化图像和边界框
def visualize_bbox(image, labels, class_names):
    for label in labels:
        class_id, *yolo_bbox = label
        class_id = int(class_id)
        class_name = class_names[class_id]
        bbox = yolo_to_opencv_bbox(yolo_bbox, image.shape[1], image.shape[0])
        cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(image, class_name, (bbox[0], bbox[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

# 分析数据集
def analyze_dataset(data, class_names):
    class_count = defaultdict(int)
    for item in data:
        for label in item["labels"]:
            class_id = int(label[0])
            class_count[class_names[class_id]] += 1
    return class_count

# 示例
image_dir = "/Users/gatilin/Downloads/coco128/images/train2017"
label_dir = "/Users/gatilin/Downloads/coco128/labels/train2017"
# class_names = ["class1", "class2", "class3"]
class_names =  [ 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
         'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
         'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
         'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
         'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
         'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
         'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
         'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
         'hair drier', 'toothbrush']

data = read_yolo_dataset(image_dir, label_dir, class_names)
print(f"数据集大小：{len(data)}")

# 可视化示例
sample = data[0]
image = cv2.imread(sample["image_path"])
visualize_bbox(image, sample["labels"], class_names)

# 数据集分析
class_count = analyze_dataset(data, class_names)
print("类别统计：")
for class_name, count in class_count.items():
    print(f"{class_name}: {count}")