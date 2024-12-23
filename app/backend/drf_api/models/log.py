'''Log model'''

# Libs imports
from django.db import models

# App imports
from drf_api.models import MBase

class MLog(MBase): # pylint: disable=too-few-public-methods
	'''Log model'''

	action = models.CharField(
		blank=False,
		db_index=True,
		max_length=40,
		null=False,
	)

	actor = models.CharField(
		blank=False,
		db_index=True,
		max_length=255,
		null=False,
	)

	created_on = models.DateTimeField(auto_now_add=True)

	payload = models.TextField(default='')

	def __str__(self):
		'''To string method'''
		return f'{self.id}:{self.action}:{self.actor}'

	@staticmethod
	def get_headers(request):
		'''get the header from the request'''
		fields = [
			'HTTP_USER_AGENT',
			'CONTENT_TYPE',
			'PATH_INFO',
			'QUERY_STRING',
			'REMOTE_ADDR',
			'REMOTE_HOST',
			'REQUEST_METHOD',
		]
		return {field: request.META.get(field) for field in fields}

	class Meta:
		app_label = 'drf_api'
		ordering = ['-created_on']
		abstract = False
