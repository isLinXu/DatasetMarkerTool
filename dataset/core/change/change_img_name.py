# -*- coding:utf8 -*-

import os


class BatchRename():
    '''
    批量重命名文件夹中的图片文件
    '''

    def __init__(self):
        self.path = '/media/hxzh02/SB@home/hxzh/Dataset/无人机相关数据集合集/1-火焰数据集/fire_dataset/VOC2007/Annotations/'

    def rename(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
        i = 1
        n = 6
        for item in filelist:
            if item.endswith('.png') or item.endswith('.jpg'):
                n = 6 - len(str(i))
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), str(0) * n + str(i) + '.png')
                try:
                    os.rename(src, dst)
                    print('converting %s to %s ...' % (src, dst))
                    i = i + 1

                except:
                    continue
        print('total %d to rename & converted %d jpgs' % (total_num, i))

    def rename_xml(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
        i = 1
        n = 6
        for item in filelist:
            if item.endswith('.xml'):
                n = 6 - len(str(i))
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), str(0) * n + str(i) + '.xml')
                try:
                    os.rename(src, dst)
                    print('converting %s to %s ...' % (src, dst))
                    i = i + 1

                except:
                    continue
        print('total %d to rename & converted %d jpgs' % (total_num, i))



if __name__ == '__main__':
    demo = BatchRename()
    # demo.rename()
    demo.rename_xml()
