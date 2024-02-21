import os
from collections import defaultdict

def analyze_yolo_dataset(dataset_path, classes_to_analyze, splits=['train', 'test']):
    class_counts = defaultdict(int)
    image_counts = defaultdict(int)

    for split in splits:
        split_dir = os.path.join(dataset_path, 'labels', split)
        if not os.path.exists(split_dir):
            print(f"Split '{split}' does not exist in the dataset.")
            continue
        for label_file in os.listdir(split_dir):
            with open(os.path.join(dataset_path, 'labels', split, label_file), 'r') as f:
                lines = f.readlines()

            found_classes = [int(line.split()[0]) for line in lines if int(line.split()[0]) in classes_to_analyze]

            for cls in found_classes:
                class_counts[cls] += 1

            if found_classes:
                for cls in set(found_classes):
                    image_counts[cls] += 1

    print("类别统计：")
    for cls, count in class_counts.items():
        print(f"类别 {cls}: {count} 个标签")

    print("\n图片统计：")
    for cls, count in image_counts.items():
        average_labels = class_counts[cls] / count
        print(f"类别 {cls}: {count} 张图片 (平均每张图片 {average_labels:.2f} 个标签)")

if __name__ == '__main__':
    # 指定数据集路径
    dataset_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/coco128'

    # 指定要分析的类别
    classes_to_analyze = [0, 1, 2, 3]

    # 分析数据集
    analyze_yolo_dataset(dataset_path, classes_to_analyze)