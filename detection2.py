import os
from boxing import trace_box
from cv2 import imwrite
from datetime import datetime


ok = False

path = r"\\storage01\Robotica\Dataset CME\ferramentas desmontadas kit trocater"
folders = os.listdir(path)

# for folder in folders:

folder = 4
subfolders = os.listdir(r"{}\{}".format(path, folder))
for subfolder in subfolders:
        folder_path = r"{}\{}\{}\fotos".format(path, folder, subfolder)
        images = os.listdir(folder_path)
        instrument = "{}_{}".format(folder, subfolder)
        destination_folder = os.getcwd() + instrument

        if "instruments" not in os.listdir():
            os.mkdir(r"instruments")

        if instrument not in os.listdir("instruments"):
            os.mkdir(r"instruments\{}".format(instrument))

        if "validation_images" not in os.listdir(r"instruments\{}".format(instrument)):
            os.mkdir(r"instruments\{}\validation_images".format(instrument))

        os.chdir(r"instruments\{}".format(instrument))
        image_count = len(images)

        with open("labels.txt", "w") as labels:
            start = datetime.now()

            for i, image in enumerate(images):

                try:
                    output = trace_box(
                        folder_path + "\\" + image,
                        padding=(0, "percent"),
                        box_inflation=(3, 3),
                        threshold_sat=120,
                        threshold_hue=12,
                        show=False)
                    imwrite(
                        "validation_images\\" + image,
                        output[0])
                    labels.write(image + " -> " + str(output[1]) + "\n")
                    os.system("cls")
                    percent = 100 * i / image_count
                    label_len = 50
                    process_label = ["#" if percent >= (i + 1) * 100 / label_len else "_" for i in range(label_len)]
                    print("Ferramenta: {}".format(instrument))
                    print("Progresso: {} de {} imagens\n".format(i, image_count)
                        + "".join(process_label) + f" {percent:.2f}%")
                    
                except Exception as error:
                    print("Imagem", image, "ignorada")
                    # print(error)
                    
            end = datetime.now()
            time_lapse = end - start
            print("Procedimento completo em {}s".format(time_lapse.seconds))
            print(f"Aproximadamente {(time_lapse.seconds / image_count):.4f}s por imagem")
