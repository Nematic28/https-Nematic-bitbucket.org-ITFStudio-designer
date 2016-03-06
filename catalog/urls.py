from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'designer.views.catalog', name='view'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^designer/$', 'designer.views.index'),
                       # url(r'^designer/(\d+)', 'designer.views.index'),
                       url(r'^designer/view/(\d+)$', 'designer.views.catalog', name='view'),
                       url(r'^designer/view/$', 'designer.views.catalog', name='main'),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                         + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)