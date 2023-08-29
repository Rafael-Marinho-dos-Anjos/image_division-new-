
import os


folder = input("Você deseja formatar as labels de que pasta de arquivos? ")

while folder not in os.listdir("instruments"):
    folder = input("Pasta de arquivos inexistente em \\instruments, tente de novo. ")

with open(r"instruments\{}\labels.txt".format(folder), "r") as labels:
    labels_str = labels.read()

if "Label" not in os.listdir(r"instruments\{}".format(folder)):
    os.mkdir(r"instruments\{}\Label".format(folder))

if "YOLO" not in os.listdir(r"instruments\{}\Label".format(folder)):
    os.mkdir(r"instruments\{}\Label\YOLO".format(folder))

if "Open Images" not in os.listdir(r"instruments\{}\Label".format(folder)):
    os.mkdir(r"instruments\{}\Label\Open Images".format(folder))

labels_list = labels_str.split("\n")
total = len(labels_list) - 1

for count, label in enumerate(labels_list):
    if len(label) < 3:
        continue
    image_path, _, xmin, ymin, xmax, ymax = label.split()
    open_images_ds_notation = f"{folder} {xmin[2:-1]} {ymin[:-2]} {xmax[1:-1]} {ymax[:-2]}"
    width = int(xmax[1:-1]) - int(xmin[2:-1])
    height = int(ymax[:-2]) - int(ymin[:-2])
    yolo_notation = f"{folder} {xmin[2:-1]} {ymin[:-2]} {width} {height}"
    image_path = image_path[:-3] + "txt"

    with open(r"instruments\{}\Label\Open Images\{}".format(folder, image_path), "w") as notation:
        notation.write(open_images_ds_notation)

    with open(r"instruments\{}\Label\YOLO\{}".format(folder, image_path), "w") as notation:
        notation.write(yolo_notation)
    
    os.system("cls")
    count += 1
    percent = 100 * count / total
    label_len = 50
    process_label = ["#" if percent >= (i + 1) * 100 / label_len else "_" for i in range(label_len)]
    print("Progresso: {} de {} labels\n".format(count, total)
        + "".join(process_label) + f" {percent:.2f}%")
