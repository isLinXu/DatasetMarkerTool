import os
import random

import xml.etree.ElementTree as ET

# def generate_train_val_test_txt():
xml_file_path = '/home/linxu/Desktop/VOC2007/Annotations/'  # xml文件路径
save_Path = '/home/linxu/Desktop/VOC2007/ImageSets/Main/'

trainval_percent = 0.9
train_percent = 0.8
total_xml = os.listdir(xml_file_path)  # 得到文件夹下所有文件名称
print("total_xml:", total_xml)

num = len(total_xml)
list = range(num)
tv = int(num * trainval_percent)
tr = int(tv * train_percent)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)
print("train and val size", tv)
print("train size", tr)
############################在Main下生成test.txt、train.txt、val.txt、trainval.txt这四个文件##################################
"""
将信息写入test.txt、train.txt、val.txt、trainval.txt
"""

if not os.path.exists(save_Path):
    os.makedirs(save_Path)

ftrainval = open(os.path.join(save_Path, 'trainval.txt'), 'w')
ftest = open(os.path.join(save_Path, 'test.txt'), 'w')
ftrain = open(os.path.join(save_Path, 'train.txt'), 'w')
fval = open(os.path.join(save_Path, 'val.txt'), 'w')
for i in list:  # 第i个xml文件
    xml_name = total_xml[i][:-4]
    if i in trainval:
        ftrainval.write(xml_name + "\n")
        if i in train:
            ftrain.write(xml_name + "\n")
        else:
            fval.write(xml_name + "\n")
    else:
        ftest.write(xml_name + "\n")
ftrainval.close()
ftrain.close()
fval.close()
ftest.close()

##########################生成Main中的各类txt文件############################################
"""
将信息写入(class_name)_test.txt、(class_name)_train.txt、(class_name)_val.txt、(class_name)_trainval.txt
 """
# 这个代码运行一次生成一类的txt文件，所以当你有多类的时候要改这里和下面对应的地方
# VOC_CLASSES = ['dog']
VOC_CLASSES = ['0_0_0_20_0_0','0_0_0_16_0_0','1_0_6_21_42_0','1_0_0_1_8_1',
                '1_0_6_21_43_0','0_0_0_50_0_0','1_0_0_31_0_0','0_0_0_30_3_0',
                '1_0_3_22_46_0','0_0_0_30_4_0','0_0_0_40_1_0','0_0_0_18_0_0',
                '1_0_3_22_47_0','1_0_0_2_30_0','1_0_4_21_40_0','0_0_0_30_2_0',
                '1_0_0_30_3_0','1_0_3_22_45_0','1_0_0_1_8_0','0_0_0_28_0_0',
                '1_0_0_1_53_0','1_0_0_1_4_0','1_0_0_1_6_0','1_0_3_22_41_0'
               ]


for idx in range(len(VOC_CLASSES)):  # 每一个类单独处理
    class_name = VOC_CLASSES[idx]
    # 创建txt
    class_trainval = open(os.path.join(save_Path, str(class_name) + '_trainval.txt'), 'w')
    class_test = open(os.path.join(save_Path, str(class_name) + '_test.txt'), 'w')
    class_train = open(os.path.join(save_Path, str(class_name) + '_train.txt'), 'w')
    class_val = open(os.path.join(save_Path, str(class_name) + '_val.txt'), 'w')
    for k in list:
        xml_name = total_xml[k][:-4]  # xml的名称
        print(xml_name)
        xml_path = os.path.join(xml_file_path, xml_name + '.xml')
        # 将获取的xml文件名送入到dom解析
        tree = ET.parse(xml_path)  # 输入xml文件具体路径
        root = tree.getroot()
        # 创建一个空列表，用于保存xml中object的name
        object_names = []
        for object in root.findall('object'):
            # 获取xml object标签<name>
            object_name = object.find('name').text
            object_names.append(object_name)

        if len(object_names) > 0 and 'dog' in object_names:  # 存在object（矩形框并且class_name在object_name列表中  # 这里的类别对应上面VOC_CLASSES
            if k in trainval:
                class_trainval.write(xml_name + ' ' + str(1) + "\n")
                if k in train:
                    class_train.write(xml_name + ' ' + str(1) + "\n")
                else:
                    class_val.write(xml_name + ' ' + str(1) + "\n")
            else:
                class_test.write(xml_name + ' ' + str(1) + "\n")
        else:
            if k in trainval:
                class_trainval.write(xml_name + ' ' + str(-1) + "\n")
                if k in train:
                    class_train.write(xml_name + ' ' + str(-1) + "\n")
                else:
                    class_val.write(xml_name + ' ' + str(-1) + "\n")
            else:
                class_test.write(xml_name + ' ' + str(-1) + "\n")

    class_trainval.close()
    class_test.close()
    class_train.close()
    class_val.close()  # 1类的.txt编辑好了
