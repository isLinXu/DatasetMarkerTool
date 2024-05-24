import albumentations as A
import cv2
import os
import json
import numpy as np


class YOLOAug(object):
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.pre_image_path = config['pre_image_path']
        self.pre_label_path = config['pre_label_path']
        self.aug_save_image_path = config['aug_save_image_path']
        self.aug_save_label_path = config['aug_save_label_path']
        self.labels = config['labels']
        self.is_show = config['is_show']
        self.start_filename_id = config['start_filename_id']
        self.max_len = config['max_len']

        # 数据增强选项
        augmentation_params = config['augmentation_params']
        self.aug = A.Compose([
            # 随机改变图像的亮度、对比度、饱和度、色调
            A.RandomBrightnessContrast(brightness_limit=augmentation_params['brightness_limit'],
                                       contrast_limit=augmentation_params['contrast_limit'],
                                       p=1),
            # 高斯滤波
            A.GaussianBlur(p=augmentation_params['gaussian_blur_p']),
            # 高斯模糊
            A.GaussNoise(p=augmentation_params['gauss_noise_p']),
            # 直方图均衡
            A.CLAHE(clip_limit=augmentation_params['clahe_clip_limit'],
                    tile_grid_size=augmentation_params['clahe_tile_grid_size'],
                    p=augmentation_params['clahe_p']),
            # 均衡图像直方图
            A.Equalize(p=augmentation_params['equalize_p']),
            # 随机水平翻转
            A.HorizontalFlip(p=augmentation_params['horizontal_flip_p']),
            # 随机选择一个增强方式
            A.OneOf([
                # 随机改变图像的亮度、对比度、饱和度、色调
                A.RGBShift(r_shift_limit=augmentation_params['rgb_shift_limit'],
                           g_shift_limit=augmentation_params['rgb_shift_limit'],
                           b_shift_limit=augmentation_params['rgb_shift_limit'],
                           p=augmentation_params['channel_shuffle_p']),
                # 随机排列通道
                A.ChannelShuffle(p=augmentation_params['channel_shuffle_p']),
                # 随机改变图像的亮度、对比度、饱和度、色调
                A.ColorJitter(p=augmentation_params['color_jitter_p']),
                # 随机丢弃通道
                A.ChannelDropout(p=augmentation_params['channel_dropout_p']),
            ], p=augmentation_params['downscale_p']),
            # 随机缩小和放大来降低图像质量
            A.Downscale(p=augmentation_params['downscale_p']),
            # 压印输入图像并将结果与原始图像叠加
            A.Emboss(p=augmentation_params['emboss_p']),
        ],
            # 经过归一化
            # min_area: 表示bbox占据的像素总个数, 当数据增强后, 若bbox小于这个值则从返回的bbox列表删除该bbox.
            # min_visibility: 值域为[0,1], 如果增强后的bbox面积和增强前的bbox面积比值小于该值, 则删除该bbox
            A.BboxParams(format='yolo', min_area=augmentation_params['min_area'],
                         min_visibility=augmentation_params['min_visibility'], label_fields=['category_id'])
        )

        if not os.path.exists(self.aug_save_image_path):
            os.makedirs(self.aug_save_image_path)
        if not os.path.exists(self.aug_save_label_path):
            os.makedirs(self.aug_save_label_path)

        print("--------*--------")
        image_len = len(os.listdir(self.pre_image_path))
        print("the length of images: ", image_len)
        if self.start_filename_id is None:
            print("the start_filename id is not set, default: len(image)", image_len)
            self.start_filename_id = image_len

        print("--------*--------")

    def get_data(self, image_name):
        """
        获取图片和对应的label信息

        :param image_name: 图片文件名, e.g. 0000.jpg
        :return:
        """
        image = cv2.imread(os.path.join(self.pre_image_path, image_name))

        pre_img_label_path = os.path.join(self.pre_label_path, image_name.split('.')[0] + '.txt')
        if os.path.exists(pre_img_label_path):
            with open(pre_img_label_path, 'r', encoding='utf-8') as f:
                label_txt = f.readlines()

            label_list = []
            cls_id_list = []
            for label in label_txt:
                label_info = label.strip().split(' ')
                cls_id_list.append(int(label_info[0]))
                label_list.append([float(x) for x in label_info[1:]])
                # print(label_info[1:])

            anno_info = {'image': image, 'bboxes': label_list, 'category_id': cls_id_list}
            return anno_info

    def aug_image(self):
        '''
        :param is_show: 是否实时展示: 每增强一张图片就把对应的标注框和标签画出并imshow

        Returns:
        '''
        image_list = os.listdir(self.pre_image_path)

        file_name_id = self.start_filename_id
        for image_filename in image_list[:]:
            image_suffix = image_filename.split('.')[-1]
            # 部分环境下会存在.ipynb_checkpoints文件, 为了不报错, 根据文件后缀过滤
            if image_suffix not in ['jpg', 'png']:
                continue

            aug_anno = self.get_data(image_filename)

            # 获取增强后的信息
            try:
                aug_info = self.aug(**aug_anno)  # {'image': , 'bboxes': , 'category_id': }
                aug_image = aug_info['image']
                aug_bboxes = aug_info['bboxes']
                aug_category_id = aug_info['category_id']

                name = '0' * self.max_len
                cnt_str = str(file_name_id)
                length = len(cnt_str)
                new_image_filename = name[:-length] + cnt_str + f'.{image_suffix}'
                new_label_filename = name[:-length] + cnt_str + '.txt'
                print(f"aug_image_{new_image_filename}: ")

                aug_image_copy = aug_image.copy()
                for cls_id, bbox in zip(aug_category_id, aug_bboxes):
                    print(f" --- --- cls_id: ", cls_id)

                    if self.is_show:
                        tl = 2
                        h, w = aug_image_copy.shape[:2]
                        x_center = int(bbox[0] * w)
                        y_center = int(bbox[1] * h)
                        width = int(bbox[2] * w)
                        height = int(bbox[3] * h)
                        xmin = int(x_center - width / 2)
                        ymin = int(y_center - height / 2)
                        xmax = int(x_center + width / 2)
                        ymax = int(y_center + height / 2)
                        text = f"{self.labels[cls_id]}"
                        t_size = cv2.getTextSize(text, 0, fontScale=tl / 3, thickness=tl)[0]
                        cv2.rectangle(aug_image_copy, (xmin, ymin - 3), (xmin + t_size[0], ymin - t_size[1] - 3),
                                      (0, 0, 255), -1, cv2.LINE_AA)  # filled
                        cv2.putText(aug_image_copy, text, (xmin, ymin - 2), 0, tl / 3, (255, 255, 255), tl, cv2.LINE_AA)
                        aug_image_show = cv2.rectangle(aug_image_copy, (xmin, ymin), (xmax, ymax), (255, 255, 0), 2)
            except:
                pass

            if self.is_show:
                cv2.imshow(f'aug_image_{new_image_filename}', aug_image_show)
                key = cv2.waitKey(0)
                # 按下s键保存增强，否则取消保存此次增强
                if key & 0xff == ord('s'):
                    pass
                else:
                    cv2.destroyWindow(f'aug_image_{new_image_filename}')
                    continue
                cv2.destroyWindow(f'aug_image_{new_image_filename}')

            # 保存增强后的信息
            print("aug_save_image_path: ", self.aug_save_image_path)
            cv2.imwrite(os.path.join(self.aug_save_image_path, new_image_filename), aug_image)

            with open(os.path.join(self.aug_save_label_path, new_label_filename), 'w', encoding='utf-8') as lf:
                for cls_id, bbox in zip(aug_category_id, aug_bboxes):
                    lf.write(str(cls_id) + ' ')
                    for i in bbox:
                        # 保存小数点后六位
                        lf.write(str(i)[:8] + ' ')
                    lf.write('\n')

            file_name_id += 1


if __name__ == '__main__':
    config_path = 'config.json'
    aug = YOLOAug(config_path)
    aug.aug_image()
