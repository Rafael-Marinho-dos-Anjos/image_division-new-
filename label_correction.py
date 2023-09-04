""" Conversion module to labeling resized images
"""
import os


WIDTH = 3840
HEIGHT = 2160

LABEL_WIDTH = 560
LABEL_HEIGHT = 560

folders = [ 
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "cabo"
    # , "1_1",
    # "1_2", "1_3", "1_4", "2_1",
    # "2_2", "2_3", "2_4", "3_1",
    # "3_2", "4_1", "4_2", "4_3",
    # "4_4", "5_1", "5_2"
]

def convert_label(label_text) -> str:
    label_text = label_text.split(" ")
    label_text[1] = str(int(WIDTH * int(label_text[1]) / LABEL_WIDTH))
    label_text[2] = str(int(HEIGHT * int(label_text[2]) / LABEL_HEIGHT))
    label_text[3] = str(int(WIDTH * int(label_text[3]) / LABEL_WIDTH))
    label_text[4] = str(int(HEIGHT * int(label_text[4]) / LABEL_HEIGHT))
    label_text = " ".join(label_text)
    return label_text

parent_path = "instruments\\"

for folder in folders:
    yolo_labels = os.listdir(parent_path + folder + "\\Label\\YOLO")
    open_images_labels = os.listdir(parent_path + folder + "\\Label\\Open Images")

    for label in yolo_labels:
        with open(parent_path + folder + "\\Label\\YOLO\\" + label, "r") as label_txt:
            text = label_txt.read()
        text = convert_label(text)
        with open(parent_path + folder + "\\Label\\YOLO\\" + label, "w") as label_txt:
            label_txt.write(text)

    for label in open_images_labels:
        with open(parent_path + folder + "\\Label\\Open Images\\" + label, "r") as label_txt:
            text = label_txt.read()
        text = convert_label(text)
        with open(parent_path + folder + "\\Label\\Open Images\\" + label, "w") as label_txt:
            label_txt.write(text)
