
import os
from collections import defaultdict
from tqdm import tqdm

def analyze_yolo_dataset(dataset_path, classes_to_analyze, class_names=None, splits=['train', 'test']):
    class_counts = defaultdict(int)
    image_counts = defaultdict(int)
    total_images = 0

    if not os.path.exists(dataset_path):
        print(f"Dataset path '{dataset_path}' does not exist.")
        return

    for split in splits:
        split_dir = os.path.join(dataset_path, 'labels', split)
        if not os.path.exists(split_dir):
            print(f"Split '{split}' does not exist in the dataset.")
            continue

        for label_file in tqdm(os.listdir(split_dir), desc=f"Processing {split} data"):
            with open(os.path.join(dataset_path, 'labels', split, label_file), 'r') as f:
                lines = f.readlines()

            found_classes = [int(line.split()[0]) for line in lines if int(line.split()[0]) in classes_to_analyze]

            for cls in found_classes:
                class_counts[cls] += 1

            if found_classes:
                for cls in set(found_classes):
                    image_counts[cls] += 1
            total_images += 1

    print("类别统计：")
    for cls, count in class_counts.items():
        class_name = class_names[cls] if class_names else cls
        print(f"类别 {class_name}: {count} 个标签")

    print("\n图片统计：")
    for cls, count in image_counts.items():
        class_name = class_names[cls] if class_names else cls
        average_labels = class_counts[cls] / count
        print(f"类别 {class_name}: {count} 张图片 (平均每张图片 {average_labels:.2f} 个标签)")

    print(f"\n总图片数量：{total_images}")

if __name__ == '__main__':
    # 指定数据集路径
    dataset_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128'

    # 指定要分析的类别
    classes_to_analyze = [0, 1, 2, 3]

    # 类别名称（可选）
    # class_names = None
    class_names = {
        0: 'person',
        1: 'bicycle',
        2: 'car',
        3: 'motorcycle',
    }

    # 分析数据集
    analyze_yolo_dataset(dataset_path, classes_to_analyze, class_names)
