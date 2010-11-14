from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from rb.views import home
from rb.views import user_page
urlpatterns = patterns('',
					(r'^site_media/(?P<path>.*)$', 
						'django.views.static.serve', 
						{'document_root': 'media'}),
						(r'^$',home),
						(r'getinfo',user_page)
    # Example:
    # (r'^pylist/', include('pylist.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
