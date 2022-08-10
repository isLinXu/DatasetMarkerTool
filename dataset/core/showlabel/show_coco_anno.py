import albumentations as A
import cv2
import os
import json
import numpy as np

# 定义增强类
class COCOAug(object):

    def __init__(self,
                 anno_path=None,
                 image_path=None,
                 save_image_path=None,
                 anno_mode='train',
                 is_show=True,
                 start_filename_id=None,
                 start_anno_id=None,
                 ):
        """

        :param anno_path: json文件的路径
        :param pre_image_path: 需要增强的图片路径
        :param save_image_path: 保存的图片路径
        :param anno_mode: 有train,val两种, 同时也对应两种路径, 两种json文件[train.json, val.json]
        :param is_show: 是否实时展示: 每增强一张图片就把对应的标注框和标签画出并imshow
        :param start_filename_id: 新的图片起始名称. 同时也对应图片的id, 后续在此基础上依次+1,
                                  如果没有指定则按已有的图片长度继续+1
        :param start_anno_id: 新的注释id起始号, 后续在此基础上依次+1, 如果没有指定则按已有的注释个数长度继续+1
        """
        self.anno_path = anno_path
        self.aug_image_path = image_path
        self.save_image_path = save_image_path
        self.anno_mode = anno_mode
        self.is_show = is_show
        self.start_filename_id = start_filename_id
        self.start_anno_id = start_anno_id

        # 打开json文件
        with open(os.path.join(self.anno_path, f"{self.anno_mode}.json"), 'r', encoding='utf-8') as load_f:
            self.load_dict = json.load(load_f)  # ['images', 'annotations', 'categories']

            self.labels = []  # 读取标签列表
            for anno in self.load_dict['categories']:
                self.labels.append(anno['name'])

            print("--------- * ---------")
            if self.start_filename_id is None:
                self.start_filename_id = len(self.load_dict['images'])
                print("the start_filename_id is not set, default: len(images)")
            if self.start_anno_id is None:
                self.start_anno_id = len(self.load_dict['annotations'])
                print("the start_anno_id is not set, default: len(annotations)")
            print("len(images)     : ", self.start_filename_id)
            print("len(annotations): ", self.start_anno_id)
            print("categories: ", self.load_dict['categories'])
            print("labels: ", self.labels)
            print("--------- * ---------")

    def image_show(self, max_len=4):
        """
        json格式
        "images": [{"file_name": "013856.jpg", "height": 1080, "width": 1920, "id": 13856},...]
        "annotations": [{"image_id": 13856, "id": 0, "category_id": 2, "bbox": [541, 517, 79, 102],
                         "area": 8058, "iscrowd": 0, "segmentation": []}, ...]
        "categories": [{"id": 0, "name": "Motor Vehicle"}, ...]


        :param start_filename_id: 起始图片id号
        :param start_anno_id: 起始注释框id号
        :param max_len: 默认数据集不超过9999, 即: 0000~9999 如果更多可以设置为5 即00000~99999

        :return: None
        """
        # 对每一张图片遍历
        for index, item in enumerate(self.load_dict['images'][:]):
            image_name = item['file_name']
            # print('image_name',image_name)
            image_suffix = image_name.split(".")[-1]  # 获取图片后缀 e.g. [.jpg .png]
            image_id = item['id']

            bboxes_list = []
            category_id_list = []
            # 对每一张图片找到所有的标注框, 并且bbox和label的id要对应上
            for anno in self.load_dict['annotations']:
                if anno['image_id'] == image_id:
                    bboxes_list.append(anno['bbox'])
                    category_id_list.append(anno['category_id'])

            try:
                # 读取图片
                image = cv2.imread(os.path.join(self.aug_image_path, image_name))
                h, w = image.shape[:2]
                # 生成图片的anno字典
                aug_anno = {'image': image, 'height': h, 'width': w, 'bboxes': bboxes_list, 'category_id': category_id_list}

                # 对增强后的bbox取整
                for index, bbox in enumerate(bboxes_list):
                    x, y, w, h = bbox
                    bboxes_list[index] = [int(x + 0.5), int(y + 0.5), int(w + 0.5), int(h + 0.5)]

                # 是否进行实时展示图片, 用于检测是否有误
                if self.is_show:
                    tl = 2
                    image_copy = image
                    for bbox, category_id in zip(bboxes_list, category_id_list):
                        text = f"{self.labels[category_id]}"
                        t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tl)[0]
                        cv2.rectangle(image_copy, (bbox[0], bbox[1] - 3),
                                      (bbox[0] + t_size[0], bbox[1] - t_size[1] - 3),
                                      (0, 0, 255), -1, cv2.LINE_AA)  # filled
                        cv2.putText(image_copy, text, (bbox[0], bbox[1] - 2), 0, tl / 3, (255, 255, 255), tl,
                                    cv2.LINE_AA)
                        aug_image_show = cv2.rectangle(image_copy, (bbox[0], bbox[1]),
                                                       (bbox[0] + bbox[2], bbox[1] + bbox[3]),
                                                       (255, 255, 0), 2)

                    cv2.imshow('image_show', aug_image_show)

                    # 实时检测增强后的标注框是否有较大偏差, 符合要求按下's'健保存, 其他键跳过
                    key = cv2.waitKey(0)
                    # 按下s键保存增强，否则取消保存此次增强
                    if key & 0xff == ord('s'):
                        pass
                    else:
                        # cv2.destroyWindow(f'aug_image_show')
                        continue
                    # cv2.destroyWindow(f'aug_image_show')
            except:
                pass



if __name__ == '__main__':
    # 对示例数据集进行增强, 运行成功后会在相应目录下保存
    # dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/coco128/coco_img/000000000009.jpg'
    # img = cv2.imread(dir)
    # print(img)
    # 图片路径
    IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/coco128/val2017/'
    SAVE_IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/coco128/coco_img/'

    # anno路径
    ANNO_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/coco128/annotations'
    # mode = 'val'  # ['train', 'val']
    mode = 'instances_val'

    aug = COCOAug(
        anno_path=ANNO_PATH,
        image_path=IMAGE_PATH,
        save_image_path=SAVE_IMAGE_PATH,
        anno_mode=mode,
        is_show=True,
    )
    # aug.image_aug()
    aug.image_show()
