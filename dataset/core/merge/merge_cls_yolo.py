import os
import shutil
from tqdm import tqdm

def update_labels(lines, class_mapping):
    return [str(class_mapping[int(line.split()[0])]) + line[line.find(' '):] for line in lines]

def merge_datasets(dataset1_path, dataset2_path, merged_dataset_path, class_mapping, splits=['train', 'test']):
    # 创建新数据集的目录结构
    for split in splits:
        os.makedirs(os.path.join(merged_dataset_path, 'images', split), exist_ok=True)
        os.makedirs(os.path.join(merged_dataset_path, 'labels', split), exist_ok=True)

    # 遍历第一个数据集的标签文件
    for split in splits:
        for label_file in tqdm(os.listdir(os.path.join(dataset1_path, 'labels', split)), desc=f'Processing {split} data'):
            # 读取第一个数据集的标签并更新类别索引
            with open(os.path.join(dataset1_path, 'labels', split, label_file), 'r') as f:
                labels1 = f.readlines()
            labels1 = update_labels(labels1, class_mapping)

            # 查找并读取第二个数据集中相应的标签文件
            labels2_path = os.path.join(dataset2_path, 'labels', split, label_file)
            if os.path.exists(labels2_path):
                with open(labels2_path, 'r') as f:
                    labels2 = f.readlines()
                labels2 = update_labels(labels2, class_mapping)
            else:
                labels2 = []

            # 合并两个标签文件
            merged_labels = labels1 + labels2

            # 复制相关的图像文件到新数据集
            image_file = label_file.replace('.txt', '.jpg')
            src_image_path = os.path.join(dataset1_path, 'images', split, image_file)
            dst_image_path = os.path.join(merged_dataset_path, 'images', split, image_file)

            if os.path.exists(src_image_path):
                shutil.copy(src_image_path, dst_image_path)

            # 将合并后的标签文件写入新数据集
            with open(os.path.join(merged_dataset_path, 'labels', split, label_file), 'w') as f:
                f.writelines(merged_labels)

    print("合并完成！新数据集已保存到：", merged_dataset_path)

# 指定数据集路径
dataset1_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/data5'
dataset2_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/data4'
merged_dataset_path = '/Users/gatilin/PycharmProjects/DatasetMarkerTool/data_merge'

# 类别映射（示例）
class_mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7}

# 合并两个数据集
merge_datasets(dataset1_path, dataset2_path, merged_dataset_path, class_mapping)