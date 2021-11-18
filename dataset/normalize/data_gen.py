import argparse
import os
import shutil
from pathlib import Path


# generate a dataset from individual images for torchvision.datasets.ImageFolder
def generate_dataset(root):
    image_paths = os.listdir(root)
    images = [i for i in image_paths if '.png' in i]
    names = sorted(list(set([i.split(".")[0].split("-")[0] for i in images])))
    # mkdir
    for n in names:
        Path(os.path.join(root, n)).mkdir(exist_ok=True)  # python 3.5 above
    for p in image_paths:
        dest = os.path.join(root, p.split(".")[0].split("-")[0])
        if os.path.exists(dest):
            shutil.move(os.path.join(root, p), dest)
        else:
            print("the destination " + dest + " does not exist, please check!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a dataset from individual images for '
                                                 'torchvision.datasets.ImageFolder.')
    parser.add_argument('--root', metavar='DIR', type=str, help='path to labelled images', default='train')
    args = parser.parse_args()
    generate_dataset(args.root)
