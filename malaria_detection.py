# -*- coding: utf-8 -*-
"""Malaria_detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZtyzrXSQe_dVh1eHskTP5YtajBemCQTI
"""

!wget https://github.com/krishnaik06/Malaria-Detection/blob/master/Dataset.zip

import zipfile
 
zip_ref = zipfile.ZipFile("/content/Dataset.zip", 'r')
zip_ref.extractall()

from keras.layers import Input, Lambda, Dense, Flatten
from keras.models import Model
#from keras.applications.vgg16 import VGG16
from keras.applications.vgg19 import VGG19
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
 
# re-size all the images to this
IMAGE_SIZE = [224, 224]
 
train_path = '/content/Dataset/Train'
valid_path = '/content/Dataset/Test'
 
# add preprocessing layer to the front of VGG
vgg = VGG19(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)
 
# don't train existing weights
for layer in vgg.layers:
  layer.trainable = False
  
 
  
  # useful for getting number of classes
folders = glob('/content/Dataset/Train/*')
  
 
# our layers - you can add more if you want
x = Flatten()(vgg.output)
# x = Dense(1000, activation='relu')(x)
prediction = Dense(len(folders), activation='softmax')(x)
 
# create a model object
model = Model(inputs=vgg.input, outputs=prediction)
 
# view the structure of the model
model.summary()
 
# tell the model what cost and optimization method to use
model.compile(
  loss='categorical_crossentropy',
  optimizer='adam',
  metrics=['accuracy']
)
 
 
# Use the Image Data Generator to import the images from the dataset
from keras.preprocessing.image import ImageDataGenerator
 
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)
 
test_datagen = ImageDataGenerator(rescale = 1./255)
 
training_set = train_datagen.flow_from_directory('/content/Dataset/Train',
                                                 target_size = (224, 224),
                                                 batch_size = 32,
                                                 class_mode = 'categorical')
 
test_set = test_datagen.flow_from_directory('/content/Dataset/Test',
                                            target_size = (224, 224),
                                            batch_size = 32,
                                            class_mode = 'categorical')
 
 
# fit the model
r = model.fit_generator(
  training_set,
  validation_data=test_set,
  epochs=5,
  steps_per_epoch=len(training_set),
  validation_steps=len(test_set)
)
# loss
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.show()
plt.savefig('LossVal_loss')
 
# accuracies
plt.plot(r.history['acc'], label='train acc')
plt.plot(r.history['val_acc'], label='val acc')
plt.legend()
plt.show()
plt.savefig('AccVal_acc')
 
import tensorflow as tf
 
from keras.models import load_model
 
model.save('model_vgg19.h5')

MODEL_PATH ='model_vgg19.h5'
 
# Load your trained model
model = load_model(MODEL_PATH)
 
 
def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))
 
    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   
 
    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)
 
    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="The Person is Infected With Pneumonia"
    else:
        preds="The Person is not Infected With Pneumonia"
    
    
    return preds

model_predict('/content/Dataset/Test/Parasite/C39P4thinF_original_IMG_20150622_105554_cell_10.png',model)