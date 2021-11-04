import os
import shutil
import glob
import xml.etree.ElementTree as et
from PIL import Image, ImageDraw


class Polygon:
    def __init__(self):
        self.points = []

    def addPoint(self, point):
        self.points.append(point)

    def toString(self):
        result = ''

        for point in self.points:
            result += point + ', '

            return result


"""
Class to create a bounding box of a given polygon.
The corners of the box are saved in the class variables p1 and p2.
"""


class BoundingBox:
    def __init__(self, polygon):
        self.min_x = polygon.points[0][0]
        self.min_y = polygon.points[0][1]
        self.max_x = polygon.points[0][0]
        self.max_y = polygon.points[0][1]

        for point in polygon.points:
            self.min_x = min(self.min_x, point[0])
            self.min_y = min(self.min_y, point[1])
            self.max_x = max(self.max_x, point[0])
            self.max_y = max(self.max_y, point[1])

        self.p1 = (self.min_x, self.min_y)
        self.p2 = (self.max_x, self.max_y)

    def getXMin(self):
        return self.min_x

    def getYMin(self):
        return self.min_y

    def getXMax(self):
        return self.max_x

    def getYMax(self):
        return self.max_y


"""
Class to save the annotations as a list of polygons and the filename of the associated image.
"""


class ImageAnnotation:
    def __init__(self, imageFilename, imageWidht, imageHeight, polygons):
        self.image_filename = imageFilename
        self.imageWidht = imageWidht
        self.imageHeight = imageHeight
        self.polygons = polygons


"""
Class to extract annotations from xml-files created by the LabelMe tool.
"""


class LabelMe:
    """
    Method to create a class object for the given image and annotation directory
    """

    def __init__(self, images_dir, annotations_dir):
        self.images_dir = images_dir
        self.annotations_dir = annotations_dir

    """
    Extracts all annotations from the annotation directory and saves them in a list of annotation objects
    """

    def extractImageAnnotations(self):
        imageAnnotations = []
        annotation_paths = glob.glob(self.annotations_dir + '/*.xml')

        for annotation_path in annotation_paths:
            xml_tree = et.parse(annotation_path)
            xml_root = xml_tree.getroot()
            xml_polygons = xml_root.findall("./object/polygon")
            polygons = []
            image_filename = xml_root.find('filename').text
            imageWidht, imageHeight = Image.open(self.images_dir + '/' + image_filename).size

            if len(xml_polygons) > 0:
                for xml_polygon in xml_polygons:
                    polygon = Polygon()
                    points = xml_polygon.iter('pt')

                    for point in points:
                        x = int(point.find('x').text)
                        y = int(point.find('y').text)

                        polygon.addPoint((x, y))

                    polygons.append(polygon)

            imageAnnotations.append(ImageAnnotation(image_filename, imageWidht, imageHeight, polygons))

        return imageAnnotations


def calcPolygonBoundingBoxRatio(polygon, boundingBox):
    # calculate bounding box size
    boundingBoxSize = abs((boundingBox.p1[0] - boundingBox.p2[0]) * (boundingBox.p1[1] - boundingBox.p2[1]))
    # calculate area of polygon
    polygonSize = calcPolygonArea(polygon)

    return polygonSize * 1.0 / boundingBoxSize * 1.0


class PascalVocAnnotation:
    def __init__(self, baseFolder, imageFolder, imageFilename, imageWidht, imageHeight, boundingBox):
        self.baseFolder = baseFolder;
        self.filename = imageFilename.replace('.jpg', '.xml')
        self.imageFolder = imageFolder
        self.imageFilename = imageFilename
        self.imageWidht = imageWidht
        self.imageHeight = imageHeight
        self.boundingBox = boundingBox

    def createXMLAnnotation(self):
        xmlAnnotation = et.Element('annotation')

        xmlAnnotationFolder = et.SubElement(xmlAnnotation, 'folder')
        xmlAnnotationFilename = et.SubElement(xmlAnnotation, 'filename')

        xmlAnnotationSize = et.SubElement(xmlAnnotation, 'size')
        xmlAnnotationSizeWidth = et.SubElement(xmlAnnotationSize, 'width')
        xmlAnnotationSizeHeight = et.SubElement(xmlAnnotationSize, 'height')
        xmlAnnotationSizeDepth = et.SubElement(xmlAnnotationSize, 'depth')

        xmlAnnotationObject = et.SubElement(xmlAnnotation, 'object')
        xmlAnnotationObjectName = et.SubElement(xmlAnnotationObject, 'name')
        xmlAnnotationObjectBndBox = et.SubElement(xmlAnnotationObject, 'bndbox')
        xmlAnnotationObjectBndBoxXmin = et.SubElement(xmlAnnotationObjectBndBox, 'xmin')
        xmlAnnotationObjectBndBoxYmin = et.SubElement(xmlAnnotationObjectBndBox, 'ymin')
        xmlAnnotationObjectBndBoxXmax = et.SubElement(xmlAnnotationObjectBndBox, 'xmax')
        xmlAnnotationObjectBndBoxYmax = et.SubElement(xmlAnnotationObjectBndBox, 'ymax')

        xmlAnnotationFolder.text = self.baseFolder
        xmlAnnotationFilename.text = self.imageFilename

        xmlAnnotationSizeWidth.text = str(self.imageWidht)
        xmlAnnotationSizeHeight.text = str(self.imageHeight)
        xmlAnnotationSizeDepth.text = str(3)

        xmlAnnotationObjectName.text = 'stairs'
        xmlAnnotationObjectBndBoxXmin.text = str(self.boundingBox.getXMin())
        xmlAnnotationObjectBndBoxYmin.text = str(self.boundingBox.getYMin())
        xmlAnnotationObjectBndBoxXmax.text = str(self.boundingBox.getXMax())
        xmlAnnotationObjectBndBoxYmax.text = str(self.boundingBox.getYMax())

        return et.ElementTree(xmlAnnotation)


labelmeBaseFolder = 'data/labelme'
labelmeImageFolder = labelmeBaseFolder + '/Images'
labelmeAnnotationFolder = labelmeBaseFolder + '/Annotations'
pascalVocBaseFolder = 'tf-faster-rcnn/data/stairs/stairs'
pascalVocAnnotationFolder = pascalVocBaseFolder + '/Annotations'
pascalVocJPEGImageFolder = pascalVocBaseFolder + '/Images'

# create folder structure for pascal voc format with the two folders Annotations ans JPEGImages
if os.path.exists(pascalVocBaseFolder):
    shutil.rmtree(pascalVocBaseFolder)

os.makedirs(pascalVocBaseFolder)
os.makedirs(pascalVocAnnotationFolder)
os.makedirs(pascalVocJPEGImageFolder)

# extract annotations from labelme
labelMe = LabelMe(labelmeImageFolder, labelmeAnnotationFolder)
imageAnnotations = labelMe.extractImageAnnotations()

# convert labelme annotations to pascal voc annotations
for annotation in imageAnnotations:
    image = Image.open(labelmeImageFolder + '/' + annotation.image_filename).convert('RGB')

    # print(annotation.image_filename)

    # only use annotations with only one polygon for now
    if len(annotation.polygons) == 1:
        for polygon in annotation.polygons:
            # make sure the polygon has more than 2 points
            if len(polygon.points) > 2:
                boundingBox = BoundingBox(polygon);
                pascalVocAnnotation = PascalVocAnnotation(pascalVocBaseFolder, labelmeImageFolder,
                                                          annotation.image_filename, annotation.imageWidht,
                                                          annotation.imageHeight, boundingBox)
                # save annotation in pascal voc format
                pascalVocAnnotation.createXMLAnnotation().write(
                    pascalVocAnnotationFolder + '/' + pascalVocAnnotation.filename)
                # copy image in pascal voc folder structure
                image.save(pascalVocJPEGImageFolder + '/' + annotation.image_filename)
