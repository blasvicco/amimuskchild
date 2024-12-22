'''Is Face validator'''

# General imports
import os

# Lib imports
import cv2
from rest_framework.exceptions import ValidationError

class VIsFace(): # pylint: disable=too-few-public-methods
	'''VFileSize class definition'''
	def __init__(self, error_msg='IMAGE_DOES_NOT_CONTAIN_A_FACE'):
		'''constructor'''
		self.error_msg = error_msg

	def __call__(self, image_path):
		'''validation'''

		# Load the Haar cascade file
		face_cascade = cv2.CascadeClassifier(
			os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
		)

		# Read the image
		gray_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

		# Detect faces
		faces = face_cascade.detectMultiScale(
			gray_image,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30),
		)

		# Check if exactly one face is detected
		if len(faces) == 1:
			# Extract the face coordinates
			(x, y, w, h) = faces[0]
			# Save the cropped face to a new file
			return gray_image[y:y + h, x:x + w]
		elif len(faces) == 0:
			raise ValidationError(self.error_msg)
		raise ValidationError('MULTIPLE_FACES_DETECTED')
