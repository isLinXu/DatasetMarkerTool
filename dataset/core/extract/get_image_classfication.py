import numpy as np
import os
import shutil

# 读取txt文件并将其转化为array
f = open(r"./data/test.txt")
line = f.readline()
data_list = []
while line:
    num = list(map(str, line.split(',')))
    data_list.append(num)
    line = f.readline()
f.close()
data_array = np.array(data_list)
num = len(data_array)
print(num)

# 读取每张图片按照其分类复制到相应的文件夹中
imgs = os.listdir('./used_dataset')
imgnum = len(imgs)  # 文件夹中图片的数量
j = 1
for i in range(num):  # 遍历每张图片
    # print(int(data_array[i][0]))
    # label=int(data_array[i][0])    #图片对应的类别
    shutil.copyfile('./used_dataset/' + data_array[i][0], './test/' + data_array[i][0])
    j += 1
print("拷贝结束！")
print("共拷贝" + str(num) + "个文件")
