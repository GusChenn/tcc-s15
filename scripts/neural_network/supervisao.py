import numpy as np
from tensorflow import keras
import os

image_size = (180, 180)
prediction_images_dir = "./images/ready_to_predict/"
images = []
batch_size = 10
limiar_de_decisa = 0.5

# Carrega todas as imagens a serem analisadas em uma lista
print("Gerando vetor de imagens a serem analisadas...")
for filename in os.listdir(prediction_images_dir):
  f = os.path.join(prediction_images_dir, filename)
  if os.path.isfile(f):
    img = keras.preprocessing.image.load_img(f, target_size=image_size)
    img = keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    images.append(img)


# Carrega modelo
print("Carregando modelo...")
loaded_model = keras.models.load_model("modelo_treinado")
loaded_model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Empilha imagens
print("Manipulando imagens...")
images = np.vstack(images)

# Gera predições
print("Fazendo previsão...")
predictions = loaded_model.predict(images, batch_size=batch_size)

# pronto = 1; n pronto = 0
predictions = np.where(predictions > limiar_de_decisa, 1, 0)

positive = np.count_nonzero(predictions == 1)
negative = np.count_nonzero(predictions == 0)

print("Resultado predicao: {} imagens prontas, {} imagens nao prontas".format(positive, negative))

if positive > negative:
  print("esta pronto")
else:
  print("n esta pronto")