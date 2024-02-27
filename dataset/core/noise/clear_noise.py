import os
import cv2
import imagehash
from PIL import Image
from tqdm import tqdm

def process_images(input_folder, output_folder, hash_threshold=5):
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取输入文件夹中的所有图片文件
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

    # 保存已处理过的图片哈希值
    processed_hashes = set()

    # 处理图片并显示进度
    for image_file in tqdm(image_files, desc="处理进度"):
        image_path = os.path.join(input_folder, image_file)

        # 读取图片
        image = cv2.imread(image_path)

        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 去噪
        denoised = cv2.fastNlMeansDenoising(gray, h=30, templateWindowSize=7, searchWindowSize=21)

        # 保存去噪后的图片
        denoised_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(denoised_image_path, denoised)

        # 计算图片哈希值
        img_hash = imagehash.average_hash(Image.open(denoised_image_path))

        # 判断图片是否重复
        is_duplicate = any(abs(img_hash - processed_hash) < hash_threshold for processed_hash in processed_hashes)

        if is_duplicate:
            # 如果图片重复，则删除
            os.remove(denoised_image_path)
        else:
            # 如果图片不重复，则将其哈希值添加到已处理哈希值集合中
            processed_hashes.add(img_hash)

    print("处理完成，共处理了 {} 张图片，去重后剩余 {} 张图片。".format(len(image_files), len(processed_hashes)))


if __name__ == "__main__":
    input_folder = "/Users/gatilin/PycharmProjects/smart-spider/电瓶车"
    output_folder = "/Users/gatilin/PycharmProjects/smart-spider/电瓶车_clear"
    process_images(input_folder, output_folder)