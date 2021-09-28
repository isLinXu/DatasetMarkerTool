import json
import cv2


#第一个coco json类型

bnd_id_start = 1

times = 0

json_dict = {
    "images": [],
    "type": "instances",
    "annotations": [],
    "categories" : []
}




# 这里是你的txt文件的读取
with open('test_gt_TT100Kthree.txt','r') as f:
    data = f.readlines()

bnd_id = bnd_id_start


for d in data:
    content = d.split(";")
    filename = content[0].split(".jpg")[0]     #这里可能修改，txt文件每一行第一个属性是图片路径，通过split()函数把图像名分离出来就行
    # img = cv2.imread("/home/dell/桌面/GTSDB/VOC2007"+content[0])
    try:
        height, width=2048,2048
        image_id = int(filename)
    except:
        times +=1
        print('file is error')

# type 已经填充

#定义image 填充到images里面
    image = {
        'file_name' : filename,  #文件名
        'height'    : height,    #图片的高
        'width'     : width,     #图片的宽
        'id'        : image_id   #图片的id，和图片名对应的
    }
    json_dict['images'].append(image)

    c=content[1:]
    xmin,ymin,xmax,ymax,label = c


    xmin = int(xmin)
    ymin = int(ymin)
    xmax = int(xmax)
    ymax = int(ymax)
    o_width = abs(int(xmax) - int(xmin))
    o_height = abs(int(ymax) - int(ymin))

    area = o_width * o_height
    category_id = label.strip()

    # #定义annotationhb
    annotation = {
        'area'          : area,  #
        'iscrowd'       : 0,
        'image_id'      : image_id,  #图片的id
        'bbox'          :[xmin, ymin, o_width,o_height],
        'category_id'   : int(category_id)+1, #类别的id 通过这个id去查找category里面的name
        'id'            : bnd_id,  #唯一id ,可以理解为一个框一个Id
        'ignore'        : 0,
        'segmentation'  : []
    }

    json_dict['annotations'].append(annotation)

    bnd_id += 1
    #
#定义categories

#你得类的名字(cid,cate)对应
classes = ['0','1','2','3']

for i in range(len(classes)):

    cate = classes[i]
    cid = i
    category = {
        'supercategory' : 'none',
        'id'            : cid,  #类别的id ,一个索引，主键作用，和别的字段之间的桥梁
        'name'          : cate  #类别的名字比如房子，船，汽车
    }

    json_dict['categories'].append(category)



json_fp = open("TT100K_val.json",'w')
json_str = json.dumps(json_dict)
json_fp.write(json_str)
json_fp.close()
