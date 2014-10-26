from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from bandnames.names.views import BandList, BandDetail

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^list/$', BandList.as_view(), name='band_list'),
    url(r'^band/(?P<band_id>\d+)/$', BandDetail.as_view(), name='bandinfo'),
    # Examples:
    # url(r'^$', 'bandnames.views.home', name='home'),
    # url(r'^bandnames/', include('bandnames.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
if not settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )
