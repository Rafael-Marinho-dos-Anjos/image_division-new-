import os
import shutil
from random import choice

destination_folder = os.getcwd() + r"\examples"
os.system("cls")
path = r"\\storage01\Robotica\Dataset CME\ferramentas montadas"
folders = os.listdir(path)

image_count = 0
for folder in folders:
    try:
        folder_path = path + r"\{}\fotos".format(folder)
        images = os.listdir(folder_path)
        selected_images = [choice(images) for i in range(250)]
        for image in selected_images:
            image_count += 1
            shutil.copy2(folder_path+"\\"+image, destination_folder+"\\image_{}.jpg".format(image_count))
            os.system("cls")
            print("Copiando arquivos...")
            print("Arquivo", image, "copiado")
    except Exception as error:
        print(error)
