# -*- coding: UTF-8 -*-
import os
import numpy as np
import json
import csv

splits = ['train', 'test']

for split in splits:
    tt100k_root = 'E:/objDetect/tt100k'  # 这里填你的 TT100K 数据集的根目录

    # 读取 json 文件
    jsonFilePath = os.path.join(tt100k_root, 'data', 'anno_xml/annotations.json')
    with open(jsonFilePath, 'r', encoding='utf-8') as f:
        labels = json.load(f)

    # 读取 ids 文件
    idsFilePath = os.path.join(tt100k_root, 'data', split, 'ids.txt')
    with open(idsFilePath, 'r', encoding='utf-8') as f:
        ids = f.readlines()
        for i in range(len(ids)):
            ids[i] = ids[i].replace('\n','')

    # 将 json 中的标签转换格式，并存于变量 annos 中
    annos = ["filename,width,height,class,xmin,ymin,xmax,ymax"]
    for i in ids:
        for obj in labels['imgs'][i]['objects']:
            anno = "%s.jpg,%d,%d,%s,%f,%f,%f,%f"%(i, 2048, 2048,
                                                  obj['category'],
                                                  obj['bbox']['xmin'],
                                                  obj['bbox']['ymin'],
                                                  obj['bbox']['xmax'],
                                                  obj['bbox']['ymax'])
            annos.append(anno)

    # 把转换格式后的标签写入 csv 文件
    with open('./data/' + split + '_labels.csv','w') as f:
        for anno in annos:
            f.write(anno + '\n')
