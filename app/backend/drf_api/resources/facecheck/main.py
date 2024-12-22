'''DRF facecheck viewset'''

# General imports
import os

# Lib imports
import cv2
import numpy as np
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from tensorflow.keras.models import load_model

# App imports
from drf_api.resources.facecheck.permission import PFacecheck
from drf_api.validators import VFileMimeType, VFileSize, VIsFace

# constants
FACE_ACCEPTED_MIMETYPES = ['image/png', 'image/jpeg']
FACE_FILE_SIZE = 500000 # 0.5mb
LABEL = {0:'TRUMP', 1:'MUSK'} # original labels for the model = {0:'OLD', 1:'YOUNG'}
RESIZE_TO = '64x64'

class VSFacecheck(viewsets.ViewSet):
	'''Facecheck View Set'''
	parser_classes = (MultiPartParser,)
	permission_classes = [PFacecheck]
	required_scopes = ['frontend']

	@action(detail=False, methods=['post'])
	def predict(self, request, *args, **kwargs):
		'''Predict if face picture is child of Musk or Trump'''
		file_uploaded = request.FILES.get('face')
		file_uploaded = (VFileSize(
			size_limit=FACE_FILE_SIZE,
			error_msg='NOT_VALID_FACE_FILE_SIZE_TOO_LARGE',
		))(file_uploaded)
		file_path = (VFileMimeType(
			types=FACE_ACCEPTED_MIMETYPES,
			error_msg='NOT_VALID_AVATAR_FILE_TYPE',
		))(file_uploaded.temporary_file_path())
		face_img = (VIsFace())(file_path)
		if face_img is not None:
			# Pre process image
			face_img = VSFacecheck.pre_process_img(face_img)
			# formatting image for input layer
			input_img = np.expand_dims(
				np.repeat(face_img[..., np.newaxis], 3, axis=-1),
				axis=0,
			)
			# Predict
			model = load_model(
				os.path.join(os.sep, 'home', 'app', 'model', 'age_range.keras')
			)
			predictions = model.predict(input_img)
			index = int(np.argmax(predictions, axis=1))
			return Response({
				'confidence': predictions[0][index],
				'prediction': LABEL[index],
			})
		return Response({'face': None})

	@staticmethod
	def pre_process_img(face_img):
		"""pre process img"""
		target_width, target_height = [int(value) for value in RESIZE_TO.split('x')]
		# resize
		target_aspect_ratio = target_width / target_height # Calculate new aspect ratio
		height, width = face_img.shape[:2] # Get original dimensions
		aspect_radio = width / height
		# Check if width needs to be adjusted
		new_width, new_height = target_width, target_height
		if target_aspect_ratio > aspect_radio:
				new_width = int(new_height * aspect_radio)
		else:
				new_height = int(new_width / aspect_radio)

		# Resize the image
		resized_image = cv2.resize(face_img, (new_width, new_height))

		# Create a black canvas with target dimensions
		blank_image = np.zeros((target_height, target_width), np.uint8)
		yoff = round((target_height - new_height) / 2)
		xoff = round((target_width - new_width) / 2)
		new_image = blank_image.copy()
		new_image[yoff:yoff + new_height, xoff:xoff + new_width] = resized_image

		# save new image
		new_image = cv2.fastNlMeansDenoising(new_image)
		new_image = cv2.equalizeHist(new_image)
		return new_image
