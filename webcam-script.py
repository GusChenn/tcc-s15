import cv2

CAM_PORT = 0
cam = cv2.VideoCapture(CAM_PORT)
result, image = cam.read()

if result:
    cv2.imshow("imagem", image)
else:
    print("Problema")
