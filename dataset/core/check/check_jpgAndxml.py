import os, shutil
# import sys
from tqdm import *

# sys.path.append("../")

def checkJpgXml(jpeg_dir, annot_dir):
    """
    dir1 是图片所在文件夹
    dir2 是标注文件所在文件夹
    """ 
    pBar = tqdm(total=len(os.listdir(jpeg_dir)))
    cnt = 0
    for file in os.listdir(jpeg_dir):
        pBar.update(1)
        f_name, f_ext = file.split(".")
        if not os.path.exists(os.path.join(annot_dir, f_name + ".txt")):
            print(f_name)
            cnt += 1

    if cnt > 0:
        print("有%d个文件不符合要求。" % (cnt))
    else:
        print("所有图片和对应的xml文件都是一一对应的。")


if __name__ == "__main__":
    dir1 = r"../GarbageData/images/garbage_test"
    dir2 = r"../GarbageData/labels/garbage_test"
    checkJpgXml(dir1, dir2)