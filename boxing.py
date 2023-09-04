
import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from copy import deepcopy


def trace_box(
        path: str,
        padding: tuple[float, str] = (0, 'pixel'),
        box_inflation: [float, tuple] = 0,
        threshold_sat: int = 100,
        threshold_hue: int = 17,
        show: bool = False,
        save: bool = False
        ) -> tuple[tuple[int], tuple[int]]:
    """
    Calculates the two oposite vertices of a box envolving an instrument
    restrained in the given image.

    Parameters:
    path [str] The path of image archive;
    padding [tuple] The size of ignored boder of image;
        if padding is (int, 'pixel'): The size of border
            is equal to number of pixels given on first index;
        if padding is (float, 'percent'): The size of border
            is equal to the percentage given on first index;
    box_inflation [float, tuple] The percentage amount of increment
        of box size, if is a tuple the first index is of the
        x axis inflation and seccond is of y axis inflation;
    threshold [int] The threshold adjust of image segmentation;
    show [bool] If is True, shows the image with box traced.
    """
    img = io.imread(path)
    shape = deepcopy(img.shape)[:2]
    dim = (560,560)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    hls_img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    h = hls_img.copy()
    h[:,:,1], h[:,:,2] = hls_img[:,:,0], hls_img[:,:,0]
    s = hls_img.copy()
    s[:,:,0], s[:,:,1] = hls_img[:,:,2], hls_img[:,:,2]

    ret, thrsld_1 = cv2.threshold(s, threshold_sat, 255, cv2.THRESH_BINARY_INV)
    ret, thrsld_2 = cv2.threshold(h, threshold_hue, 255, cv2.THRESH_BINARY_INV)

    thrsld = thrsld_1 + thrsld_2

    h, w = thrsld.shape[:2]
    floodfill = thrsld.copy()

    kernel = np.ones((2, 2), np.uint8)
    floodfill = cv2.erode(floodfill, kernel, iterations=1)
    floodfill = cv2.dilate(floodfill, kernel, iterations=1)

    kernel = np.ones((9, 9), np.uint8)
    floodfill = cv2.dilate(floodfill, kernel, iterations=1)

    mask = np.zeros([h + 2, w + 2], np.uint8)

    for i in range(0, dim[0]):
        floodfill[0,i] = 255,255,255
        floodfill[i,0] = 255,255,255
        floodfill[dim[0]-1,i] = 255,255,255
        floodfill[i,dim[0]-1] = 255,255,255
    cv2.floodFill(floodfill, mask, (0,0), (0, 0, 0), (128, 128, 128), (255, 255, 255))

    thrsld = cv2.erode(floodfill, kernel, iterations=1)

    new = cv2.bitwise_and(thrsld, thrsld, mask=np.zeros((h, w), 'uint8'))
    contours, _ = cv2.findContours(cv2.cvtColor(thrsld, cv2.COLOR_BGR2GRAY), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) == 0:
        return 0
    
    empty = True
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            empty = False
            mask = np.zeros((h, w), 'uint8')
            cv2.drawContours(mask, [cnt], -1, 255, -1) 
            new += cv2.bitwise_and(thrsld, thrsld, mask=mask)

    if empty:
        return 0

    thrsld = new

    max = [None, None]
    min = [None, None]

    # if not (isinstance(padding, (tuple, list))):
    #     return 0
    
    if padding[1].lower() == "pixel":
        border = [padding[0], padding[0]]
    elif padding[1].lower() == "percent":
        border = [thrsld.shape[0]*padding[0]/100,
                  thrsld.shape[1]*padding[0]/100]
    else:
        return 0

    for y, line in enumerate(thrsld):
        for x, pxl in enumerate(line):

            if y <= border[0] \
            or y >= thrsld.shape[0] - border[0] \
            or x <= border[1] \
            or x >= thrsld.shape[1] - border[1]:
                continue

            if pxl[0] > 200:

                if max[0] is None or max[0] < x:
                    max[0] = x

                if max[1] is None or max[1] < y:
                    max[1] = y

                if min[0] is None or min[0] > x:
                    min[0] = x

                if min[1] is None or min[1] > y:
                    min[1] = y

    delta_x = max[0] - min[0]
    delta_y = max[1] - min[1]

    # if isinstance(box_inflation, (tuple, list)):
    pixels_inflation = tuple(map(int, (box_inflation[0] * delta_x / 100,
                                       box_inflation[1] * delta_y / 100)))
    # else:
    #     pixels_inflation = tuple(map(int, (box_inflation * delta_x / 100,
    #                                        box_inflation * delta_y / 100)))

    max = [max[0]+pixels_inflation[0], max[1]+pixels_inflation[1]]
    min = [min[0]-pixels_inflation[0], min[1]-pixels_inflation[1]]

    if max[0] >= thrsld.shape[1]:
        max[0] = thrsld.shape[1] - 1

    if max[1] >= thrsld.shape[0]:
        max[1] = thrsld.shape[0] - 1

    if min[0] < 0:
        min[0] = 0

    if min[1] < 0:
        min[1] = 0

    output = cv2.cvtColor(hls_img, cv2.COLOR_HLS2RGB)
    output = cv2.rectangle(output, min, max, [0,0,255], 3)
    
    min = (
        int(shape[1] * min[0] / dim[0]),
        int(shape[0] * min[1] / dim[1])
    )
    max = (
        int(shape[1] * max[0] / dim[0]),
        int(shape[0] * max[1] / dim[1])
    )

    diag_img = (dim[0]**2 + dim[1]**2)
    diag_box = (delta_x)**2 + (delta_y)**2
    if (diag_box / diag_img)**(1/2) < 0.05:
        raise ValueError("Nao foi possivel tracar uma box na imagem")

    if show:
        # img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img2 = cv2.rectangle(img, min, max, [255,0,0], 9)
        plt.imshow(img2)
        plt.show()

    # return (min, max)
    # return (cv2.cvtColor(img2, cv2.COLOR_BGR2RGB), (min, max))
    return (output, (min, max), thrsld)

if __name__ == "__main__":
    # image_count = 3750
    # # from take_images import image_count
    # path_folder = os.getcwd() + "\\examples\\"
    # paths = os.listdir(path_folder)

    # labels = open("labels.txt", "w")
    # start = datetime.now()
    # for imag, path in enumerate(paths):
    #     try:
    #         output = trace_box(
    #             path_folder + path,
    #             padding=(0, "percent"),
    #             box_inflation=(1, 1),
    #             show=False)
    #         cv2.imwrite(
    #             path_folder + "traced_examples\\" + path,
    #             output[0])
    #         labels.write(path + " -> " + str(output[1]) + "\n")
    #         os.system("cls")
    #         percent = 100 * imag / image_count
    #         label_len = 50
    #         process_label = ["#" if percent >= (i + 1) * 100 / label_len else "_" for i in range(label_len)]
    #         print("Progresso: {} de {} imagens\n".format(imag, image_count)
    #             + "".join(process_label) + f" {percent:.2f}%")
    #     except Exception as error:
    #         print("Imagem", path, "ignorada")
    #         if path[-4:] == ".jpg":
    #             shutil.copy2(path_folder + path, path_folder + "traced_examples\\discart\\" + path)
    # end = datetime.now()
    # time_lapse = end - start
    # print("Procedimento completo em {}s".format(time_lapse.seconds))
    # print(f"Aproximadamente {(time_lapse.seconds / image_count):.4f}s por imagem")

    trace_box(
        r"\\storage01\Robotica\Dataset CME\ferramentas montadas\11\fotos\frame_0080.jpg",
        padding=(0, "percent"),
        box_inflation=(1, 1),
        show=True
    )
