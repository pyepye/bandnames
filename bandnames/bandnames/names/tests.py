from django.test import TestCase
from bandnames.names.models import Bands


class BandNamesTest(TestCase):

    def setUp(self):
        Bands.objects.create(
            name='test',
            reason='test',
            source='test',
            scrapped_from='test',
        )

    def test_band_name(self):
        name = Bands.objects.get(name="test")
        self.assertEqual(name.name, 'test')
