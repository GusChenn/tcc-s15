import numpy as np
from PIL import Image

originalImage = Image.open("./outputs/images-set4/set4000053.bmp").convert('RGB')
mask = Image.open("./tcc-mask.png").convert('L')

originalImageArray = np.array(originalImage)
maskArray = np.array(mask)

croppedImageArray = np.dstack((originalImageArray,maskArray))

croppedImage = Image.fromarray(croppedImageArray)
# display(croppedImage)
croppedImageWithBlackBackground = mask.paste(croppedImage, (0, 0), mask)
croppedImage = croppedImage.save("final.png")
