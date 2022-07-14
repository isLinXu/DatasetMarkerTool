import random
import os

def gen_label_list(xml_dir, img_dir, out_dir, label):
    '''
    生成label_list、train.txt和val.txt
    Args:
        xml_dir: 标签文件地址
        img_dir: 图像文件地址
        out_dir: 输出地址
        label: 生成标签文档

    Returns:

    '''
    random.seed(2020)

    path_list = list()
    print('img_dir', img_dir)
    for img in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img)
        xml_path = os.path.join(xml_dir, img.replace('jpg', 'xml'))
        print('img_path', img_path)
        print('xml_path', xml_path)
        path_list.append((img_path, xml_path))
    random.shuffle(path_list)
    ratio = 0.9
    traintxt_dir = out_dir + 'train.txt'
    valtxt_dir = out_dir + 'val.txt'
    train_f = open(traintxt_dir, 'w')  # 生成训练文件
    val_f = open(valtxt_dir, 'w')  # 生成验证文件

    for i, content in enumerate(path_list):
        img, xml = content
        text = img + ' ' + xml + '\n'
        if i < len(path_list) * ratio:
            train_f.write(text)
        else:
            val_f.write(text)
    train_f.close()
    val_f.close()

    output_dir = out_dir + 'label_list.txt'
    with open(output_dir, 'w') as f:
        for text in label:
            f.write(text + '\n')


if __name__ == '__main__':
    # 标签文件地址
    xml_dir = '/home/linxu/Desktop/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/Annotations'
    # 图像文件地址
    img_dir = '/home/linxu/Desktop/PaddleDetection/dataset/voc/VOCdevkit/VOC2007/JPEGImages'
    # 输出地址
    out_dir = '/home/linxu/Desktop/PaddleDetection/dataset/voc/'

    # 生成标签文档
    # label = ['fall']  # 设置你想检测的类别
    label = ['0_0_0_20_0_0', '0_0_0_16_0_0', '1_0_6_21_42_0', '1_0_0_1_8_1',
             '1_0_6_21_43_0', '0_0_0_50_0_0', '1_0_0_31_0_0', '0_0_0_30_3_0',
             '1_0_3_22_46_0', '0_0_0_30_4_0', '0_0_0_40_1_0', '0_0_0_18_0_0',
             '1_0_3_22_47_0', '1_0_0_2_30_0', '1_0_4_21_40_0', '0_0_0_30_2_0',
             '1_0_0_30_3_0', '1_0_3_22_45_0', '1_0_0_1_8_0', '0_0_0_28_0_0',
             '1_0_0_1_53_0', '1_0_0_1_4_0', '1_0_0_1_6_0', '1_0_3_22_41_0'
             ]

    gen_label_list(xml_dir, img_dir, out_dir, label)
