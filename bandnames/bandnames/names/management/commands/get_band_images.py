# -*- coding: utf-8 -*-
import logging
import pylast
import urllib
from os.path import join, exists

from django.conf import settings
from django.core.management.base import NoArgsCommand

from bandnames.names.models import Bands

logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        for band in Bands.objects.all():
            band.image = lastfm_band_image(band)
            band.save()
            print "Got image for {}".format(band)


def lastfm_band_image(band):
    password_hash = pylast.md5(settings.LASTFM_PASSWORD)
    lastfm = pylast.LastFMNetwork(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_API_SECRET,
        username=settings.LASTFM_USERNAME,
        password_hash=password_hash,
    )

    try:
        image_url = lastfm.get_artist(band.name).get_cover_image()
        friendly_name = "".join(
            [c for c in band.name if c.isalpha() or c.isdigit() or c == ' ']
        ).rstrip()
        image_name = "img/{}_{}.{}".format(
            band.id,
            friendly_name.encode('ascii', 'ignore'),
            image_url.split('.')[-1:][0],
        )
    except (pylast.WSError, AttributeError):
        image_location = join(settings.MEDIA_URL, "img/missing.png")
    else:
        full_location = join(settings.MEDIA_ROOT, image_name)
        local_image, __ = urllib.urlretrieve(image_url, full_location)
        image_location = join(settings.MEDIA_URL, image_name)
        if not exists(local_image):
            image_location = join(settings.MEDIA_URL, "img/missing.png")

    return image_location
