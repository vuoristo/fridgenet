from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
import numpy as np
import os
from PIL import Image

NUM_CATEGORIES = 2
NUM_STEPS = 1000

def build_model(num_categories):
  model = Sequential()
  # input: 100x100 images with 3 channels -> (3, 100, 100) tensors.
  # this applies 32 convolution filters of size 3x3 each.
  model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=(3, 100, 100)))
  model.add(Activation('relu'))
  model.add(Convolution2D(32, 3, 3))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))

  model.add(Convolution2D(64, 3, 3, border_mode='valid'))
  model.add(Activation('relu'))
  model.add(Convolution2D(64, 3, 3))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))

  model.add(Flatten())
  # Note: Keras does automatic shape inference.
  model.add(Dense(256))
  model.add(Activation('relu'))
  model.add(Dropout(0.5))

  model.add(Dense(num_categories))
  model.add(Activation('softmax'))

  sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
  model.compile(loss='categorical_crossentropy', optimizer=sgd)
  return model

def get_filenames_and_categories(path):
  filenames = []
  category_names = []
  categories = []
  for root, dirs, files in os.walk(path):
    root_list = root.split('/')
    if len(root_list) == 2:
      cat_name = root_list[1]
      category_names.append(cat_name)
      cat = category_names.index(cat_name)
      for f in files:
        filenames.append(root + '/' + f)
        categories.append(cat)

  return np.array(filenames), np.array(categories), len(category_names)

def get_batch(batch_size, img_size, filenames,
              categories, num_categories):
  indexes = np.random.choice(len(filenames), batch_size)
  batch_names = filenames[indexes]
  batch_categories = categories[indexes]
  batch_images = [np.array(
    Image.open(name).convert('RGB').resize(img_size)) for name in batch_names]
  batch_images = np.array(batch_images)
  batch_images = np.moveaxis(batch_images, -1, 1)
  batch_categories_one_hot = np.zeros((batch_size, num_categories))
  batch_categories_one_hot[np.arange(batch_size), batch_categories] = 1

  return batch_images, batch_categories_one_hot

def train(model, num_steps):
  fnames, cats, num_cats = get_filenames_and_categories('img')
  for step in range(num_steps):
    batch_imgs, batch_cats = get_batch(
        4, (100,100), fnames, cats, num_cats)
    model.train_on_batch(batch_imgs, batch_cats)

model = build_model(NUM_CATEGORIES)
train(model, NUM_STEPS)

model.save('trained_model')
