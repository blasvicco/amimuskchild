'''Base model'''

# General imports
from django.db import models

class MBase(models.Model):
	'''Base model'''
	class Meta:
		abstract = True
