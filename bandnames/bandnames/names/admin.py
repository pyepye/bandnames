from django.contrib import admin
from bandnames.names.models import Bands, NewBand, ReportBand

admin.site.register([Bands, NewBand, ReportBand])
