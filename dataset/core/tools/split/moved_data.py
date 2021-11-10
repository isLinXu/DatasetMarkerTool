import os
import shutil

if __name__ == '__main__':

    source_path = '/home/hxzh02/文档/smoke_coco/'
    target_path = '/home/hxzh02/文档/test'
    # rd_path = os.path.join(source_path)
    # wr_path = os.path.join(target_path)

    shutil.copy(source_path, target_path)
    print('move finish!')