'''File mimetype validator'''

# Lib imports
import mimetypes
from rest_framework.exceptions import ValidationError

class VFileMimeType(): # pylint: disable=too-few-public-methods
	''' VFileMimeType validator'''
	def __init__(self, types, error_msg='NOT_VALID_FILE_TYPE'):
		'''constructor'''
		self.error_msg = error_msg
		self.types = types

	def __call__(self, file_path):
		'''validation'''
		try:
			mimetype, _ = mimetypes.guess_type(file_path)
			if mimetype in self.types:
				return file_path
		except Exception: # pylint: disable=broad-except
			pass
		raise ValidationError(self.error_msg)
