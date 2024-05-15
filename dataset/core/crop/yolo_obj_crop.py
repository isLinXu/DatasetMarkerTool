import cv2
import os
from tqdm import tqdm
class Cropper:
    def __init__(self, class_names, sample_size=10):
        self.class_names = class_names
        self.sample_size = sample_size

    @staticmethod
    def read_gt(file_path, img_width, img_height):
        with open(file_path, 'r') as f:
            lines = f.readlines()
            boxes = []
            for line in lines:
                line = line.strip().split()
                label = int(float(line[0]))
                x, y, w, h = map(float, line[1:])
                x_min = int((x - w / 2) * img_width)
                y_min = int((y - h / 2) * img_height)
                x_max = int((x + w / 2) * img_width)
                y_max = int((y + h / 2) * img_height)
                boxes.append([x_min, y_min, x_max, y_max, label])
            return boxes

    def crop_and_save(self, img, boxes, output_folder, img_path):
        for box in boxes:
            x_min, y_min, x_max, y_max, label = box
            try:
                cropped_img = img[y_min:y_max, x_min:x_max]
                class_folder = os.path.join(output_folder, self.class_names[label])
                if not os.path.exists(class_folder):
                    os.makedirs(class_folder)
                x, y, w, h = (x_max + x_min) // 2, (y_max + y_min) // 2, x_max - x_min, y_max - y_min
                img_name = f"{os.path.splitext(os.path.basename(img_path))[0]}_{label:02}_{x:04}_{y:04}_{w:04}_{h:04}.jpg"
                cropped_img_path = os.path.join(class_folder, img_name)
                cv2.imwrite(cropped_img_path, cropped_img)
            except Exception as e:
                print(f"Error saving image: {e}")

    def crop_images(self, img_folder, gt_folder, output_folder):
        img_list = os.listdir(img_folder)
        img_list = [file for file in img_list if file.endswith(('.jpg', '.png', 'jpeg'))]

        for file in tqdm(img_list, desc='Cropping images'):
            img_path = os.path.join(img_folder, file)
            gt_path = os.path.join(gt_folder, file[:-4] + '.txt')
            if os.path.exists(gt_path):
                img = cv2.imread(img_path)
                img_height, img_width = img.shape[:2]
                boxes = self.read_gt(gt_path, img_width, img_height)
                self.crop_and_save(img, boxes, output_folder, img_path)


if __name__ == '__main__':
    class_names = ['nomotor', 'bike', 'person', 'other']
    cropper = Cropper(class_names)
    datasets_dir = 'path/to/datasets'
    img_folder = datasets_dir + '/images/train'
    gt_folder = datasets_dir + '/labels/train'
    folder = '/yolov6predictions/'
    output_folder = 'datasets/train/'

    cropper.crop_images(img_folder, gt_folder, output_folder)
