from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.gis.geos import Point
from travels import models

# Enable admin defined settings
if models.Settings.objects.count() == 0:
    p = Point(0,0)
    s = models.Settings(location=p, project_title = 'UNICEF GIS')
    s.save()

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog'),
)

urlpatterns += patterns('travels.views',
    url(r'^$', 'frontpage', name='frontpage'),
    url(r'^register/$', 'register', name='register'),
)

urlpatterns += patterns('travels.views',
    url(r'^travels.js', 'travels_js', name='travels_js'),
    url(r'^templates.js$', 'templates_js', name='templates_js'),
    url(r'^iphone_welcome.json$', 'iphone_welcome', name='iphone_welcome'),
)

urlpatterns += patterns('locast.i18n.views',
    url(r'^setlang/$', 'set_language', name='set_language'),
)

urlpatterns += patterns('locast.auth.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout')
)

urlpatterns += patterns('',
    url(r'^api/', include('travels.api.urls')),
)
