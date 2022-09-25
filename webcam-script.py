import cv2

# Ctes
CAM_PORT = 0
cam = cv2.VideoCapture(CAM_PORT, cv2.CAP_DSHOW)
base_file_name = "video_"

# Define os parametros de gravacao do video
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
video_file_format = ".avi"

# ----------------------------------------------
# ALTERAR AQ
recording_time_in_seconds = 2 
# ----------------------------------------------

recording_quantity = 1

def defineFileName (index):
    return base_file_name + str(index) + video_file_format

# 1000 loops = mais ou menos 30s
def recordingTimeInLoops (seconds):
    loops = seconds * 33
    return loops

recording_time = recordingTimeInLoops(recording_time_in_seconds)
recording_time_fraction = recording_time / 3

# Comeca a puxar os frames
for i in range (recording_quantity):
    videoFileName = defineFileName(i)
    videoWriter = cv2.VideoWriter(videoFileName, fourcc, 30.0, (1920,1080))
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cam.set(cv2.CAP_PROP_FPS, 30)
    print("Iniciando gravacao " + str(i))
    for j in range (recording_time):
        ret, frame = cam.read()
        if (ret):
            videoWriter.write(frame)
            if (j < 1 * recording_time_fraction):
                print("gravando.  resolucao: " + str(frame.shape[0]) + " x " + str(frame.shape[1]), end="\r")
            elif (j > 1 * recording_time_fraction and j < 2 * recording_time_fraction):
                print("gravando.. resolucao: " + str(frame.shape[0]) + " x " + str(frame.shape[1]), end="\r")
            elif (j > 2 * recording_time_fraction and j < 3 * recording_time_fraction):
                print("gravando... resolucao: " + str(frame.shape[0]) + " x " + str(frame.shape[1]), end="\r")
    videoWriter.release()
cam.release()
cv2.destroyAllWindows()

