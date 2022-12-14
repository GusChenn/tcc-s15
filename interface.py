import os

print("")
print("-"*80)
print("Software de supervisão de processo de refino do cacau - Amazonia 4.0.")
print("Trabalho de conclusão de curso, grupo S15")
print("V1.0")
print("-"*80)
print("")
print("")

print("Opcoes:")
print("1. Rotina de treinamento")
print("2. Rotina de supervisao")
print("")

rotina = input("Selecione a rotina a ser executada: ")

if int(rotina) == 1:
  print("Rotina selecionada: Rotina de treinamento")
  os.system("python3 .\\scripts\\video_acquisition\\webcam-script.py")
  os.system("./")
elif int(rotina) == 2:
  print("Rotina selecionada: Rotina de supervisao")