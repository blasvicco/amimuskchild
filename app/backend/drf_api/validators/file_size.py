'''File mimetype validator'''

# Lib imports
from rest_framework.exceptions import ValidationError

class VFileSize(): # pylint: disable=too-few-public-methods
	'''VFileSize class definition'''
	def __init__(self, size_limit, error_msg='FILE_SIZE_TOO_LARGE'):
		'''constructor'''
		self.error_msg = error_msg
		self.size_limit = size_limit

	def __call__(self, file):
		'''validation'''
		try:
			if file.size < self.size_limit:
				return file
		except Exception: # pylint: disable=broad-except
			pass
		raise ValidationError(self.error_msg)
