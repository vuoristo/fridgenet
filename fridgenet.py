from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K
import numpy as np
import os
import argparse

from PIL import Image

NUM_CATEGORIES = 8
NUM_STEPS = 1000 * 80
NUM_EPOCH = 2000
MINI_BATCH_SIZE = 10

class ImageLoader(object):
  def __init__(self, mini_batch_size, filenames, categories, num_categories):
    self.mini_batch_size = mini_batch_size
    self.cache = {}
    self.filenames = filenames
    self.categories = categories
    self.num_categories = num_categories
    self.image_size = (100, 100)

  def get_image(self, filepath):
    image = self.cache.get(filepath, None)
    if image:
      return image
    else:
      image = Image.open(filepath).convert('RGB').resize(self.image_size)
      self.cache[filepath] = image
      return image

  def get_images(self, count):
    indexes = np.random.choice(len(self.filenames), count)
    batch_names = self.filenames[indexes]
    batch_categories = self.categories[indexes]
    batch_images = [np.array(self.get_image(name)) for name in batch_names]
    batch_images = np.array(batch_images)
    batch_images = np.moveaxis(batch_images, -1, 1)
    batch_categories_one_hot = np.zeros((count, self.num_categories))
    batch_categories_one_hot[np.arange(count), batch_categories] = 1

    return batch_images, batch_categories_one_hot

  def get_all(self):
    return self.get_images(len(self.filenames))

  def get_batch(self):
    return self.get_images(self.mini_batch_size)

  def shuffle(self):
    image_count = len(self.filenames)
    mask = np.random.choice(np.arange(image_count), image_count, replace=False)
    new_filenames = self.filenames[mask]
    new_categories = self.categories[mask]
    return ImageLoader(self.mini_batch_size, new_filenames, new_categories, self.num_categories)

  def split(self, ratio):
    total = len(self.filenames)
    validation_examples = int(total * (1 - ratio))
    training_examples = total - validation_examples
    training_images = self.filenames[0:training_examples]
    training_labels = self.categories[0:training_examples]
    validation_images = self.filenames[-validation_examples:]
    validation_labels = self.categories[-validation_examples:]

    training_data = ImageLoader(self.mini_batch_size, training_images, training_labels, self.num_categories)
    validation_data = ImageLoader(self.mini_batch_size, validation_images, validation_labels, self.num_categories)
    return training_data, validation_data

def build_model(num_categories):
  K.set_image_dim_ordering('th')

  model = Sequential()
  # input: 100x100 images with 3 channels -> (3, 100, 100) tensors.
  # this applies 32 convolution filters of size 3x3 each.
  model.add(Convolution2D(32, 3, 3, border_mode='valid', input_shape=(3, 100, 100)))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=(2, 2)))
  model.add(Dropout(0.25))

  model.add(Convolution2D(64, 3, 3, border_mode='valid'))
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
      grouped_filenames = []
      grouped_cats = []
      for f in files:
        grouped_filenames.append(root + '/' + f)
        grouped_cats.append(cat)

      filenames.append(grouped_filenames)
      categories.append(grouped_cats)

  # normalize category sizes
  cat_lens = [len(i) for i in categories]
  min_len = min(cat_lens)
  simple_filenames = []
  simple_categories = []
  for i,j in zip(filenames, categories):
    simple_categories += j[:min_len]
    simple_filenames += i[:min_len]

  return np.array(simple_filenames), np.array(simple_categories), len(category_names)

def train(model, num_epoch):
  fnames, categories, category_count = get_filenames_and_categories('images')
  image_loader = ImageLoader(MINI_BATCH_SIZE, fnames, categories, category_count).shuffle()

  datagen = ImageDataGenerator(
      rotation_range=300,
      width_shift_range=0.2,
      height_shift_range=0.2,
      horizontal_flip=True,
      zoom_range=0.5,
      )
  training_set, validation_set = image_loader.split(0.9)

  all_imgs, all_cats = image_loader.get_all()

  for e in range(num_epoch):
    print('Epoch', e)
    batches = 0
    for X_batch, Y_batch in datagen.flow(all_imgs, all_cats, batch_size=10):
      loss = model.train_on_batch(X_batch, Y_batch)
      batches += 1
      if batches >= len(all_imgs) / 10:
        break
      if e % 10 == 0:
        model.save('trained_model')

def main():
  parser = argparse.ArgumentParser('jiiritys piiritys')
  parser.add_argument('--load_model', '-l', default=None)
  parser.add_argument('--classify', '-c', default=None)
  args = parser.parse_args()

  if args.load_model is not None:
    model = load_model(args.load_model)
  else:
    model = build_model(NUM_CATEGORIES)

  if args.classify is None:
    train(model, NUM_EPOCH)
    model.save('trained_model')
  else:
    img = np.array(Image.open(args.classify).convert('RGB').resize((100,100)))
    img = np.moveaxis(img, -1, 0)
    img = img.reshape((1,3,100,100))
    features = model.predict(img)
    print(features)

if __name__ == '__main__':
  main()
