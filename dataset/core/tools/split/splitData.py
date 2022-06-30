import os
from glob import glob
import shutil

imgs = glob("./images/*.jpg")
labels = glob("./labels_yolo/*.txt")

dir_list = ["./splitData/images",
            "./splitData/labels",
            "./splitData/images/train",
            "./splitData/images/test",
            "./splitData/images/val",
            "./splitData/labels/train",
            "./splitData/labels/test",
            "./splitData/labels/val"]
for i in range(len(dir_list)):
    try:
        os.mkdir(dir_list[i])
    except:
        print(f"{dir_list[i]} has maked")

for i in range(len(imgs)):
    print(f"正在处理第{i}张图片")
    if i % 10 < 7:
        shutil.copy(imgs[i], dir_list[2])
        shutil.copy(labels[i], dir_list[5])
    elif 7 <= i % 10 < 9:
        shutil.copy(imgs[i], dir_list[3])
        shutil.copy(labels[i], dir_list[6])
    else:
        shutil.copy(imgs[i], dir_list[4])
        shutil.copy(labels[i], dir_list[7])
print("处理完成！")