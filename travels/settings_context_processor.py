from travels import models

def project_settings(request):
  project_settings = models.Settings.objects.all()[0]
  return { 'project_settings' : project_settings }
