import os

diretorio = os.fsencode("..\\video_acquisition\\output")

for video in os.listdir(diretorio):
  print(video) 
