# -*- coding: utf-8 -*-
import re
import logging
import requests
import pylast
import urllib
from os.path import join, exists

from bs4 import BeautifulSoup

from django.conf import settings
from django.core.management.base import NoArgsCommand

from bandnames.names.models import Bands

logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        get_band_wiki()
        get_band_wiki_songs()
        get_band_rateyourmusic()


def get_band_wiki():
    url = 'http://en.wikipedia.org/wiki/List_of_band_name_etymologies'
    logger.info(url)
    req = requests.get(url, headers={'User-Agent': "Magic Browser"})
    if req.status_code == 200:
        soup = BeautifulSoup(req.content)
        section = soup.find(id="mw-content-text")
        lis = section.find_all('li')
        for li in lis:
            print_li = False
            try:
                if li.parent.parent.attrs['id'] == 'mw-content-text':
                    print_li = True
            except (AttributeError, KeyError):
                pass

            if print_li:
                ignore = ['See also', 'References', 'Bibliography']
                if (
                    li.find_previous('h2').find_next('span').string not in
                    ignore
                ):
                    anchors = li.find_all('a')
                    last_anchor = li.find_all('a')[len(anchors)-1]
                    ref_url = get_wiki_ref_from_achor(soup, last_anchor)
                    if not ref_url:
                        ref_url = url
                    artist_info = li.get_text().split(u'ÔÇö', 1)
                    artist_info = artist_info[0].split(u'\u2014')
                    if len(artist_info) == 1:
                        artist_info = artist_info[0].split(u'-', 1)

                    try:
                        artist_name = artist_info[0].strip().encode('utf-8')
                        artist_desc = artist_info[1].strip().encode('utf-8')
                        artist_desc = artist_desc.replace(
                            last_anchor.get_text().encode('utf-8'), ''
                        )
                    except IndexError:
                        pass
                    else:
                        add_band(artist_name, artist_desc, ref_url, url)


def get_band_wiki_songs():
    url = ('http://en.wikipedia.org/wiki/List_of_bands_named_after_other_'
           'bands%27_songs')
    logger.info(url)
    req = requests.get(url, headers={'User-Agent': "Magic Browser"})
    if req.status_code == 200:
        soup = BeautifulSoup(req.content)
        section = soup.find(id="mw-content-text")
        lis = section.find_all('li')
        for li in lis:

            print_li = False
            try:
                if li.parent.parent.attrs['id'] == 'mw-content-text':
                    print_li = True
            except (AttributeError, KeyError):
                pass
            if print_li:
                ignore = [
                    'Approximations and partial matches',
                    'Exact matches'
                ]
                if li.find_previous('h2').find_next('span').string in ignore:
                    anchors = li.find_all('a')
                    last_anchor = li.find_all('a')[len(anchors)-1]
                    ref_url = get_wiki_ref_from_achor(soup, last_anchor)
                    if not ref_url:
                        ref_url = url
                    artist_info = li.get_text().split(u' after', 1)
                    if len(artist_info) < 2:
                        artist_info = li.get_text().split(u' from', 1)
                    if len(artist_info) < 2:
                        artist_info = li.get_text().split(u',', 1)
                    artist_name = artist_info[0].strip().encode('utf-8')
                    if artist_name[-1:] == ',':
                        artist_name = artist_name[:-1]
                    artist_desc = "Named after {}".format(
                        artist_info[1].strip().encode('utf-8')
                    )
                    add_band(artist_name, artist_desc, ref_url, url)


def get_band_rateyourmusic():
    artist_rows = []
    grabbed_artists = 0
    for num in range(1, 11):
        url = ('http://rateyourmusic.com/list/DanFalco/why_are_they_called_dur'
               'an_duran__a_guide_to_band_name_etymologies/{}/'.format(num))
        logger.info(url)
        req = requests.get(url, headers={'User-Agent': "Magic Browser"})
        if req.status_code == 200:
            html = req.content

            table = html.split('<table id="user_list">')[1]
            table = table.split('</table>')[0]
            artist_rows = table.split('</tr>')[:-1]
            grabbed_artists += len(artist_rows)

            for artist_html in artist_rows:
                artist_info = artist_html.split('list_artist">')[1]
                artist_name, artist_desc = artist_info.split(
                    '</a></b><br><br>'
                )
                artist_desc = fix_html_codes(artist_desc)
                add_band(artist_name, artist_desc, url, url)


def add_band(name, reason, source, scrapped):
    try:
        band = Bands.objects.get(name=name)
        logger.info(
            'Band already exits with name {}'.format(name, scrapped)
        )
    except Bands.DoesNotExist:
        image_location = lastfm_band_image(name)
        Bands.objects.create(
            name=name,
            image=image_location,
            reason=reason,
            source=source,
            scrapped_from=scrapped,
        )
        print '{} - {}'.format(name, scrapped)
        logger.info('Band added: {} - {}'.format(name, source))
    else:
        if band.reason != reason:
            logger.info(
                'New descrition for {} - {}'.format(
                    name, reason
                )
            )


def get_wiki_ref_from_achor(soup, anchor):
    if anchor.attrs['href'].startswith('#cite_note'):
        ref_li = soup.find(id=anchor.attrs['href'][1:])
        for anc in ref_li.find_all('a'):
            if 'class' in anc.attrs and 'external' in anc.attrs['class']:
                return anc.attrs['href']
    else:
        return False


def fix_html_codes(a_string):
    a_string = a_string.replace(
        'ÔÇö', '-').replace(
        '&#34;', '"').replace(
        '&#39;', '\'').replace(
        '&#34;', '"').replace(
        '<td>', '').replace(
        '</td>', '').replace(
        '<em>', '').replace(
        '<br />', '').replace(
        '</em>', '')

    match = '/[^<]*(<a href="([^"]+)">([^<]+)<\/a>)/g'
    a_string = re.sub(match, '', a_string)
    return a_string


def lastfm_band_image(name):
    password_hash = pylast.md5(settings.LASTFM_PASSWORD)
    lastfm = pylast.LastFMNetwork(
        api_key=settings.LASTFM_API_KEY,
        api_secret=settings.LASTFM_API_SECRET,
        username=settings.LASTFM_USERNAME,
        password_hash=password_hash,
    )

    try:
        image_url = lastfm.get_artist(name).get_cover_image()
    except pylast.WSError:
        image_location = join(settings.MEDIA_URL, "img/missing.png")
    else:
        friendly_name = "".join(
            [c for c in name if c.isalpha() or c.isdigit() or c == ' ']
        ).rstrip()
        image_name = "img/{}.{}".format(
            friendly_name, image_url.split('.')[-1:][0]
        )
        full_location = join(settings.MEDIA_ROOT, image_name)
        local_image, __ = urllib.urlretrieve(image_url, full_location)
        image_location = join(settings.MEDIA_URL, image_name)
        if not exists(local_image):
            image_location = join(settings.MEDIA_URL, "img/missing.png")

    return image_location
