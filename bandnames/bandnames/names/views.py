import logging

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from bandnames.names.models import Bands as Band
from bandnames.names.forms import NewBandForm, ReportBandForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


class BandList(TemplateView):
    template_name = "band_list.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.GET.get('search'):
            band_list = Band.objects.filter(
                name__contains=request.GET['search']
            ).extra(
                select={'lower_name': 'lower(name)'}
            ).order_by('lower_name')
            context['search_term'] = request.GET['search']
        else:
            band_list = Band.objects.all().extra(
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
        context['band'] = Band.objects.get(name=context.get('band_name'))
        return context


class BandReport(TemplateView):
    template_name = "band_report.html"

    def get_context_data(self, **context):
        context['band'] = Band.objects.get(name=context.get('band_name'))
        context['form'] = ReportBandForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = ReportBandForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.band = context['band']
            report.save()
            band_url = reverse_lazy(
                'band_info', kwargs={'band_name': context['band'].name}
            )
            url = "{}?reported=True".format(band_url)
            return HttpResponseRedirect(url)

        context['form'] = ReportBandForm(request.POST)
        return self.render_to_response(context)


class NewBand(FormView):
    template_name = 'new_band.html'
    form_class = NewBandForm
    success_url = reverse_lazy('band_list')

    def form_valid(self, form):
        form.save()
        return super(NewBand, self).form_valid(form)


class NewBandSuccess(TemplateView):
    template_name = "new_band_success.html"
