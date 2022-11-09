import cv2
import datetime

"""
Funcoes auxiliares
"""
def getOutputName (prefix, id):
    return str(prefix) + base_file_name + str(id) + video_file_format

def getOutputTextFormat ():
    return "| Fazendo gravacao: " + str(final_time - currentTime()) + " |"

def currentTime ():
    return datetime.datetime.now()

def getFrame (next_record_time):
    while (currentTime() <= next_record_time + record_duration):
        ret, frame = cam.read()
        if (ret):
            videoWriter.write(frame)
            print(getOutputTextFormat(), end="\r")
    return currentTime()

"""
------------------------------------------------------------------------------
Declaracao de variaveis
------------------------------------------------------------------------------
"""
base_file_name = "_record_"
video_file_format = ".mp4"
time_between_records = 20
record_duration = 5
CAM_PORT = 1
recording_count = 0
# CAM_PORT = 0 # descomentar quando estiver usando uma webcam conectada por usb
# cam = cv2.VideoCapture(CAM_PORT, cv2.CAP_DSHOW) # descomentar quando estiver usando uma webcam conectada por usb

# constantes camera
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
cam = cv2.VideoCapture(CAM_PORT)
width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = 30.0

# constantes tempo
initial_time = currentTime()
total_duration = datetime.timedelta(minutes=1)
final_time = initial_time + total_duration

time_between_records = datetime.timedelta(seconds=time_between_records)
record_duration = datetime.timedelta(seconds=record_duration)

last_record = initial_time

"""
-----------------------------------------------------------------------------
Configura gravação
-----------------------------------------------------------------------------
"""
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, fps)


"""
-----------------------------------------------------------------------------
Inicio do programa
-----------------------------------------------------------------------------
"""
print("Iniciando gravacao")

next_record_time = initial_time

while (currentTime() < final_time):
    if (currentTime() >= next_record_time):
        videoFileName = getOutputName(recording_count, currentTime())
        videoWriter = cv2.VideoWriter(videoFileName, fourcc, fps, (int(width), int(height)))
        finished_record_time = getFrame(next_record_time)
        next_record_time = finished_record_time + time_between_records
        recording_count += 1

# Finaliza gravacao            
videoWriter.release()
cam.release()
cv2.destroyAllWindows()