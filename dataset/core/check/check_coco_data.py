


import json

def check_parse_coco(coco_dir):
    coco_anno = json.load(open(coco_dir))

    # coco_anno.keys
    print('keys:', coco_anno.keys())

    # 查看类别信息
    classes = coco_anno['categories']
    print('物体类别:', classes)

    class_list = []
    for cls in classes:
        print(cls)
        class_list.append(cls['name'])
    # for cl in class_list:
    #     print(cl)
    print('class_list:', class_list)

    # 查看一共多少张图
    print('图像数量：', len(coco_anno['images']))

    # 查看一共多少个目标物体
    print('标注物体数量：', len(coco_anno['annotations']))

    # 查看一条目标物体标注信息
    print('查看一条目标物体标注信息：', coco_anno['annotations'][0])



if __name__ == '__main__':
    coco_dir = '/media/hxzh02/SB@home/hxzh/PaddleDetection/dataset/coco/coco2017/annotations/instances_train.json'
    check_parse_coco(coco_dir)
    # coco_anno = json.load(open(coco_dir))
    #
    # # coco_anno.keys
    # print('keys:', coco_anno.keys())
    #
    # # 查看类别信息
    # print('物体类别:', coco_anno['categories'])
    #
    # # 查看一共多少张图
    # print('图像数量：', len(coco_anno['images']))
    #
    # # 查看一共多少个目标物体
    # print('标注物体数量：', len(coco_anno['annotations']))
    #
    # # 查看一条目标物体标注信息
    # print('查看一条目标物体标注信息：', coco_anno['annotations'][0])