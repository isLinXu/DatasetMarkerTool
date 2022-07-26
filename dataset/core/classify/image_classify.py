import tkinter as tk
from tkinter.messagebox import showinfo
import os
from PIL import Image, ImageTk

dir_path = "/home/linxu/Desktop/coco128/coco128/images/train2017/"  # 文件夹路径
prefix = "marked"  # 文本标记过后的前缀，防止重复标记

top = tk.Tk()
top.title("图片标记器")
width = 640
height = 480
top.geometry(f'{width}x{height}')


# 标记当前图片，并切换到下一个图片
def next_img(type):
    global index
    o_name = img_file_names[index]
    o_path = dir_path + "/" + o_name
    n_name = prefix + "_" + type + "_" + o_name
    n_path = dir_path + "/" + n_name
    # 重命名文件  abc.png-->marked_1_abc.png
    os.rename(o_path, n_path)

    # 如果是最后一个，给出提示，关闭程序
    if index + 1 >= len(imgs):
        showinfo(title='提示', message='已经是最后一个')
        top.destroy()
        return
    # 索引加1，更换图片
    index = index + 1
    label_img.configure(image=imgs[index])


imgs = []  # 所有图片
img_file_names = []  # 所有图片的名称
all_files = os.listdir(dir_path)
for f_name in all_files:  # 遍历所有图片
    if f_name.startswith(prefix) or not f_name.endswith(".jpg"):
        continue  # 如果已经标注过了，下一个
    img_path = dir_path + "/" + f_name
    img = Image.open(img_path)  # 打开图片
    photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
    # 把图片和名称存储起来
    imgs.append(photo)
    img_file_names.append(f_name)

# 先展示第一个
index = 0
label_img = tk.Label(top, image=imgs[index])
label_img.place(x=20, y=20)

class_names = ['空调', '烧烤', '海滩', '蝉', '赛龙舟', '电风扇', '雪糕', '泳衣', '西瓜', '粽子']


# 按键的回调
def callback(event):
    c = event.char  # 获取键盘输入
    if c in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "x"]:
        # 如果输入的是上面的数字，就给这幅图分类改名字
        next_img(str(c))


# 绑定键盘事件
frame = tk.Frame(top, width=20, height=20)
frame.bind("<Key>", callback)
frame.focus_set()
frame.pack()

# 摆放数字
b_x = 160  # 基础X位置
b_y = -10  # 基础Y位置
d_l = 75  # 间距
button = tk.Button(top, text="1 " + class_names[1], command=lambda: next_img("1"))
button.place(x=b_x, y=b_y + 1 * d_l)
button = tk.Button(top, text="2 " + class_names[2], command=lambda: next_img("2"))
button.place(x=b_x, y=b_y + 2 * d_l)
button = tk.Button(top, text="3 " + class_names[3], command=lambda: next_img("3"))
button.place(x=b_x, y=b_y + 3 * d_l)
button = tk.Button(top, text="4 " + class_names[4], command=lambda: next_img("4"))
button.place(x=b_x, y=b_y + 4 * d_l)
button = tk.Button(top, text="5 " + class_names[5], command=lambda: next_img("5"))
button.place(x=b_x, y=b_y + 5 * d_l)

button = tk.Button(top, text="6 " + class_names[6], command=lambda: next_img("6"))
button.place(x=b_x + d_l, y=b_y + 1 * d_l)
button = tk.Button(top, text="7 " + class_names[7], command=lambda: next_img("7"))
button.place(x=b_x + d_l, y=b_y + 2 * d_l)
button = tk.Button(top, text="8 " + class_names[8], command=lambda: next_img("8"))
button.place(x=b_x + d_l, y=b_y + 3 * d_l)
button = tk.Button(top, text="9 " + class_names[9], command=lambda: next_img("9"))
button.place(x=b_x + d_l, y=b_y + 4 * d_l)
button = tk.Button(top, text="0 " + class_names[0], command=lambda: next_img("0"))
button.place(x=b_x + d_l, y=b_y + 5 * d_l)

top.mainloop()


def image_classify_action(dir_path, prefix):
    dir_path = "/home/linxu/Desktop/coco128/coco128/images/train2017/"  # 文件夹路径
    prefix = "marked"  # 文本标记过后的前缀，防止重复标记

    top = tk.Tk()
    top.title("图片标记器")
    width = 640
    height = 480
    top.geometry(f'{width}x{height}')

    imgs = []  # 所有图片
    img_file_names = []  # 所有图片的名称
    all_files = os.listdir(dir_path)
    for f_name in all_files:  # 遍历所有图片
        if f_name.startswith(prefix) or not f_name.endswith(".jpg"):
            continue  # 如果已经标注过了，下一个
        img_path = dir_path + "/" + f_name
        img = Image.open(img_path)  # 打开图片
        photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
        # 把图片和名称存储起来
        imgs.append(photo)
        img_file_names.append(f_name)

    # 先展示第一个
    index = 0
    label_img = tk.Label(top, image=imgs[index])
    label_img.place(x=20, y=20)

    class_names = ['空调', '烧烤', '海滩', '蝉', '赛龙舟', '电风扇', '雪糕', '泳衣', '西瓜', '粽子']

    # 绑定键盘事件
    frame = tk.Frame(top, width=20, height=20)
    frame.bind("<Key>", callback)
    frame.focus_set()
    frame.pack()

    # 摆放数字
    b_x = 160  # 基础X位置
    b_y = -10  # 基础Y位置
    d_l = 75  # 间距
    button = tk.Button(top, text="1 " + class_names[1], command=lambda: next_img("1"))
    button.place(x=b_x, y=b_y + 1 * d_l)
    button = tk.Button(top, text="2 " + class_names[2], command=lambda: next_img("2"))
    button.place(x=b_x, y=b_y + 2 * d_l)
    button = tk.Button(top, text="3 " + class_names[3], command=lambda: next_img("3"))
    button.place(x=b_x, y=b_y + 3 * d_l)
    button = tk.Button(top, text="4 " + class_names[4], command=lambda: next_img("4"))
    button.place(x=b_x, y=b_y + 4 * d_l)
    button = tk.Button(top, text="5 " + class_names[5], command=lambda: next_img("5"))
    button.place(x=b_x, y=b_y + 5 * d_l)

    button = tk.Button(top, text="6 " + class_names[6], command=lambda: next_img("6"))
    button.place(x=b_x + d_l, y=b_y + 1 * d_l)
    button = tk.Button(top, text="7 " + class_names[7], command=lambda: next_img("7"))
    button.place(x=b_x + d_l, y=b_y + 2 * d_l)
    button = tk.Button(top, text="8 " + class_names[8], command=lambda: next_img("8"))
    button.place(x=b_x + d_l, y=b_y + 3 * d_l)
    button = tk.Button(top, text="9 " + class_names[9], command=lambda: next_img("9"))
    button.place(x=b_x + d_l, y=b_y + 4 * d_l)
    button = tk.Button(top, text="0 " + class_names[0], command=lambda: next_img("0"))
    button.place(x=b_x + d_l, y=b_y + 5 * d_l)

    top.mainloop()
