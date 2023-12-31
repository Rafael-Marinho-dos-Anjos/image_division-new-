""" Conversion module to labeling resized images
"""
import os


WIDTH = 1
HEIGHT = 1

LABEL_WIDTH = 3840
LABEL_HEIGHT = 2160

folders = [ 
    # "1", "2", "3", "4", "5",
    # "6", "7", "8", "9", "10",
    # "11", "12", "13", "14", "cabo",
    # "1_1",
    # "1_2", "1_3", "1_4", "2_1",
    # "2_2", "2_3", "2_4", 
    "7"
    # "cabo"
]

def convert_label(label_text) -> str:
    label_text = label_text.split(" ")
    label_text[1] = str((WIDTH * float(label_text[1]) / LABEL_WIDTH))
    label_text[2] = str((HEIGHT * float(label_text[2]) / LABEL_HEIGHT))
    label_text[3] = str((WIDTH * float(label_text[3]) / LABEL_WIDTH))
    label_text[4] = str((HEIGHT * float(label_text[4]) / LABEL_HEIGHT))
    label_text = " ".join(label_text)
    return label_text

parent_path = "instruments\\"
bar_length = 50

for i, folder in enumerate(folders):
    yolo_labels = os.listdir(parent_path + folder + "\\Label\\YOLO")
    open_images_labels = os.listdir(parent_path + folder + "\\Label\\Open Images")

    for j, label in enumerate(yolo_labels):
        with open(parent_path + folder + "\\Label\\YOLO\\" + label, "r") as label_txt:
            text = label_txt.read()

        text = convert_label(text)
        with open(parent_path + folder + "\\Label\\YOLO\\" + label, "w") as label_txt:
            label_txt.write(text)

        process_bar = ""
        for bar_dot in range(bar_length):
            process_bar += "#" if (j / (2 * len(yolo_labels))) * bar_length >= bar_dot else "_"

        percent = j / (2 * len(yolo_labels))
        percent *= 100
        print("""folder {} of {}\n{} {}%""".
        format(i+1, len(folders), process_bar, percent))

    for j, label in enumerate(open_images_labels):
        with open(parent_path + folder + "\\Label\\Open Images\\" + label, "r") as label_txt:
            text = label_txt.read()

        text = convert_label(text)
        with open(parent_path + folder + "\\Label\\Open Images\\" + label, "w") as label_txt:
            label_txt.write(text)

        process_bar = ""
        for bar_dot in range(bar_length):
            process_bar += "#" if (j / (2 * len(yolo_labels)) + 0.5) * bar_length >= bar_dot else "_"

        percent = j / (2 * len(yolo_labels)) + 0.5
        percent *= 100
        print("""folder {} of {}\n{} {}%""".
        format(i+1, len(folders), process_bar, percent))
