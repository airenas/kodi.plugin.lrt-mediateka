# -*- coding: utf-8 -*-
import sys
import os
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmc
import xbmcaddon
import xbmcplugin

from bs4 import BeautifulSoup
import json
import urllib2

_url = sys.argv[0]
_handle = int(sys.argv[1])

Categories = [{'name': 'Panorama',
               'thumb': 'https://www.lrt.lt/img/2019/07/23/478013-415893-393x221.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/panorama',
               'genre': 'Panorama'},
              {'name': 'Filmai',
               'thumb': 'https://www.lrt.lt/img/2019/05/03/421437-888122-615x345.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/filmai',
               'genre': 'Filmai'},
               {'name': 'Serialai',
               'thumb': 'https://www.lrt.lt/img/2021/05/16/970232-487353-282x158.png',
               'url': 'https://www.lrt.lt/tema/serialai',
               'genre': 'Serialai'},
              {'name': 'Sportas. Orai',
               'thumb': 'https://www.lrt.lt/img/2019/07/23/478391-523744-615x345.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/sportas-orai',
               'genre': 'Sportas'},
              {'name': 'Mediateka',
               'thumb': 'https://www.lrt.lt/img/2019/07/24/478788-929703-615x345.jpg',
               'url': 'https://www.lrt.lt/mediateka',
               'genre': 'Mediateka'},
              {'name': 'Filmai (tema)',
               'thumb': 'https://www.lrt.lt/img/2019/11/02/542178-778716-1287x836.jpg',
               'url': 'https://www.lrt.lt/tema/filmai',
               'genre': 'Filmai'},
              {'name': 'Dokumentiniai filmai (tema)',
               'thumb': 'https://www.lrt.lt/img/2019/11/02/542178-778716-1287x836.jpg',
               'url': 'https://www.lrt.lt/tema/dokumentinis-filmas',
               'genre': 'Filmai'},
              {'name': 'Dokumentiniai filmai',
               'thumb': 'https://www.lrt.lt/img/2019/11/02/542178-778716-1287x836.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/kiti/filmai/dokumentiniai-filmai',
               'genre': 'Filmai'},
              {'name': 'Dviračio žinios',
               'thumb': 'https://www.lrt.lt/img/2019/11/02/542178-778716-1287x836.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/dviracio-zinios',
               'genre': 'Dviračio žinios'},
              {'name': 'Dienos tema',
               'thumb': 'https://www.lrt.lt/img/2020/10/11/739344-314128-393x221.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/dienos-tema',
               'genre': 'Dienos tema'},
              {'name': 'Klauskite daktaro',
               'thumb': 'https://www.lrt.lt/img/2019/10/31/538472-544-1287x836.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/klauskite-daktaro',
               'genre': 'Klauskite daktaro'},
              {'name': 'Beatos virtuvė',
               'thumb': 'https://www.lrt.lt/img/2019/11/01/542088-934580-1287x836.jpg',
               'url': 'https://www.lrt.lt/mediateka/video/beatos-virtuve',
               'genre': 'Beatos virtuvė'}]

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


############################################################################


def extract_image(p_html):
    img = p_html.find('img', attrs={'class': 'media-block__image'})
    if img and img.get('src'):
        return 'https://www.lrt.lt' + img.get('src')
    if img and img.get('data-src'):
        return 'https://www.lrt.lt' + img.get('data-src')
    xbmc.log('No image ', level=xbmc.LOGNOTICE)
    return ''


############################################################################


def extract_genre(p_html):
    m = p_html.find('a', attrs={'class': 'info-block__link'})
    if m:
        return m.get_text()
    return ''


############################################################################


def extract_date(p_html):
    m = p_html.find('span', attrs={'class': 'info-block__text'})
    if m:
        xbmc.log('Date ' + m.get_text().encode('utf-8'), level=xbmc.LOGNOTICE)
        return m.get_text()
    xbmc.log('No date ', level=xbmc.LOGNOTICE)
    return None


############################################################################


def skip(p_html):
    div = p_html.find_parent('div', attrs={'class': 'swipe-list-xs-down'})
    if div:
        return True
    return False


############################################################################


def get_videos(url):
    xbmc.log("Loading " + url, level=xbmc.LOGNOTICE)
    headers = {'Cookie': 'beget=begetok; has_js=1;',
               'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38'}
    req = urllib2.Request(url, None, headers)
    resp = urllib2.urlopen(req)
    html = resp.read()
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all('div', attrs={'class': 'media-block'})
    xbmc.log('Div size ' + str(len(divs)), level=xbmc.LOGNOTICE)
    res = []
    uniqRes = set()
    for d in divs:
        # xbmc.log('Div: ' + str(d), level=xbmc.LOGNOTICE)
        parentDiv = d.find_parent('div')
        m = parentDiv.find('h3', attrs={'class': 'news__title'})
        link = m.find('a')
        ref = link.get('href')
        if (not ref in uniqRes) and (not skip(d)):
            r = {}

            dt = extract_date(parentDiv)
            if dt:
                r["name"] = dt + ' ' + m.get_text()
            else:
                r["name"] = m.get_text()

            r["url"] = ref
            r["genre"] = extract_genre(parentDiv)
            r["thumb"] = extract_image(d)
            res.append(r)
            uniqRes.add(ref)
    return res


############################################################################


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'LRT Mediateka')
    xbmcplugin.setContent(_handle, 'videos')
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    CACHE_PATH = xbmc.translatePath(ADDON.getAddonInfo("Profile"))
    if not os.path.exists(CACHE_PATH):
        os.makedirs(CACHE_PATH)
    xbmc.log("Path {0} cache oath {1}".format(PATH, CACHE_PATH), level=xbmc.LOGNOTICE)
    for c in Categories:
        list_item = xbmcgui.ListItem(label=c['name'])
        list_item.setArt({'thumb': c['thumb'],
                          'icon': c['thumb'],
                          'fanart': c['thumb']})
        list_item.setInfo('video', {'title': c['name'],
                                    'genre': c['genre'],
                                    'mediatype': 'video'})
        url = get_url(action='list', url=c['url'])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


############################################################################
def list_videos(url):
    xbmcplugin.setPluginCategory(_handle, url)
    xbmcplugin.setContent(_handle, 'videos')
    videos = get_videos(url)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        list_item.setArt(
            {'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', url=video['url'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


############################################################################


def get_play_url(url):
    data = json.load(urllib2.urlopen(
        'https://www.lrt.lt/servisai/stream_url/vod/media_info/?url=' + url))
    return data["playlist_item"]["file"]


############################################################################


def play_video(url):
    xbmc.log("Play " + url, level=xbmc.LOGNOTICE)
    play_url = get_play_url(url)
    xbmc.log("Got play URL " + play_url, level=xbmc.LOGNOTICE)
    play_item = xbmcgui.ListItem(path=play_url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


############################################################################


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    xbmc.log("route {0} - {1}".format(params['action'], params['url']), level=xbmc.LOGNOTICE)
    if params:
        if params['action'] == 'list':
            list_videos(params['url'])
        else:
            if params['action'] == 'play':
                play_video(params['url'])
            else:
                raise ValueError(
                    'Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()


############################################################################
if __name__ == '__main__':
    router(sys.argv[2][1:])
