import urllib2
# from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from bandnames.names.models import Bands, NewBand, ReportBand


class BandNamesBasePagesTest(TestCase):

    def test_home(self):
        response = self.client.get(reverse('band_list'))
        self.assertTrue(response.status_code == 200)

    def test_about(self):
        response = self.client.get(reverse('about'))
        self.assertTrue(response.status_code == 200)


class BandNamesTest(TestCase):

    def setUp(self):
        self.band1 = Bands.objects.create(
            name='Some Band Name',
            reason='First band reason',
            source='test',
            scrapped_from='test',
        )
        self.band2 = Bands.objects.create(
            name='Another Band Name',
            reason='Second band reason',
            source='test',
            scrapped_from='test',
        )
        self.client = Client()

    def test_band_list(self):
        response = self.client.get(reverse('band_list'))
        self.assertTrue(response.status_code == 200)
        for band in response.context['bands']:
            self.assertIn(band, [self.band1, self.band2])

        self.assertTrue(response.content.count(self.band1.name) == 1)
        self.assertTrue(response.content.count(self.band2.name) == 1)

    def test_band_list_search(self):
        search_url = '{0}?search={1}'.format(reverse('band_list'), self.band1.name)  # NOQA
        response = self.client.get(search_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context['bands']) == 1)
        self.assertTrue(response.context['bands'][0] == self.band1)
        # Once in the search box, once  in 'results for' and once in the list
        self.assertTrue(response.content.count(self.band1.name) == 2)

    def test_band_details(self):
        response = self.client.get(
            reverse('band_info', args=(self.band1.name,))
        )
        self.assertTrue(response.status_code == 200)
        self.assertTrue(self.band1 == response.context['band'])
        self.assertTrue(response.content.count(self.band1.reason) == 1)


class BandNamesReportTest(TestCase):

    def setUp(self):
        self.band1 = Bands.objects.create(
            name='Some Band Name',
            reason='First band reason',
            source='test',
            scrapped_from='test',
        )
        self.band2 = Bands.objects.create(
            name='Another Band Name',
            reason='Second band reason',
            source='test',
            scrapped_from='test',
        )
        self.client = Client()

    def test_band_report_page(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        response = self.client.get(report_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(self.band1 == response.context['band'])

    def test_band_report(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        email = 'test@example.com'
        source = 'http://example.com'
        reason = 'This is a reason'
        name = 'Test'
        data = {
            'reporter_email': [email],
            'source': [source],
            'reason': [reason],
            'reporter_name': [name]
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 302)
        report = ReportBand.objects.get(band=self.band1)
        self.assertTrue(report.reporter_email == email)
        self.assertTrue(report.source == source)
        self.assertTrue(report.reason == reason)
        self.assertTrue(report.reporter_name == name)
        report.delete()

    def test_band_report_no_email(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        source = 'http://example.com'
        reason = 'This is a reason'
        name = 'Test'
        data = {
            'source': [source],
            'reason': [reason],
            'reporter_name': [name]
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 302)
        report = ReportBand.objects.get(band=self.band1)
        self.assertTrue(report.source == source)
        self.assertTrue(report.reason == reason)
        self.assertTrue(report.reporter_name == name)
        report.delete()

    def test_band_report_no_reporter_name(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        email = 'test@example.com'
        source = 'http://example.com'
        reason = 'This is a reason'
        data = {
            'reporter_email': [email],
            'source': [source],
            'reason': [reason],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 302)
        report = ReportBand.objects.get(band=self.band1)
        self.assertTrue(report.reporter_email == email)
        self.assertTrue(report.source == source)
        self.assertTrue(report.reason == reason)
        report.delete()

    def test_band_report_bad_email(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        email = 'test'
        source = 'http://example.com'
        reason = 'This is a reason'
        name = 'Test'
        data = {
            'reporter_email': [email],
            'source': [source],
            'reason': [reason],
            'reporter_name': [name]
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 200)
        report_url = urllib2.unquote(report_url)
        report_url = urllib2.unquote(report_url)
        self.assertTrue(report_url == response.request['PATH_INFO'])
        self.assertIn('reporter_email', response.context['form'].errors)
        with self.assertRaises(ReportBand.DoesNotExist):
            ReportBand.objects.get(band=self.band1)

    def test_band_report_no_reason(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        email = 'test@example.com'
        source = 'http://example.com'
        name = 'Test'
        data = {
            'reporter_email': [email],
            'source': [source],
            'reporter_name': [name]
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 200)
        report_url = urllib2.unquote(report_url)
        self.assertTrue(report_url == response.request['PATH_INFO'])
        self.assertIn('reason', response.context['form'].errors)
        with self.assertRaises(ReportBand.DoesNotExist):
            ReportBand.objects.get(band=self.band1)

    def test_band_report_no_source(self):
        report_url = reverse('band_report', args=(self.band1.name,))
        email = 'test@example.com'
        reason = 'This is a reason'
        name = 'Test'
        data = {
            'reporter_email': [email],
            'reason': [reason],
            'reporter_name': [name]
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 200)
        report_url = urllib2.unquote(report_url)
        self.assertTrue(report_url == response.request['PATH_INFO'])
        self.assertIn('source', response.context['form'].errors)
        with self.assertRaises(ReportBand.DoesNotExist):
            ReportBand.objects.get(band=self.band1)


class NewBandTest(TestCase):

    def test_new_band_page(self):
        report_url = reverse('new_band')
        response = self.client.get(report_url)
        self.assertTrue(response.status_code == 200)

    def test_new_band(self):
        report_url = reverse('new_band')
        name = 'Test'
        reason = 'This is a reason'
        source = 'http://example.com'
        submitter_name = 'Test'
        submitter_email = 'test@example.com'
        data = {
            'name': [name],
            'reason': [reason],
            'source': [source],
            'submitter_name': [submitter_name],
            'submitter_email': [submitter_email],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 302)
        band = NewBand.objects.get(name=name)
        self.assertTrue(band.name == name)
        self.assertTrue(band.reason == reason)
        self.assertTrue(band.source == source)
        self.assertTrue(band.submitter_name == submitter_name)
        self.assertTrue(band.submitter_email == submitter_email)
        band.delete()

    def test_new_band_no_email(self):
        report_url = reverse('new_band')
        name = 'Test'
        reason = 'This is a reason'
        source = 'http://example.com'
        submitter_name = 'Test'
        data = {
            'name': [name],
            'reason': [reason],
            'source': [source],
            'submitter_name': [submitter_name],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 302)
        band = NewBand.objects.get(name=name)
        self.assertTrue(band.name == name)
        self.assertTrue(band.reason == reason)
        self.assertTrue(band.source == source)
        self.assertTrue(band.submitter_name == submitter_name)
        band.delete()

    def test_new_band_no_name(self):
        report_url = reverse('new_band')
        name = 'Test'
        reason = 'This is a reason'
        source = 'http://example.com'
        submitter_email = 'test@example.com'
        data = {
            'name': [name],
            'reason': [reason],
            'source': [source],
            'submitter_email': [submitter_email],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 302)
        band = NewBand.objects.get(name=name)
        self.assertTrue(band.name == name)
        self.assertTrue(band.reason == reason)
        self.assertTrue(band.source == source)
        self.assertTrue(band.submitter_email == submitter_email)
        band.delete()

    def test_new_band_bad_email(self):
        report_url = reverse('new_band')
        name = 'Test'
        reason = 'This is a reason'
        source = 'http://example.com'
        submitter_name = 'Test'
        submitter_email = 'test'
        data = {
            'name': [name],
            'reason': [reason],
            'source': [source],
            'submitter_name': [submitter_name],
            'submitter_email': [submitter_email],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 200)
        report_url = urllib2.unquote(report_url)
        self.assertTrue(report_url == response.request['PATH_INFO'])
        self.assertIn('submitter_email', response.context['form'].errors)
        with self.assertRaises(NewBand.DoesNotExist):
            NewBand.objects.get(name=name)

    def test_new_band_no_reason(self):
        report_url = reverse('new_band')
        name = 'Test'
        source = 'http://example.com'
        submitter_name = 'Test'
        submitter_email = 'test@example.com'
        data = {
            'name': [name],
            'source': [source],
            'submitter_name': [submitter_name],
            'submitter_email': [submitter_email],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 200)
        report_url = urllib2.unquote(report_url)
        self.assertTrue(report_url == response.request['PATH_INFO'])
        self.assertIn('reason', response.context['form'].errors)
        with self.assertRaises(NewBand.DoesNotExist):
            NewBand.objects.get(name=name)

    def test_new_band_no_source(self):
        report_url = reverse('new_band')
        name = 'Test'
        reason = 'This is a reason'
        submitter_name = 'Test'
        submitter_email = 'test@example.com'
        data = {
            'name': [name],
            'reason': [reason],
            'submitter_name': [submitter_name],
            'submitter_email': [submitter_email],
        }
        response = self.client.post(report_url, data=data)
        self.assertTrue(response.status_code == 200)
        report_url = urllib2.unquote(report_url)
        self.assertTrue(report_url == response.request['PATH_INFO'])
        self.assertIn('source', response.context['form'].errors)
        with self.assertRaises(NewBand.DoesNotExist):
            NewBand.objects.get(name=name)


# class BandNamesManagementCommandsTest(TestCase):

#     def test_get_band_names(self):
#         call_command('get_band_names', test=True)
#         url = 'http://en.wikipedia.org/wiki/List_of_band_name_etymologies'
#         self.assertTrue(Bands.objects.filter(scrapped_from=url).count() > 0)
#         url = 'http://en.wikipedia.org/wiki/List_of_bands_named_after_other_bands%27_songs'  # NOQA
#         self.assertTrue(Bands.objects.filter(scrapped_from=url).count() > 0)
#         url = 'http://rateyourmusic.com/list/DanFalco/why_are_they_called_duran_duran__a_guide_to_band_name_etymologies/1/'  # NOQA
#         self.assertTrue(Bands.objects.filter(scrapped_from=url).count() > 0)
#         url = 'http://www.rateyourmusic.com/list/EverythingEvil/bands_named_after_movies_/'  # NOQA
#         self.assertTrue(Bands.objects.filter(scrapped_from=url).count() > 0)
