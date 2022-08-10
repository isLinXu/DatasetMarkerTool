import cv2
import os
# 定义类
class YOLOShow(object):
    def __init__(self,
                 pre_image_path=None,
                 pre_label_path=None,
                 aug_save_image_path=None,
                 aug_save_label_path=None,
                 labels=None,
                 is_show=True,
                 start_filename_id=None,
                 max_len=4):
        """
        :param pre_image_path:
        :param pre_label_path:
        :param aug_save_image_path:
        :param aug_save_label_path:
        :param labels: 标签列表, 需要根据自己的设定, 用于展示图片
        :param is_show:
        :param start_filename_id:
        :param max_len:
        """
        self.pre_image_path = pre_image_path
        self.pre_label_path = pre_label_path
        self.aug_save_image_path = aug_save_image_path
        self.aug_save_label_path = aug_save_label_path
        self.labels = labels
        self.is_show = is_show
        self.start_filename_id = start_filename_id
        self.max_len = max_len
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

        with open(os.path.join(self.pre_label_path, image_name.split('.')[0] + '.txt'), 'r',
                  encoding='utf-8') as f:
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

    def show_image(self):
        image_list = os.listdir(self.pre_image_path)

        file_name_id = self.start_filename_id
        for image_filename in image_list[:]:
            image_suffix = image_filename.split('.')[-1]
            # 为了不报错, 根据文件后缀过滤
            if image_suffix not in ['jpg', 'png']:
                continue

            anno_info = self.get_data(image_filename)

            # 获取信息
            try:
                _image = anno_info['image']
                _bboxes = anno_info['bboxes']
                _category_id = anno_info['category_id']

                aug_image_copy = _image.copy()
                for cls_id, bbox in zip(_category_id, _bboxes):
                    # print(f" --- --- cls_id: ", cls_id)
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
                cv2.imshow(f'yolo_image_show', aug_image_show)
                key = cv2.waitKey(0)
                # 按下s键保存增强，否则取消保存此次增强
                if key & 0xff == ord('s'):
                    pass
                else:
                    cv2.destroyWindow(f'yolo_image_show')
                    continue
                cv2.destroyWindow(f'yolo_image_show')


if __name__ == '__main__':
    # 对示例数据集进行增强, 运行成功后会在相应目录下保存
    # 原始图片和label路径
    PRE_IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/YOLO/images/train2017/'
    PRE_LABEL_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/YOLO/labels/train2017/'

    # 增强后的图片和label保存的路径
    AUG_SAVE_IMAGE_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/YOLO/aug/images/'
    AUG_SAVE_LABEL_PATH = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco128/YOLO/aug/labels/'

    # 类别列表, 需要根据自己的修改
    # labels = ['side-walk', 'speed-limit', 'turn-left', 'slope', 'speed']
    labels = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
              'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
              'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
              'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
              'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
              'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
              'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
              'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
              'teddy bear','hair drier', 'toothbrush']

    show = YOLOShow(pre_image_path=PRE_IMAGE_PATH,
                  pre_label_path=PRE_LABEL_PATH,
                  aug_save_image_path=AUG_SAVE_IMAGE_PATH,
                  aug_save_label_path=AUG_SAVE_LABEL_PATH,
                  labels=labels,
                  is_show=True)
    show.show_image()
