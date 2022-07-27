import os
import re
#coding=utf-8
#def filematch(file):
import xml.etree.ElementTree as ET


#anno_path = 'F:/数据集/luoshuan/Annos（包含正常螺栓和正常碗头）/'
anno_path = 'G:/pythonStudy/xml/'
def main():
    filelist = os.listdir(anno_path)
  #  for file in filelist:
   #     a=re.findall(r'[0-9]{2}_[0-9]{6}', file)
   #    if a !=None:
   #         print(a)
    num, annos = _ParseAnnotation(filelist[1])
    _CreateObjectAnnotation(filelist[0], annos)

def _ParseAnnotation(filepath):
    if os.path.exists(anno_path + filepath) == False:
        print(filepath+' :not found')
    tree = ET.parse(anno_path + filepath)
    annos = [None]*10
    num = 0 
    for annoobject in tree.iter():
        if 'object' in annoobject.tag:
            for element in list(annoobject):
                if 'name' in element.tag:
                    name = element.text
                    print(name)
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
                     #       annos[num] = {'name':name, 'xmin':int(xmin), 'ymin':int(ymin), 'xmax':int(xmax), 'ymax':int(ymax)}
                            annos[num] = {'name':name, 'xmin':xmin, 'ymin':ymin, \
                                        'xmax':xmax, 'ymax':ymax}                     
                            num += 1
    for i in range(num):
        print(annos[i])
    return num, annos

def _CreateObjectAnnotation(filepath, annos):
    if os.path.exists(anno_path + filepath) == False:
        print('not found' + anno_path + filepath)
    tree = ET.parse(anno_path + filepath)
    root = tree.getroot()
    for annotation in annos:
        if annotation != None:
            _CreateElement(root, annotation)  
    tree.write(anno_path + filepath, encoding='utf-8', xml_declaration=True)

def _CreateElement(root, annotation):
    object1 = ET.Element('object')
    name = ET.SubElement(object1, 'name')
    name.text = annotation['name']
    pose = ET.SubElement(object1, 'pose')
    pose.text = 'Unspecified'
    truncated = ET.SubElement(object1, 'truncated')
    truncated.text = '0'
    difficult = ET.SubElement(object1, 'difficult')
    difficult.text = '0'
    bndbox = ET.SubElement(object1, 'bndbox')
    xmin = ET.SubElement(bndbox, 'xmin')
    xmin.text = annotation['xmin']
    ymin = ET.SubElement(bndbox, 'ymin')
    ymin.text = annotation['ymin']
    xmax = ET.SubElement(bndbox, 'xmax')
    xmax.text = annotation['xmax']
    ymax = ET.SubElement(bndbox, 'ymax')
    ymax.text = annotation['ymax']
    root.append(object1)

#def FileMatch:
    
    
if __name__ == "__main__":
    main()

