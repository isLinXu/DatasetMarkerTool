import os
import random
import xml.dom.minidom


def generate_train_val_test_txt():
    xml_file_path = "/home/aistudio/PaddleDetection/dataset/“自定义数据集的名字”/Annotations/train/"  # xml文件路径，train和val需各运行一次
    save_Path = "/home/aistudio/PaddleDetection/dataset/“自定义数据集的名字”/ImageSets/"  # ImageSets文件夹路径

    # 考虑到有可能已有的数据集是train和val(dev)放在一起的，这样设计可以随机分出训练集和验证集
    trainval_percent = 1.0  # trainval_percent是训练集和验证集占总图片的比例，设为1.0
    train_percent = 1.0  # train_percent是训练集占训练集和验证集的比例，如果是训练集文件夹则=1.0，如果是验证集文件夹则=0.0

    total_xml = os.listdir(xml_file_path)  # 得到文件夹下所有文件名称
    num = len(total_xml)  # 获取总的描述文件数
    list = range(num)  # 生成描述文件索引表
    tv = int(num * trainval_percent)  # 按比例计算trainval的数量
    tr = int(tv * train_percent)  # 再按比例计算train的数量
    trainval = random.sample(list, tv)  # 随机从数据集中分出trainval
    train = random.sample(trainval, tr)  # 随机从trainval中分出train

    print("train and val:", tv)  # trainval的总数
    print("train:", tr)  # train的总数

    ftrain = open(os.path.join(save_Path, 'train.txt'), 'w')
    fval = open(os.path.join(save_Path, 'val.txt'), 'w')

    # 要求描述文件（xml文件）的名字和图片名字一样！（当然不包括后缀部分...）
    # 下面这个地址要根据你数据集各部分放在AiStudio中的地址做修改！！！
    # 下面这个地址要根据你数据集各部分放在AiStudio中的地址做修改！！！
    # 下面这个地址要根据你数据集各部分放在AiStudio中的地址做修改！！！
    for i in list:  # 遍历第i个xml文件
        xml_name = total_xml[i][:-4]  # 去除".xml"
        if i in train:
            ftrain.write(
                "/home/aistudio/PaddleDetection/dataset/“自定义数据集的名字”/JPEGImages/train/" + xml_name + ".jpg" + " " + "/home/aistudio/PaddleDetection/dataset/“自定义数据集的名字”/Annotations/train/" + xml_name + ".xml" + "\n")
        else:
            fval.write(
                "/home/aistudio/PaddleDetection/dataset/“自定义数据集的名字”/JPEGImages/val/" + xml_name + ".jpg" + " " + "/home/aistudio/PaddleDetection/dataset/“自定义数据集的名字”/Annotations/val/" + xml_name + ".xml" + "\n")

    ftrain.close()
    fval.close()


generate_train_val_test_txt()
# 如果train和val分两次运行，需要避免之前生成的有效的那个被覆盖，换句话说，实际上两次运行只需要分别保存一个txt（备份下，把没用的那个删掉）
