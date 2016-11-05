from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase


from bandnames.names.models import Bands


class BandNamesBasePagesTest(TestCase):

    def test_home(self):
        response = self.client.get(reverse('home'))
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

        # Check HTML
        self.assertTrue(response.content.count('<div class="band-wrap">') == 2)
        self.assertTrue(response.content.count(self.band1.name) == 1)
        self.assertTrue(response.content.count(self.band2.name) == 1)

    def test_band_list_search(self):
        search_url = '{0}?search={1}'.format(reverse('band_list'), self.band1.name)  # NOQA
        response = self.client.get(search_url)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(len(response.context['bands']) == 1)
        self.assertTrue(response.context['bands'][0] == self.band1)

        # Check HTML
        self.assertTrue(response.content.count('<div class="band-wrap">') == 1)
        self.assertTrue(response.content.count('Search results for the search') == 1)  # NOQA
        # Once in the search box, once  in 'results for' and once in the list
        self.assertTrue(response.content.count(self.band1.name) == 3)

    def test_band_details(self):
        response = self.client.get(reverse('band_info', args=(self.band1.id,)))
        self.assertTrue(response.status_code == 200)
        self.assertTrue(self.band1 == response.context['band'])

        # Check HTML
        h2 = '<h2>{0}</h2>'.format(self.band1.name)
        self.assertTrue(response.content.count(h2) == 1)
        self.assertTrue(response.content.count(self.band1.reason) == 1)


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
