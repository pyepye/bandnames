from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from bandnames.names.views import (
    BandList, BandDetail, BandReport, NewBand, NewBandSuccess
)

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='front.html'), name='home'),
    url(r'^bands/$', BandList.as_view(), name='band_list'),
    url(r'^band/(?P<band_name>.*)/$', BandDetail.as_view(), name='band_info'),
    url(r'^band/(?P<band_name>.*)/report/$', BandReport.as_view(), name='band_report'),  # NOQA
    url(r'^newband/$', NewBand.as_view(), name='new_band'),
    url(r'^newband/success/$', NewBandSuccess.as_view(), name='new_band_success'),  # NOQA
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),  # NOQA
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
if not settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),  # NOQA
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),  # NOQA
    )
