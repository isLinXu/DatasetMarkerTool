from sklearn.model_selection import train_test_split
import os

"""
train_test_split的用法
train_size：训练集大小
float：0 - 1之间，表示训练集所占的比例
int：直接指定训练集的数量
None：自动为测试集的补集，也就是原始数据集减去测试集
test_size：测试集大小，默认值是0.25
float：0 - 1之间，表示测试集所占的比例
int：直接指定测试集的数量
None：自动为训练集的补集，也就是原始数据集减去训练集
random_state：可以理解为随机数种子，主要是为了复现结果而设置
shuffle：表示是否打乱数据位置，True或者False，默认是True
stratify：表示是否按照样本比例（不同类别的比例）来划分数据集，
例如原始数据集类A: 类B = 75 %:25 %，那么划分的测试集和训练集中的A: B的比例都会是75 %:25 %；可用于样本类别差异很大的情况，一般使用为：stratify = y，即用数据集的标签y来进行划分。
"""

imagedir = '/home/jd/projects/pytorch-deeplab-xception/dataloaders/datasets/wind/JPEGImages/'

outdir = '/home/jd/projects/pytorch-deeplab-xception/dataloaders/datasets/wind/ImageSets/'

images = []
for file in os.listdir(imagedir):
    filename = file.split('.')[0]
    images.append(filename)
# 训练集测试集验证集比例为：4：2：2
train, test = train_test_split(images, train_size=0.5, random_state=0)
val, test = train_test_split(test, train_size=0.5, random_state=0)

with open(outdir + "train.txt", 'w') as f:
    f.write('\n'.join(train))
with open(outdir + "val.txt", 'w') as f:
    f.write('\n'.join(val))
with open(outdir + "test.txt", 'w') as f:
    f.write('\n'.join(test))
