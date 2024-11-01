import cv2
import numpy as np
import json
import argparse
import os
from tqdm import tqdm
from PIL import Image, ImageDraw, ImageFont


def visualize_coco(images_folder, coco_path, output_folder):
    # 读取COCO JSON文件
    with open(coco_path, 'r') as f:
        coco_data = json.load(f)

    # 获取图像ID和文件名的映射
    image_id_to_filename = {image['id']: image['file_name'] for image in coco_data['images']}

    # 遍历每个图像ID
    for image_id, image_filename in tqdm(image_id_to_filename.items(), desc='Processing images'):
        image_path = os.path.join(images_folder, image_filename)
        print("image_filename:", image_filename)
        # 读取图片
        image = cv2.imread(image_path)

        # 检查图像是否成功加载
        if image is None:
            print(f"Error: Unable to load image at {image_path}")
            continue

        # 提取标签名和边界框
        for annotation in coco_data['annotations']:
            if annotation['image_id'] != image_id:
                continue

            label_id = annotation['category_id']
            label_name = None
            for category in coco_data['categories']:
                if category['id'] == label_id:
                    label_name = category['name']
                    break

            bbox = annotation['bbox']
            if bbox:
                x, y, w, h = [int(coord) for coord in bbox]
                print("label_name:", label_name, "bbox:", bbox)

                # 在图片上绘制边界框和标签名
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 使用PIL库绘制中文字符
                pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_image)
                # font = ImageFont.truetype("simhei.ttf", 20) # 使用适当的字体文件，例如simhei.ttf
                font = ImageFont.truetype("./SimHei.ttf",
                                          20)
                draw.text((x, y - 20), label_name, font=font, fill=(0, 255, 0, 0))
                image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        # 保存可视化结果
        output_path = os.path.join(output_folder, image_filename)
        # 确保输出子目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Visualize COCO JSON annotations on images in a folder')
    parser.add_argument('images_folder', type=str, help='Path to the folder containing the image files')
    parser.add_argument('coco_path', type=str, help='Path to the COCO JSON file')
    parser.add_argument('output_folder', type=str, help='Path to the folder to save the visualization results')

    args = parser.parse_args()
    visualize_coco(args.images_folder, args.coco_path, args.output_folder)