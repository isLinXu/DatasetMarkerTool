from __future__ import print_function
import argparse
import glob
import os
import json
from tqdm import tqdm

def coco2yolo(path,output_path):
    '''
    """
    :param path: json文件路径
    :param output_path: txt文件保存路径
    :return:
    '''
    # os.path.join 合并路径
    # glob.glob 获取所有匹配的路径
    json_files = sorted(glob.glob(os.path.join(path, '*.json')))  # 得到json文件路径下的所有json文件


    # for i in tqdm(range(0, len(json_files))):
    # for i in tqdm(range(0, len(json_files))):
    #    json_file = json_files[i]
    for json_file in json_files:
        with open(json_file) as f:
            data = json.load(f)  # 将json文件转化为字典
            images = data['images']
            annotations = data['annotations']

            # 图片w h，为归一化作准备
            width = 500.0
            height = 500.0

            for i in tqdm(range(0, len(images))):
                converted_results = []
                for ann in annotations:
                    if ann['image_id'] == i and ann['category_id'] <= 6:  # FLIR数据集中只有1-3
                        cat_id = int(ann['category_id'])

                        # letf top为左下角坐标 bbox_width bbox_height为目标框长宽
                        # 将bbox数值转化为float类型
                        left, top, bbox_width, bbox_height = map(float, ann['bbox'])

                        # Yolo的id从0开始，FILIR从1开始
                        cat_id -= 1

                        # 求中心点坐标
                        x_center, y_center = (
                            left + bbox_width / 2, top + bbox_height / 2)

                        # 归一化
                        x_rel, y_rel = (x_center / width, y_center / height)
                        w_rel, h_rel = (bbox_width / width, bbox_height / height)
                        converted_results.append(
                            (cat_id, x_rel, y_rel, w_rel, h_rel))

                image_name = images[i]['file_name']

                # 这里image_name是thermal_8_bit/FLIR_xxxxx.jpeg格式,我们文件名只需要FLIR_xxxxx部分
                image_name = image_name[:-4]

                print(image_name)  # 验证是名称否正确

                file = open(output_path + str(image_name) + '.txt', 'w+')
                file.write('\n'.join('%d %.6f %.6f %.6f %.6f' % res for res in converted_results))
                file.close()




if __name__ == '__main__':
    path = '/media/hxzh02/SB@home/hxzh/Yolov8_Efficient/data/datasets/coco/annotations'

    output_path = '/media/hxzh02/SB@home/hxzh/Yolov8_Efficient/data/datasets/coco/'
    coco2yolo(path, output_path)