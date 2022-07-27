import io
import sys
import os
import xml.etree.ElementTree as ET
#sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
##修改下面的地址为你存放xml文件的位置，注意斜杠使用/,最后末尾需要加上/
anno_path = 'F:/张珂老师巡检图像/new gradingring/xml/'
#anno_num = [0 for i in range(18)]
#将下面改成你自己的VOC数据集类别
class_name = ('insulator bunch-drop', 'insulator damage', 'insulator pollution', 
                  'bjsb strands','shockproof hammer deformation', 'shockproof hammer intersection', 
                  'cover slab losing', 'illegal construction', 'illegal constructing', 
                  'grading ring damage', 'birdnest', 'foreign body','shielded ring corrosion',
                  'normal single insulator', 'normal grading ring', 'normal shockproof hammer', 
                  'normal shielded ring', 'normal pre-twisted suspension clamp', 'normal single insulator2', 
                  'normal grading ring2')
def _main():
    anno_num = [0]*30
    filelist = os.listdir(anno_path)
    for file in filelist:
        num, annos = _ParseAnnotation(file)
        anno_num = _Count(num, annos, anno_num)
    for j in range(len(class_name)):
        print(class_name[j]+ ': ' + str(anno_num[j]))

def _ParseAnnotation(filepath):
    if os.path.exists(anno_path + filepath) == False:
        print(filepath+' :not found')
    tree = ET.parse(anno_path + filepath)
    annos = [None]*30
    num = 0 
    for annoobject in tree.iter():
        if 'object' in annoobject.tag:
            for element in list(annoobject):
                if 'name' in element.tag:
                    name = element.text 
                if 'bndbox' in element.tag:
                    for size in list(element):
                        if 'xmin' in size.tag:
                            xmin = size.text
                        if 'ymin' in size.tag:
                            ymin = size.text
                        if 'xmax' in size.tag:
                            xmax = size.text
                        if 'ymax' in size.tag:
                            ymax = size.text
                            annos[num] = {'name':name, 'xmin':int(xmin), 'ymin':int(ymin), 'xmax':int(xmax), 'ymax':int(ymax)}
                            #annos[num] = {'name':name, 'xmin':xmin, 'ymin':ymin, \
                             #           'xmax':xmax, 'ymax':ymax}                     
                            num += 1
    return num, annos

def _Count(num, annos, anno_num):
    for i in range(num):
        for j in range(len(class_name)):
            if annos[i]['name'] == class_name[j]:
                anno_num[j] += 1
    return anno_num

if __name__ == '__main__':
    _main()
