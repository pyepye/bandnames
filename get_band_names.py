# -*- coding: utf-8 -*-
import re
import urllib2

from bs4 import BeautifulSoup

artists = []


def get_all_artists():
    get_band_rateyourmusic()
    get_band_wiki()
    get_band_wiki_songs()
    print_artists()


def get_band_wiki():
    url = 'http://en.wikipedia.org/wiki/List_of_band_name_etymologies'
    print 'URL: {}'.format(url)
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    context = urllib2.urlopen(req)
    html = context.read()
    soup = BeautifulSoup(html)
    section = soup.find(id="mw-content-text")
    lis = section.find_all('li')
    for li in lis:
        print_li = False
        try:
            if li.parent.parent.attrs['id'] == 'mw-content-text':
                print_li = True
                # print li.parent.prettify().encode('utf-8')
        except (AttributeError, KeyError):
            pass

        if print_li:
            ignore = ['See also', 'References', 'Bibliography']
            if li.find_previous('h2').find_next('span').string not in ignore:
                # import pdb; pdb.set_trace()
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
                    # print "{} - {}".format(artist_name, artist_desc)
                    artist = {'name': artist_name,
                              'description': artist_desc,
                              'source': ref_url,
                              'scrapped': url}
                    artists.append(artist)
                    # print "{} - {}".format(artist_name, ref_url)


def get_band_wiki_songs():
    url = 'http://en.wikipedia.org/wiki/List_of_bands_named_after_other_bands%27_songs'
    print 'URL: {}'.format(url)
    req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
    context = urllib2.urlopen(req)
    html = context.read()
    soup = BeautifulSoup(html)
    section = soup.find(id="mw-content-text")
    lis = section.find_all('li')
    for li in lis:

        print_li = False
        try:
            if li.parent.parent.attrs['id'] == 'mw-content-text':
                print_li = True
                # print li.parent.prettify().encode('utf-8')
        except (AttributeError, KeyError):
            pass
        if print_li:
            ignore = ['Approximations and partial matches', 'Exact matches']
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
                # print "{} - {}".format(artist_name, artist_desc)
                artist = {'name': artist_name,
                          'description': artist_desc,
                          'source': ref_url,
                          'scrapped_from': url}
                artists.append(artist)


def get_band_rateyourmusic():
    artist_rows = []
    grabbed_artists = 0
    for num in range(1, 11):
        url = 'http://rateyourmusic.com/list/DanFalco/why_are_they_called_duran_duran__a_guide_to_band_name_etymologies/{}/'.format(num)
        print 'URL: {}'.format(url)
        req = urllib2.Request(url, headers={'User-Agent': "Magic Browser"})
        context = urllib2.urlopen(req)
        html = context.read()

        table = html.split('<table id="user_list">')[1]
        table = table.split('</table>')[0]
        artist_rows = table.split('</tr>')[:-1]
        grabbed_artists += len(artist_rows)

        for artist_html in artist_rows:
            artist_info = artist_html.split('list_artist">')[1]
            artist_name, artist_desc = artist_info.split('</a></b><br><br>')
            artist_desc = fix_html_codes(artist_desc)
            artist = {'name': artist_name,
                      'description': artist_desc,
                      'source': url,
                      'scrapped': url}
            artists.append(artist)


def print_artists():
    print 'ARTIST LENGTH: {}'.format(len(artists))
    artists_sorted = sorted(artists, key=lambda a: a['name'])
    desc_length = []
    for artist in artists_sorted:
        desc_length.append(len(artist['description']))
        print '{} - {}'.format(artist['name'], artist['source'])
    print max(desc_length)


def get_wiki_ref_from_achor(soup, anchor):
    if anchor.attrs['href'].startswith('#cite_note'):
        ref_li = soup.find(id=anchor.attrs['href'][1:])
        for anc in ref_li.find_all('a'):
            if 'class' in anc.attrs and 'external' in anc.attrs['class']:
                return anc.attrs['href']
    else:
        return False

def fix_html_codes(a_string):
    a_string = a_string.replace('ÔÇö', '-'
                      ).replace('&#34;', '"'
                      ).replace('&#39;', '\''
                      ).replace('&#34;', '"'
                      ).replace('<td>', ''
                      ).replace('</td>', ''
                      ).replace('<em>', ''
                      ).replace('<br />', ''
                      ).replace('</em>', '')
    match = '/[^<]*(<a href="([^"]+)">([^<]+)<\/a>)/g'
    a_string = re.sub(match, '', a_string)
    return a_string


if __name__ == '__main__':
    get_all_artists()
