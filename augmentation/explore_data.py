import os
import time
import glob
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import torchvision
from bs4 import BeautifulSoup
from PIL import Image
import torch
from torchvision import transforms
import albumentations
import albumentations.pytorch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils

img_list = sorted(glob.glob('Face Mask Detection/images/*'))
annot_list = sorted(glob.glob('Face Mask Detection/annotations/*'))

'''
print(len(img_list))
print(len(annot_list))
print(img_list[:10])
print(annot_list[:10])
'''


def generate_box(obj):
    xmin = float(obj.find('xmin').text)
    ymin = float(obj.find('ymin').text)
    xmax = float(obj.find('xmax').text)
    ymax = float(obj.find('ymax').text)

    return [xmin, ymin, xmax, ymax]


def generate_label(obj):
    if obj.find('name').text == "with_mask":
        return 1
    elif obj.find('name').text == "mask_weared_incorrect":
        return 2
    return 0


def generate_target(file):
    with open(file) as f:
        data = f.read()
        soup = BeautifulSoup(data, "html.parser")
        objects = soup.find_all("object")

        num_objs = len(objects)

        boxes = []
        labels = []
        for i in objects:
            boxes.append(generate_box(i))
            labels.append(generate_label(i))

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels, dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels

        return target


def plot_image(img_path, annotation):
    img = mpimg.imread(img_path)

    fig, ax = plt.subplots(1)
    ax.imshow(img)

    for idx in range(len(annotation["boxes"])):
        xmin, ymin, xmax, ymax = annotation["boxes"][idx]

        if annotation['labels'][idx] == 0:
            rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='r',
                                     facecolor='none')

        elif annotation['labels'][idx] == 1:

            rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='g',
                                     facecolor='none')

        else:

            rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='orange',
                                     facecolor='none')

        ax.add_patch(rect)

    plt.show()


def plot_image_from_output(img, annotation):
    img = img.permute(1, 2, 0)

    fig, ax = plt.subplots(1)
    ax.imshow(img)

    for idx in range(len(annotation["boxes"])):
        xmin, ymin, xmax, ymax = annotation["boxes"][idx]

        if annotation['labels'][idx] == 0:
            rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='r',
                                     facecolor='none')

        elif annotation['labels'][idx] == 1:

            rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='g',
                                     facecolor='none')

        else:

            rect = patches.Rectangle((xmin, ymin), (xmax - xmin), (ymax - ymin), linewidth=1, edgecolor='orange',
                                     facecolor='none')

        ax.add_patch(rect)

    plt.show()


# bbox = generate_target(annot_list[232])
# plot_image(img_list[232], bbox)


class TorchvisionMaskDataset(Dataset):
    def __init__(self, path, transforms):

        self.transforms = transforms
        self.path = path
        self.imgs = list(sorted(os.listdir(self.path)))

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        file_image = self.imgs[idx]
        file_label = self.imgs[idx][:-3] + 'xml'
        img_path = os.path.join(self.path, file_image)

        if 'test' in self.path:
            label_path = os.path.join("Face Mask Detection/test_annotations/", file_label)
        else:
            label_path = os.path.join("Face Mask Detection/annotations/", file_label)

        print(label_path, ",", file_image)

        img = Image.open(img_path).convert("RGB")

        target = generate_target(label_path)

        if self.transforms is not None:
            img = self.transforms(img)

        return img, target


torchvision_transform = transforms.Compose([
    transforms.Resize((300, 300)),
    transforms.RandomCrop(224),
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.2),
    transforms.RandomHorizontalFlip(p=1),
    transforms.ToTensor(),
])

only_totensor = transforms.Compose([transforms.ToTensor()])

torchvision_dataset_no_transform = TorchvisionMaskDataset(
    path='Face Mask Detection/images/',
    transforms=only_totensor
)

img, annot = torchvision_dataset_no_transform[0]
print('transforms 적용 전')
plot_image_from_output(img, annot)

torchvision_dataset = TorchvisionMaskDataset(
    path='Face Mask Detection/images/',
    transforms=torchvision_transform)

img, annot = torchvision_dataset[0]

print('transforms 적용 후')
plot_image_from_output(img, annot)


class AlbumentationsDataset(Dataset):
    def __init__(self, path, transform=None):
        self.path = path
        self.imgs = list(sorted(os.listdir(self.path)))
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        file_image = self.imgs[idx]
        file_label = self.imgs[idx][:-3] + 'xml'
        img_path = os.path.join(self.path, file_image)

        if 'test' in self.path:
            label_path = os.path.join("Face Mask Detection/test_annotations/", file_label)
        else:
            label_path = os.path.join("Face Mask Detection/annotations/", file_label)

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(label_path)
        target = generate_target(label_path)

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']

        return image, target


albumentations_transform = albumentations.Compose([
    albumentations.Resize(300, 300),
    albumentations.RandomCrop(224, 224),
    albumentations.ColorJitter(p=1),
    albumentations.HorizontalFlip(p=1),
    albumentations.pytorch.transforms.ToTensorV2()
])

img, annot = torchvision_dataset_no_transform[0]
plot_image_from_output(img, annot)

albumentation_dataset = AlbumentationsDataset(
    path='Face Mask Detection/images/',
    transform=albumentations_transform
)

img, annot = albumentation_dataset[0]
plot_image_from_output(img, annot)

albumentations_transform_oneof = albumentations.Compose([
    albumentations.Resize(300, 300),
    albumentations.RandomCrop(224, 224),
    albumentations.OneOf([
        albumentations.HorizontalFlip(p=1),
        albumentations.RandomRotate90(p=1),
        albumentations.VerticalFlip(p=1)
    ], p=1),
    albumentations.OneOf([
        albumentations.MotionBlur(p=1),
        albumentations.OpticalDistortion(p=1),
        albumentations.GaussNoise(p=1)
    ], p=1),
    albumentations.pytorch.ToTensorV2()
])

albumentation_dataset_oneof = AlbumentationsDataset(
    path='Face Mask Detection/images/',
    transform=albumentations_transform_oneof
)

num_samples = 10
fig, ax = plt.subplots(1, num_samples, figsize=(25, 5))
for i in range(num_samples):
    ax[i].imshow(transforms.ToPILImage()(albumentation_dataset_oneof[0][0]))
    ax[i].axis('off')


class BboxAugmentationDataset(Dataset):
    def __init__(self, path, transform=None):
        self.path = path
        self.imgs = list(sorted(os.listdir(self.path)))
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        file_image = self.imgs[idx]
        file_label = self.imgs[idx][:-3] + 'xml'
        img_path = os.path.join(self.path, file_image)

        if 'test' in self.path:
            label_path = os.path.join("Face Mask Detection/test_annotations/", file_label)
        else:
            label_path = os.path.join("Face Mask Detection/annotations/", file_label)

        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        target = generate_target(label_path)

        if self.transform:
            transformed = self.transform(image=image, bboxes=target['boxes'], labels=target['labels'])
            image = transformed['image']
            target = {'boxes': transformed['bboxes'], 'labels': transformed['labels']}

        return image, target


bbox_transform = albumentations.Compose(
    [albumentations.HorizontalFlip(p=1),
     albumentations.Rotate(p=1),
     albumentations.pytorch.transforms.ToTensorV2()],
    bbox_params=albumentations.BboxParams(format='pascal_voc', label_fields=['labels']),
)

bbox_transform_dataset = BboxAugmentationDataset(
    path='Face Mask Detection/images/',
    transform=bbox_transform
)

img, annot = bbox_transform_dataset[0]
plot_image_from_output(img, annot)

import random

random.seed(2022)

idx = random.sample(range(853), 170)
print(len(idx))
print(idx[:10])

import numpy as np
import shutil

for img in np.array(sorted(os.listdir('Face Mask Detection/images')))[idx]:
    shutil.move('Face Mask Detection/images/' + img, 'Face Mask Detection/test_images/' + img)

for annot in np.array(sorted(os.listdir('Face Mask Detection/annotations')))[idx]:
    shutil.move('Face Mask Detection/annotations/' + annot, 'Face Mask Detection/test_annotations/' + annot)

# %%
print(len(os.listdir('Face Mask Detection/annotations')))
print(len(os.listdir('Face Mask Detection/images')))
print(len(os.listdir('Face Mask Detection/test_annotations')))
print(len(os.listdir('Face Mask Detection/test_images')))

from tqdm import tqdm
import pandas as pd
from collections import Counter


def get_num_objects_for_each_class(dataset):
    total_labels = []

    for img, annot in tqdm(dataset):
        total_labels += [int(i) for i in annot['labels']]

    return Counter(total_labels)


train_data = BboxAugmentationDataset(
    path='Face Mask Detection/images/'
)

test_data = BboxAugmentationDataset(
    path='Face Mask Detection/test_images/'
)

train_objects = get_num_objects_for_each_class(train_data)
test_objects = get_num_objects_for_each_class(test_data)

print('\n train 데이터에 있는 객체', train_objects)
print('\n test 데이터에 있는 객체', test_objects)


# %%


class MaskDataset(Dataset):
    def __init__(self, path, transform=None):
        self.path = path
        self.imgs = list(sorted(os.listdir(self.path)))
        self.transform = transform

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        file_image = self.imgs[idx]
        file_label = self.imgs[idx][:-3] + 'xml'
        img_path = os.path.join(self.path, file_image)

        if 'test' in self.path:
            label_path = os.path.join("Face Mask Detection/test_annotations/", file_label)
        else:
            label_path = os.path.join("Face Mask Detection/annotations/", file_label)

        img = Image.open(img_path).convert("RGB")
        target = generate_target(label_path)

        to_tensor = torchvision.transforms.ToTensor()

        if self.transform:
            img, transform_target = self.transform(np.array(img), np.array(target['boxes']))
            target['boxes'] = torch.as_tensor(transform_target)

        # tensor로 변경
        img = to_tensor(img)

        return img, target


dataset = MaskDataset('Face Mask Detection/images/')
test_dataset = MaskDataset('Face Mask Detection/test_images/')

data_loader = torch.utils.data.DataLoader(dataset, batch_size=4)
test_data_loader = torch.utils.data.DataLoader(test_dataset, batch_size=2)

# %%


retina = torchvision.models.detection.retinanet_resnet50_fpn(num_classes=3, pretrained=False, pretrained_backbone=True)

num_epochs = 30
retina.to(torch.device)

# parameters
params = [p for p in retina.parameters() if p.requires_grad]  # gradient calculation이 필요한 params만 추출
optimizer = torch.optim.SGD(params, lr=0.005,
                            momentum=0.9, weight_decay=0.0005)

len_dataloader = len(data_loader)

# epoch 당 약 4분 소요
for epoch in range(num_epochs):
    start = time.time()
    retina.train()

    i = 0
    epoch_loss = 0
    for images, targets in data_loader:
        images = list(image.to(device) for image in images)
        targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

        loss_dict = retina(images, targets)

        losses = sum(loss for loss in loss_dict.values())

        i += 1

        optimizer.zero_grad()
        losses.backward()
        optimizer.step()

        epoch_loss += losses
    print(epoch_loss, f'time: {time.time() - start}')


def make_prediction(model, img, threshold):
    model.eval()
    preds = model(img)
    for id in range(len(preds)):
        idx_list = []

        for idx, score in enumerate(preds[id]['scores']):
            if score > threshold:  # threshold 넘는 idx 구함
                idx_list.append(idx)

        preds[id]['boxes'] = preds[id]['boxes'][idx_list]
        preds[id]['labels'] = preds[id]['labels'][idx_list]
        preds[id]['scores'] = preds[id]['scores'][idx_list]

    return preds


from tqdm import tqdm

labels = []
preds_adj_all = []
annot_all = []
device = "GPU"
for im, annot in tqdm(test_data_loader, position=0, leave=True):
    im = list(img.to(device) for img in im)
    # annot = [{k: v.to(device) for k, v in t.items()} for t in annot]

    for t in annot:
        labels += t['labels']

    with torch.no_grad():
        preds_adj = make_prediction(retina, im, 0.5)
        preds_adj = [{k: v.to(torch.device('cpu')) for k, v in t.items()} for t in preds_adj]
        preds_adj_all.append(preds_adj)
        annot_all.append(annot)

# datasource:Kaggle Face Mask detection