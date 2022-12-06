import os
import numpy as np
from PIL import Image
import cv2

base_directory = "../image_extraction/outputs/"
output_directory = "../neural_network/images/raw/"
output_prefix = "prcsd_"
output_format = ".png"

def formatOutputFileName (filename):
    output_filename = output_prefix + filename
    output_filename_len = len(output_filename)
    output_filename = output_filename[:output_filename_len - 4]
    return output_filename + output_format


mask = Image.open("./mask.png").convert('RGB')
mask_array = np.array(mask)

for filename in os.listdir(base_directory):
    f = os.path.join(base_directory, filename)
    if os.path.isfile(f):
        print('Aplicado mascara em: ' + f)

        original_image = Image.open(f).convert('RGB')
        original_image_array = np.array(original_image)

        cropped_image_array = cv2.add(original_image_array, mask_array)
        cropped_image = Image.fromarray(cropped_image_array)

        output_filename = formatOutputFileName(filename)
        output_path = os.path.join(output_directory, output_filename)
        cropped_image = cropped_image.save(output_path)
