from django.conf import settings
from travels import models

def project_settings(request):
  project_settings = models.Settings.objects.all()[0]
  return { 'project_settings' : project_settings }

def settings_variables(request):
	''' Provides base URLs for use in templates '''

	project_settings = models.Settings.objects.all()[0]

	d = {
    	'APP_NAME': settings.APP_NAME,
    	'PROJECT_DESCRIPTION': project_settings.project_description,
	}

	# Allows settings to define which variables
	# it wants to expose to templates
	if settings.CONTEXT_VARIABLES:
	    for var in settings.CONTEXT_VARIABLES:
	        if hasattr(settings, var):
	            d[var] = getattr(settings, var)

	return d