import json
import os
import shutil
from tqdm import tqdm

def extract_category(input_json_path, output_json_path, original_images_dir, new_images_dir, target_category_id):
    with open(input_json_path, 'r') as f:
        data = json.load(f)

    # 初始化一个新的JSON数据结构
    new_data = {}

    # 如果输入数据中存在相应字段，则将其添加到新数据结构中
    if "info" in data:
        new_data["info"] = data["info"]
    if "licenses" in data:
        new_data["licenses"] = data["licenses"]
    if "categories" in data:
        new_data["categories"] = data["categories"]

    new_data["images"] = []
    new_data["annotations"] = []

    # 保存已处理的图像ID，避免重复添加
    processed_image_ids = set()

    # 遍历每个标注，使用tqdm显示进度
    for annotation in tqdm(data["annotations"], desc="Processing annotations"):
        # 如果标注的类别与目标类别相匹配
        if annotation["category_id"] == target_category_id:
            # 将标注添加到新的JSON数据结构中
            new_data["annotations"].append(annotation)

            # 如果图像ID尚未处理，将对应的图像添加到新的JSON数据结构中，并复制图片文件
            image_id = annotation["image_id"]
            if image_id not in processed_image_ids:
                image = next(image for image in data["images"] if image["id"] == image_id)
                new_data["images"].append(image)
                processed_image_ids.add(image_id)

                # 复制图片文件
                original_image_path = os.path.join(original_images_dir, image["file_name"])
                new_image_path = os.path.join(new_images_dir, image["file_name"])

                # 检查new_images_dir是否存在，如果不存在，则创建目录
                if not os.path.exists(new_images_dir):
                    os.makedirs(new_images_dir)
                if os.path.exists(original_image_path):
                    shutil.copy(original_image_path, new_image_path)
                else:
                    continue
                # shutil.copy(original_image_path, new_image_path)

    # 将新的JSON数据结构保存到文件中
    with open(output_json_path, 'w') as f:
        json.dump(new_data, f)

# 示例用法
input_json_path = "your_input_coco_json_file.json"
output_json_path = "your_output_coco_json_file.json"
original_images_dir = "path_to_your_original_images"
new_images_dir = "path_to_your_new_images"
target_category_id = 3  # 要提取的类别ID

extract_category(input_json_path, output_json_path, original_images_dir, new_images_dir, target_category_id)