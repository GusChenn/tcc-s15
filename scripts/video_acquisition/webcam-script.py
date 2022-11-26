# SCRIPT ADAPTADO PARA SER RODADO EM UMA MÁQUINA COM WINDOWS
import cv2
import datetime
from threading import Thread
from queue import Queue

"""
Funcoes auxiliares
"""
def getOutputName (prefix, id):
    return '.\\output\\' + str(prefix) + base_file_name + str(id) + video_file_format

def getOutputTextFormatRecording ():
    return "| Fazendo gravacao: " + str(final_time - currentTime()) + " |"

def getOutputTextFormatWaiting (counter):
    return "| Aguardando proxima gravacao: " + str(final_time - currentTime()) + " | gravacoes feitas: " + str(counter)

def currentTime ():
    return datetime.datetime.now()

def getFrame (next_record_time):
    while (currentTime() <= next_record_time + record_duration):
        ret, frame = cam.read()
        if (ret):
            print(getOutputTextFormatRecording(), end="\r")
            videoWriter.write(frame)
    return currentTime()

"""
------------------------------------------------------------------------------
Declaracao de variaveis
------------------------------------------------------------------------------
"""



#####################################
# VARIAVEIS QUE TALVEZ PRECISEM SER MUDADAS AQUI

CAM_PORT = 0 # tente os valores 1, 2, 3... e rode o script dnv

#####################################



base_file_name = "_gravado_"
video_file_format = ".mp4"
time_between_records = 10
record_duration = 30
recording_count = 0

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
cam = cv2.VideoCapture(CAM_PORT, cv2.CAP_DSHOW)
# width = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# height = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# forca FHD
width = 1920
height = 1080
fps = 30.0

# constantes tempo
initial_time = currentTime()
total_duration = datetime.timedelta(days=2)
final_time = initial_time + total_duration

time_between_records = datetime.timedelta(minutes=time_between_records)
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
        videoFileName = getOutputName(recording_count, currentTime().strftime('%Hh-%Mm'))
        videoWriter = cv2.VideoWriter(videoFileName, fourcc, fps, (int(width), int(height)))
        finished_record_time = getFrame(next_record_time)
        next_record_time = finished_record_time + time_between_records
        recording_count += 1
    print(getOutputTextFormatWaiting(recording_count), end='\r')

# Finaliza gravacao            
videoWriter.release()
cam.release()
cv2.destroyAllWindows()