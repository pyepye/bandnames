import logging

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView

from bandnames.names.models import Bands

# Get an instance of a logger
logger = logging.getLogger(__name__)


class BandList(TemplateView):
    template_name = "band_list.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('search'):
            band_list = Bands.objects.filter(
                name__contains=request.GET['search']
            ).extra(
                select={'lower_name': 'lower(name)'}
            ).order_by('lower_name')
            context['search_term'] = request.GET['search']
        else:
            band_list = Bands.objects.all().extra(
                select={'lower_name': 'lower(name)'}
            ).order_by('lower_name')

        paginator = Paginator(band_list, 26)

        page = request.GET.get('page')
        try:
            context['bands'] = paginator.page(page)
        except PageNotAnInteger:
            context['bands'] = paginator.page(1)
        except EmptyPage:
            context['bands'] = paginator.page(paginator.num_pages)

        return self.render_to_response(context)


class BandDetail(TemplateView):
    template_name = "band_detail.html"

    def get_context_data(self, **context):
        context['band'] = Bands.objects.get(pk=context.get('band_id'))
        return context
