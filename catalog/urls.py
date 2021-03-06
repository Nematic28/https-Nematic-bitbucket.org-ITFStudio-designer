from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'catalog.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'^designer/$', 'designer.views.index'),
                       # url(r'^designer/(\d+)', 'designer.views.index'),
                       url(r'^designer/view/$', 'designer.views.catalog'),
                       url(r'^designer/view/(\d+)', 'designer.views.catalog'),
                       )
