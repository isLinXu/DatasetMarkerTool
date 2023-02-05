import os
import sys
import shutil
import numpy as np


def load_data(data_path):
    count = 0
    data = {}
    for dir_name in os.listdir(data_path):
        dir_path = os.path.join(data_path, dir_name)
        if not os.path.isdir(dir_path):
            continue

        data[dir_name] = []
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            if not os.path.isfile(file_path):
                continue
            data[dir_name].append(file_path)

        count += len(data[dir_name])
        print("{} : {}".format(dir_name, len(data[dir_name])))

    print("total of image : {}".format(count))
    return data


def copy_dataset(src_img_list, data_index, target_path):
    target_img_list = []
    for index in data_index:
        src_img = src_img_list[index]
        img_name = os.path.split(src_img)[-1]

        shutil.copy(src_img, target_path)
        target_img_list.append(os.path.join(target_path, img_name))
    return target_img_list


def write_file(data, file_name):
    if isinstance(data, dict):
        write_data = []
        for lab, img_list in data.items():
            for img in img_list:
                write_data.append("{} {}".format(img, lab))
    else:
        write_data = data

    with open(file_name, "w") as f:
        for line in write_data:
            f.write(line + "\n")
    
    print("{} write over!".format(file_name))

def split_data(src_data_path, target_data_path, train_rate=0.8):
    src_data_dict = load_data(src_data_path)

    classes = []
    train_dataset, val_dataset = {}, {}
    train_count,val_count = 0, 0
    for i, (cls_name, img_list) in enumerate(src_data_dict.items()):
        img_data_size = len(img_list)
        random_index = np.random.choice(img_data_size, img_data_size, replace=False)

        train_data_size = int(img_data_size * train_rate)
        train_data_index = random_index[:train_data_size]
        val_data_index = random_index[train_data_size:]

        train_data_path = os.path.join(target_data_path, "train", cls_name)
        val_data_path = os.path.join(target_data_path, "val", cls_name)
        os.makedirs(train_data_path, exist_ok=True)
        os.makedirs(val_data_path, exist_ok=True)

        classes.append(cls_name)
        train_dataset[i] = copy_dataset(img_list, train_data_index, train_data_path)
        val_dataset[i] = copy_dataset(img_list, val_data_index, val_data_path)

        print("target {} train:{}, val:{}".format(cls_name, len(train_dataset[i]), len(val_dataset[i])))
        train_count += len(train_dataset[i])
        val_count += len(val_dataset[i])

    print("train size:{}, val size:{}, total:{}".format(train_count, val_count,train_count + val_count))
    write_file(classes, os.path.join(target_data_path,"classes.txt"))
    write_file(train_dataset, os.path.join(target_data_path,"train.txt"))
    write_file(val_dataset, os.path.join(target_data_path,"val.txt"))


def main():
    src_data_path = sys.argv[1]
    target_data_path = sys.argv[2]
    split_data(src_data_path, target_data_path, train_rate=0.8)


if __name__ == '__main__':
    main()