from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from bandnames.names.views import (
    BandList, BandDetail, BandReport, NewBand, NewBandSuccess
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='front.html')),
    url(r'^bands/$', BandList.as_view(), name='band_list'),
    url(r'^band/(?P<band_id>\d+)/$', BandDetail.as_view(), name='band_info'),

    url(r'^band/(?P<band_id>\d+)/report/$', BandReport.as_view(), name='band_report'),

    url(r'^newband/$', NewBand.as_view(), name='new_band'),
    url(r'^newband/success/$', NewBandSuccess.as_view(), name='new_band_success'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    # Examples:
    # url(r'^$', 'bandnames.views.home', name='home'),
    # url(r'^bandnames/', include('bandnames.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

# Uncomment the next line to serve media files in dev.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
if not settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
