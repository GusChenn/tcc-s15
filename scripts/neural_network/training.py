#!/usr/bin/env python
# coding: utf-8

# ## Setup

# In[1]:


import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ### Filter out corrupted images
# 
# When working with lots of real-world image data, corrupted images are a common
# occurence. Let's filter out badly-encoded images that do not feature the string "JFIF"
# in their header.

# In[ ]:

# ## Generate a `Dataset`

# In[5]:


image_size = (180, 180)
batch_size = 32

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "Massas",
    validation_split=0.2,
    subset="training",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)
val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    "Massas",
    validation_split=0.2,
    subset="validation",
    seed=1337,
    image_size=image_size,
    batch_size=batch_size,
)


# ## Visualize the data
# 
# Here are the first 9 images in the training dataset. As you can see, label 1 is "dog"
# and label 0 is "cat".

# In[6]:

# ## Using image data augmentation
# 
# When you don't have a large image dataset, it's a good practice to artificially
# introduce sample diversity by applying random yet realistic transformations to the
# training images, such as random horizontal flipping or small random rotations. This
# helps expose the model to different aspects of the training data while slowing down
# overfitting.

# In[8]:


data_augmentation = keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
    ]
)


# Let's visualize what the augmented samples look like, by applying `data_augmentation`
# repeatedly to the first image in the dataset:

# In[9]:

# ## Standardizing the data
# 
# Our image are already in a standard size (180x180), as they are being yielded as
# contiguous `float32` batches by our dataset. However, their RGB channel values are in
# the `[0, 255]` range. This is not ideal for a neural network;
# in general you should seek to make your input values small. Here, we will
# standardize values to be in the `[0, 1]` by using a `Rescaling` layer at the start of
# our model.

# ## Two options to preprocess the data
# 
# There are two ways you could be using the `data_augmentation` preprocessor:
# 
# **Option 1: Make it part of the model**, like this:
# 
# ```python
# inputs = keras.Input(shape=input_shape)
# x = data_augmentation(inputs)
# x = layers.Rescaling(1./255)(x)
# ...  # Rest of the model
# ```
# 
# With this option, your data augmentation will happen *on device*, synchronously
# with the rest of the model execution, meaning that it will benefit from GPU
# acceleration.
# 
# Note that data augmentation is inactive at test time, so the input samples will only be
# augmented during `fit()`, not when calling `evaluate()` or `predict()`.
# 
# If you're training on GPU, this may be a good option.
# 
# **Option 2: apply it to the dataset**, so as to obtain a dataset that yields batches of
# augmented images, like this:
# 
# ```python
# augmented_train_ds = train_ds.map(
#     lambda x, y: (data_augmentation(x, training=True), y))
# ```
# 
# With this option, your data augmentation will happen **on CPU**, asynchronously, and will
# be buffered before going into the model.
# 
# If you're training on CPU, this is the better option, since it makes data augmentation
# asynchronous and non-blocking.
# 
# In our case, we'll go with the second option. If you're not sure
# which one to pick, this second option (asynchronous preprocessing) is always a solid choice.

# ## Configure the dataset for performance
# 
# Let's make sure to use buffered prefetching so we can yield data from disk without
# having I/O becoming blocking:

# In[10]:


train_ds = train_ds.prefetch(buffer_size=32)
val_ds = val_ds.prefetch(buffer_size=32)


# ## Build a model
# 
# We'll build a small version of the Xception network. We haven't particularly tried to
# optimize the architecture; if you want to do a systematic search for the best model
#  configuration, consider using
# [KerasTuner](https://github.com/keras-team/keras-tuner).
# 
# Note that:
# 
# - We start the model with the `data_augmentation` preprocessor, followed by a
#  `Rescaling` layer.
# - We include a `Dropout` layer before the final classification layer.

# In[14]:



def make_model(input_shape, num_classes):
    inputs = keras.Input(shape=input_shape)

    # Entry block
    x = layers.Rescaling(1.0 / 255)(inputs)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.Conv2D(64, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    previous_block_activation = x  # Set aside residual

    for size in [128, 256, 512, 728]:
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(size, 3, padding="same")(x)
        x = layers.BatchNormalization()(x)

        x = layers.MaxPooling2D(3, strides=2, padding="same")(x)

        # Project residual
        residual = layers.Conv2D(size, 1, strides=2, padding="same")(
            previous_block_activation
        )
        x = layers.add([x, residual])  # Add back residual
        previous_block_activation = x  # Set aside next residual

    x = layers.SeparableConv2D(1024, 3, padding="same")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Activation("relu")(x)

    x = layers.GlobalAveragePooling2D()(x)
    if num_classes == 2:
        activation = "sigmoid"
        units = 1
    else:
        activation = "softmax"
        units = num_classes

    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(units, activation=activation)(x)
    return keras.Model(inputs, outputs)

model = make_model(input_shape=image_size + (3,), num_classes=2)


# And let's apply data augmentation to our training dataset:

# In[15]:


# Apply `data_augmentation` to the training images.
train_ds = train_ds.map(
    lambda img, label: (data_augmentation(img), label),
    num_parallel_calls=tf.data.AUTOTUNE,
)
# Prefetching samples in GPU memory helps maximize GPU utilization.
train_ds = train_ds.prefetch(tf.data.AUTOTUNE)


# ## Train the model

# In[16]:


epochs = 50

callbacks = [
    keras.callbacks.ModelCheckpoint("save_at_{epoch}.keras"),
]
model.compile(
    optimizer=keras.optimizers.Adam(1e-3),
    loss="binary_crossentropy",
    metrics=["accuracy"],
)
model.fit(
    train_ds,
    epochs=epochs,
    callbacks=callbacks,
    validation_data=val_ds,
)


# We get to ~96% validation accuracy after training for 50 epochs on the full dataset.

# ## Run inference on new data
# 
# Note that data augmentation and dropout are inactive at inference time.

# In[ ]:


img = keras.preprocessing.image.load_img(
    "PetImages/Cat/6779.jpg", target_size=image_size
)
img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Create batch axis

predictions = model.predict(img_array)
score = predictions[0]
print(f"This image is {100 * (1 - score):.2f}% cat and {100 * score:.2f}% dog.")

