
import cv2
import os
import shutil
import time
import sys

leftkeys = (81, 110, 65361, 2424832)
rightkeys = (83, 109, 65363, 2555904)
# 当前脚本工作的目录路径
root_dir = os.getcwd()
# print(root_dir)
# os.path.abspath()获得绝对路径
root_absdir = os.path.abspath(os.path.dirname(__file__))
print(root_absdir)

def make_dirs2(n):
    if not os.path.exists(os.path.join(root_dir, n)):
        os.makedirs(os.path.join(root_dir, n))


def Classification_Tools(data_dir,class_names,action_type='copy'):

    global image
    if not os.path.exists(data_dir):
        print('data_all not exists, please put data to: ', data_dir)
        time.sleep(5)
        exit()

    unconfirmed = 'unconfirmed'  # 不确定数据存放路径
    make_dirs2(unconfirmed)


    num_cls = len(class_names)
    for j in range(num_cls):
        make_dirs2(str(class_names[j]))

    image_list = os.listdir(data_dir)
    if len(image_list) == 0:
        print('no image in %s ... please put data to: %s' % (data_dir, data_dir))
        time.sleep(5)
        exit()
    cv2.namedWindow('Classification_Tools', 0)
    i = 0
    coccus_label = None
    for i in range(0, len(image_list)):
        assert i < len(image_list), ('no image left...')
        print('i', i)
        image_path = os.path.join(data_dir, image_list[i])
        print(image_path)
        image = cv2.imread(image_path)
        if image.shape is None:
            print('The images open fail!')
            continue
        else:
            print(image.shape)
            cv2.imshow('Classification_Tools', image)
            key = cv2.waitKeyEx()

        if key == ord('d'):
            coccus_label = 'unconfirmed'
            if action_type == 'copy':
                shutil.copy(image_path, os.path.join(root_dir, unconfirmed))
            else:
                shutil.move(image_path, os.path.join(root_dir, unconfirmed))
            i += 1  # (i + 1) % len(image_list)
        if key in rightkeys:
            i += 1  # (i + 1) % len(image_list)
        if key in leftkeys and coccus_label != None:
            # if not os.path.exists(os.path.join(('./' + str(coccus_label)), image_list[i-1])):
            print('leftkeys:', os.path.join(('./' + str(coccus_label)), image_list[i - 1]))
            if os.path.exists(os.path.join(('./' + str(coccus_label)), image_list[i - 1])):
                print('successful', os.path.join(('./' + str(coccus_label)), image_list[i - 1]))
                if action_type == 'copy':
                    shutil.copy(os.path.join(('./' + str(coccus_label)), image_list[i - 1]), data_dir)
                else:
                    shutil.move(os.path.join(('./' + str(coccus_label)), image_list[i - 1]), data_dir)
            i -= 1
            if i < 0:
                i = len(image_list) - 1


        if (key == ord('q')) or (key == 27):
            break

        for j in range(num_cls):
            if key & 0xFF == ord(str(j)):
                coccus_label = str(j)
                shutil.move(image_path, os.path.join(root_dir, str(class_names[j])))

                i += 1  # (i + 1) % len(image_list)
                break

if __name__ == '__main__':

    # 待分类数据路径
    data_dir = '/home/linxu/Projects/PycharmProjects/AI-Map/core/tiles'
    # 待分类名称列表
    class_names = ['house', 'road', 'space']
    # 分类标注器
    Classification_Tools(data_dir,class_names,)

