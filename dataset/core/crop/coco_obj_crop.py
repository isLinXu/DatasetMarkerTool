import os
import json
import cv2
from tqdm import tqdm
def crop_coco_images(coco_images_dir, coco_annotations_file, output_dir):
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 加载 COCO 标注文件
    with open(coco_annotations_file, 'r') as f:
        coco_annotations = json.load(f)

    # 创建类别目录
    categories = {cat['id']: cat['name'] for cat in coco_annotations['categories']}
    for cat_name in categories.values():
        os.makedirs(os.path.join(output_dir, cat_name), exist_ok=True)

    # 遍历标注文件，裁剪并保存目标区域
    for ann in tqdm(coco_annotations['annotations'], desc="Processing annotations"):
        image_id = ann['image_id']
        category_id = ann['category_id']
        bbox = ann['bbox']

        # 获取图像路径
        image_info = next((img for img in coco_annotations['images'] if img['id'] == image_id), None)
        if image_info is None:
            continue
        image_path = os.path.join(coco_images_dir, image_info['file_name'])

        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            continue

        # 裁剪目标区域
        x, y, w, h = map(int, bbox)
        cropped_image = image[y:y + h, x:x + w]

        # 检查裁剪后的图像是否为空，如果为空则跳过保存
        if cropped_image is None or cropped_image.size == 0:
            continue

        # 获取类别名称并检查目录是否存在，如果不存在则创建
        category_name = categories[category_id]
        category_path = os.path.join(output_dir, category_name)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        # 保存裁剪后的图像
        output_path = os.path.join(category_path, f"{image_id}_{ann['id']}.jpg")
        success = cv2.imwrite(output_path, cropped_image)

        # 确认图像已成功保存
        if success:
            print(f"Image saved at {output_path}")
        else:
            print(f"Failed to save image at {output_path}")

if __name__ == '__main__':
    # 示例用法
    coco_images_dir = 'path/to/coco/images'
    coco_annotations_file = 'path/to/coco/annotations/instances_train2017.json'
    output_dir = 'path/to/output/dataset'
    crop_coco_images(coco_images_dir, coco_annotations_file, output_dir)