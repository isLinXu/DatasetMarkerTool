import json
import os
import shutil
from tqdm import tqdm

def extract_categories(input_json_path, output_json_path, original_images_dir, new_images_dir, target_category_ids):
    with open(input_json_path, 'r') as f:
        data = json.load(f)

    new_data = {}

    if "info" in data:
        new_data["info"] = data["info"]
    if "licenses" in data:
        new_data["licenses"] = data["licenses"]
    if "categories" in data:
        new_data["categories"] = data["categories"]

    new_data["images"] = []
    new_data["annotations"] = []

    processed_image_ids = set()

    for annotation in tqdm(data["annotations"], desc="Processing annotations"):
        if annotation["category_id"] in target_category_ids:
            new_data["annotations"].append(annotation)

            image_id = annotation["image_id"]
            if image_id not in processed_image_ids:
                image = next(image for image in data["images"] if image["id"] == image_id)
                new_data["images"].append(image)
                processed_image_ids.add(image_id)

                original_image_path = os.path.join(original_images_dir, image["file_name"])
                new_image_path = os.path.join(new_images_dir, image["file_name"])

                if not os.path.exists(new_images_dir):
                    os.makedirs(new_images_dir)
                if os.path.exists(original_image_path):
                    shutil.copy(original_image_path, new_image_path)
                else:
                    continue

    with open(output_json_path, 'w') as f:
        json.dump(new_data, f)

# 示例用法
input_json_path = "your_input_coco_json_file.json"
output_json_path = "your_output_coco_json_file.json"
original_images_dir = "path_to_your_original_images"
new_images_dir = "path_to_your_new_images"
target_category_ids = [3, 5, 7]  # 要提取的类别ID列表

extract_categories(input_json_path, output_json_path, original_images_dir, new_images_dir, target_category_ids)