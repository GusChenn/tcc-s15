import os
import numpy as np
from PIL import Image

base_directory = "./outputs/images-set2/"
output_directory = "./outputs/preprocessed-set2/"
output_prefix = "preprocessed-"
output_format = "png"

def formatOutputFileName (filename, format, prefix):
    output_filename = prefix + filename
    output_filename_size = len(output_filename)
    output_filename = output_filename[:output_filename_size - 3]
    return output_filename + format

for filename in os.listdir(base_directory):
    f = os.path.join(base_directory, filename)
    if os.path.isfile(f):
        print('Aplicado mascara em: ' + f)

        original_image = Image.open(f).convert('RGB')
        mask = Image.open("./masks/tcc-mask.png").convert('L')

        original_image_array = np.array(original_image)
        mask_array = np.array(mask)

        cropped_image_array = np.dstack((original_image_array,mask_array))

        cropped_image = Image.fromarray(cropped_image_array)
        cropped_imageWithBlackBackground = mask.paste(cropped_image, (0, 0), mask)

        output_filename = formatOutputFileName(filename, output_format, output_prefix)
        output_path = os.path.join(output_directory, output_filename)
        cropped_image = cropped_image.save(output_path)
