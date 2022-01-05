import matplotlib.pyplot as plt
import numpy as np
import scipy.misc
import os

file_dir = "~/"  # npy文件路径
dest_dir = "~/"  # 文件存储的路径


def npy_png(file_dir, dest_dir):
    # 如果不存在对应文件，则创建对应文件
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    file = file_dir + 'name.npy'  # npy文件
    con_arr = np.load(file)  # 读取npy文件
    for i in range(0, 200):  # 循环数组 最大值为图片张数（我的是200张）  三维数组分别是：图片张数  水平尺寸  垂直尺寸
        arr = con_arr[i, :, :]  # 获得第i张的单一数组
        disp_to_img = scipy.misc.imresize(arr, [375, 1242])  # 根据需要的尺寸进行修改
        plt.imsave(os.path.join(dest_dir, "{}_disp.png".format(i)), disp_to_img, cmap='plasma')  # 定义命名规则，保存图片为彩色模式
        print('photo {} finished'.format(i))


if __name__ == "__main__":
    npy_png(file_dir, dest_dir)