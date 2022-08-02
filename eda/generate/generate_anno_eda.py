# 调用一些需要的第三方库
import numpy as np
import pandas as pd
import shutil
import json
import os
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
from matplotlib.font_manager import FontProperties
from PIL import Image
import random
myfont = FontProperties(fname=r"NotoSansCJKsc-Medium.otf", size=12)
plt.rcParams['figure.figsize'] = (12, 12)
plt.rcParams['font.family']= myfont.get_family()
plt.rcParams['font.sans-serif'] = myfont.get_name()
plt.rcParams['axes.unicode_minus'] = False


def generate_anno_eda(dataset_path, anno_file):
    '''
    数据整体分布情况
    Args:
        dataset_path:
        anno_file:

    Returns:

    '''
    with open(os.path.join(dataset_path, anno_file)) as f:
        anno = json.load(f)
    print('标签类别:', anno['categories'])
    print('类别数量：', len(anno['categories']))
    print('训练集图片数量：', len(anno['images']))
    print('训练集标签数量：', len(anno['annotations']))

    total = []
    for img in anno['images']:
        hw = (img['height'], img['width'])
        total.append(hw)
    unique = set(total)
    for k in unique:
        print('长宽为(%d,%d)的图片数量为：' % k, total.count(k))

    ids = []
    images_id = []
    for i in anno['annotations']:
        ids.append(i['id'])
        images_id.append(i['image_id'])
    print('训练集图片数量:', len(anno['images']))
    print('unique id 数量：', len(set(ids)))
    print('unique image_id 数量', len(set(images_id)))

    # 创建类别标签字典
    category_dic = dict([(i['id'], i['name']) for i in anno['categories']])
    counts_label = dict([(i['name'], 0) for i in anno['categories']])
    for i in anno['annotations']:
        counts_label[category_dic[i['category_id']]] += 1
    label_list = counts_label.keys()  # 各部分标签
    print('标签列表:', label_list)
    size = counts_label.values()  # 各部分大小
    color = ['#FFB6C1', '#D8BFD8', '#9400D3', '#483D8B', '#4169E1', '#00FFFF', '#B1FFF0', '#ADFF2F', '#EEE8AA',
             '#FFA500', '#FF6347']  # 各部分颜色
    # explode = [0.05, 0, 0]   # 各部分突出值
    patches, l_text, p_text = plt.pie(size, labels=label_list, colors=color, labeldistance=1.1, autopct="%1.1f%%",
                                      shadow=False, startangle=90, pctdistance=0.6,
                                      textprops={'fontproperties': myfont})
    plt.axis("equal")  # 设置横轴和纵轴大小相等，这样饼才是圆的
    plt.legend(prop=myfont)
    plt.show()

if __name__ == '__main__':
    # Setup the paths to train and test images
    TRAIN_DIR = 'wheat/train/'
    TRAIN_CSV_PATH = 'wheat/train.json'

    # Glob the directories and get the lists of train and test images
    train_fns = glob.glob(TRAIN_DIR + '*')
    print('数据集图片数量: {}'.format(len(train_fns)))

    # 分析训练集数据
    generate_anno_eda('wheat', 'train.json')