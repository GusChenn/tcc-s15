import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from xceptino_simplificado import xception_simplificado

# Constantes
image_size = (180, 180)
batch_size = 32
epochs = 60

# Gera datasets
print("Gerando datasets...")
train_ds, val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    ".\images\Massas",
    validation_split=0.3,
    subset="both",
    color_mode="rgb",
    seed=1212,
    image_size=image_size,
    batch_size=batch_size,
)

# Prefetch dos datasets 
print("Fazendo prefetch...")
train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)

# Carrega modelo
print("Carregando modelo...")
model = xception_simplificado()
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)

# Treina o modelo
print("Treinando modelo...")
model.fit(
    train_ds,
    epochs=epochs,
    validation_data=val_ds,
)

# Salva os pesos
print("Salvando modelo...")
model.save("modelo_treinado")