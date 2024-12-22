#!/usr/bin/python
"""Test model"""

# General imports
import os

# Lib imports
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Constants
LABEL = {0:'OLD', 1:'YOUNG'}
RESIZE_TO = '64x64'
WORKING_DIR = '/home/app/model'

def extract_single_face(image_path, output_path):
  # Load the Haar cascade file
  face_cascade = cv2.CascadeClassifier(
    os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
  )

  # Read the image
  image = cv2.imread(image_path)
  gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

  # Detect faces
  faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

  # Check if exactly one face is detected
  if len(faces) == 1:
    # Extract the face coordinates
    (x, y, w, h) = faces[0]
    # Save the cropped face to a new file
    cv2.imwrite(output_path, image[y:y + h, x:x + w])
  elif len(faces) == 0:
    raise Exception('No faces detected.')
  else:
    raise Exception(f'Multiple faces detected: {len(faces)}.')
  return False

def pre_process_img(image_path):
  """pre process img"""
  target_width, target_height = [int(value) for value in RESIZE_TO.split('x')]
  image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  # resize
  target_aspect_ratio = target_width / target_height # Calculate new aspect ratio
  height, width = image.shape[:2] # Get original dimensions
  aspect_radio = width / height
  # Check if width needs to be adjusted
  new_width, new_height = target_width, target_height
  if target_aspect_ratio > aspect_radio:
      new_width = int(new_height * aspect_radio)
  else:
      new_height = int(new_width / aspect_radio)

  # Resize the image
  resized_image = cv2.resize(image, (new_width, new_height))

  # Create a black canvas with target dimensions
  blank_image = np.zeros((target_height, target_width), np.uint8)
  yoff = round((target_height - new_height) / 2)
  xoff = round((target_width - new_width) / 2)
  new_image = blank_image.copy()
  new_image[yoff:yoff + new_height, xoff:xoff + new_width] = resized_image

  # save new image
  new_image = cv2.fastNlMeansDenoising(cv2.UMat(new_image))
  new_image = cv2.equalizeHist(cv2.UMat(new_image))
  cv2.imwrite('tmp.jpg', new_image)

def load_image(image_path):
  """load and parse image for testing model"""
  grayscale_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
  image = np.repeat(grayscale_image[..., np.newaxis], 3, axis=-1)
  if image is None:
    raise Exception(f'INVALID IMAGE: {image_path}')
  return np.expand_dims(image, axis=0)

def main():
  """main function"""
  # Load model
  model = load_model(os.path.join(WORKING_DIR, 'age_range.keras'))

  # Set img paths
  img_org = os.path.join(WORKING_DIR, 'face_small.png')
  img_tmp = os.path.join(WORKING_DIR, 'tmp.jpg')

  # Validate and extract face
  extract_single_face(img_org, img_tmp)

  # Pre process image
  pre_process_img(img_tmp)

  # Load image
  image = load_image(img_tmp)

  # Predict
  predictions = model.predict(image)
  index = int(np.argmax(predictions, axis=1))
  print(f'Prediction: {LABEL[index]}.')
  print(f'Confidence: {predictions[0][index]}.')


if __name__ == '__main__':
  main()
