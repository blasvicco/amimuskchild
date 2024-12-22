'''Custom password validators'''

# General imports
import re

# Lib imports
from django.core.exceptions import ValidationError


class NonAlphanumericPasswordValidator:
	'''Password validator non alphanumeric is required'''

	def validate(self, password, user=None):
		'''validate that at least one non alphanumeric is being use'''
		matches = re.match(r'.*[^a-zA-Z\d\s].*', password)
		if not matches:
			raise ValidationError('NON_ALPHANUMERIC_IS_REQUIRED')

