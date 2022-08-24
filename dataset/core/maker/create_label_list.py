import os
import random
import shutil


def create_label_list(xml_dir, img_dir, train_dir, train_img_dir,
                      val_dir, val_img_dir,
                      label, ratio, label_dir):
    # 划分数据集
    # 根据挂载的数据集制作制作标签文件，并进行划分
    # 生成train.txt和val.txt
    random.seed(2020)
    path_list = list()
    for img in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img)
        xml_path = os.path.join(xml_dir, img.replace('jpg', 'xml'))
        path_list.append((img_path, xml_path))
    random.shuffle(path_list)

    train_f = open(train_dir, 'w')  # 生成训练文件
    val_f = open(val_dir, 'w')  # 生成验证文件

    if not os.path.exists(train_img_dir) or not os.path.exists(val_img_dir):
        os.mkdir(train_img_dir)
        os.mkdir(val_img_dir)

    for i, content in enumerate(path_list):
        img, xml = content
        print('img:', img, 'xml:', xml)
        text = img + ' ' + xml + '\n'

        if i < len(path_list) * ratio:
            train_f.write(text)
            shutil.copy(img, train_img_dir)

        else:
            val_f.write(text)
            shutil.copy(img, val_img_dir)
    train_f.close()
    val_f.close()

    with open(label_dir, 'w') as f:
        for text in label:
            f.write(text + '\n')


if __name__ == '__main__':
    xml_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/Annotations'  # 标签文件地址
    img_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/JPEGImages'  # 图像文件地址
    train_xml_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/train.txt'
    val_xml_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/val.txt'
    train_img_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/train'
    val_img_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/val'
    ratio = 0.9
    label_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/voc128/label_list.txt'

    # label = ['insulator']  #设置你想检测的类别,生成标签文档
    # label = ['0_0_0_20_0_0', '0_0_0_16_0_0', '1_0_6_21_42_0', '1_0_0_1_8_1',
    #          '1_0_6_21_43_0', '0_0_0_50_0_0', '1_0_0_31_0_0', '0_0_0_30_3_0',
    #          '1_0_3_22_46_0', '0_0_0_30_4_0', '0_0_0_40_1_0', '0_0_0_18_0_0',
    #          '1_0_3_22_47_0', '1_0_0_2_30_0', '1_0_4_21_40_0', '0_0_0_30_2_0',
    #          '1_0_0_30_3_0', '1_0_3_22_45_0', '1_0_0_1_8_0', '0_0_0_28_0_0',
    #          '1_0_0_1_53_0', '1_0_0_1_4_0', '1_0_0_1_6_0', '1_0_3_22_41_0',
    #          '0_0_0_1_23_0', '0_0_0_30_2_1', '0_0_0_1_17_0','0_0_0_1_22_0',
    #          '0_0_0_1_8_0','0_0_0_17_0_0','0_0_0_1_52_0','1_0_0_1_22_0',
    #          '1_0_0_30_2_0','1_0_0_30_4_0']
    # label = ['0_0_0_20_0_0', '0_0_0_18_0_0', '0_0_0_50_0_0', '1_0_4_21_40_0', '0_0_0_40_1_0',
    #                '0_0_0_30_2_0', '1_0_0_1_8_1', '1_0_0_31_0_0', '0_0_0_30_3_0', '1_0_0_1_4_0',
    #                '0_0_0_16_0_0', '0_0_0_28_0_0', '1_0_0_2_30_0', '1_0_6_21_42_0', '1_0_3_22_41_0',
    #                '1_0_3_22_46_0', '0_0_0_30_4_0', '1_0_3_22_45_0', '1_0_0_1_6_0', '1_0_0_1_8_0',
    #                '1_0_0_1_53_0', '1_0_3_22_47_0', '1_0_0_30_3_0', '1_0_6_21_43_0']

    label = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
             'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
             'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
             'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
             'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
             'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
             'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
             'cell phone',
             'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear',
             'hair drier', 'toothbrush']
    create_label_list(xml_dir, img_dir, train_xml_dir, train_img_dir,
                      val_xml_dir, val_img_dir,
                      label, ratio, label_dir)
