'''Facecheck permission'''

# Lib imports
from oauth2_provider.contrib.rest_framework import IsAuthenticatedOrTokenHasScope
from rest_framework.permissions import BasePermission as DRFBasePermission

class PFacecheck(DRFBasePermission):
	'''Facecheck permission'''

	def has_permission(self, request, view):
		'''request view permission check'''
		return IsAuthenticatedOrTokenHasScope.has_permission(self, request, view) \
			and request.method in ['POST']
