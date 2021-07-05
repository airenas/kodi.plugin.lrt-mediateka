# -*- coding: utf-8 -*-
import io
import json
import os
import sys
import urllib2
from urllib import urlencode
from urlparse import parse_qsl

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from bs4 import BeautifulSoup

import categories
import extractor

_url = sys.argv[0]
_handle = int(sys.argv[1])


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def extract_date(p_html):
    m = p_html.find('span', attrs={'class': 'info-block__text'})
    if m:
        xbmc.log('Date ' + m.get_text().encode('utf-8'), level=xbmc.LOGNOTICE)
        return m.get_text()
    xbmc.log('No date ', level=xbmc.LOGNOTICE)
    return None


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
        if (not ref in uniqRes) and (not extractor.skip(d)):
            r = {}

            dt = extract_date(parentDiv)
            if dt:
                r["name"] = dt + ' ' + m.get_text()
            else:
                r["name"] = m.get_text()

            r["url"] = ref
            r["genre"] = extractor.extract_genre(parentDiv)
            r["thumb"] = extractor.extract_image(d)
            res.append(r)
            uniqRes.add(ref)
    return res


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'LRT Mediateka')
    xbmcplugin.setContent(_handle, 'videos')
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    a_path = xbmc.translatePath(ADDON.getAddonInfo("Profile"))
    if not os.path.exists(a_path):
        os.makedirs(a_path)
    xbmc.log("Path {0} cache oath {1}".format(PATH, a_path), level=xbmc.LOGNOTICE)
    # video = ADDON.getSetting("video")
    # xbmc.log("Video {0}".format(video), level=xbmc.LOGNOTICE)
    # videos = video.split(",")
    # for v in videos:
    #     v = v.strip()
    #     xbmc.log("Video {0}".format(v), level=xbmc.LOGNOTICE)
    #     vd = get_video_data(v, a_path)
    #     list_item = xbmcgui.ListItem(label=vd['name'])
    #     list_item.setArt({'thumb': vd['thumb'],
    #                       'icon': vd['thumb'],
    #                       'fanart': vd['thumb']})
    #     list_item.setInfo('video', {'title': vd['name'],
    #                                 'genre': vd['genre'],
    #                                 'mediatype': 'video'})
    #     url = get_url(action='list', url=vd['url'])
    #     xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    for c in categories.get(ADDON):
        xbmc.log("Video {0}".format(c.id), level=xbmc.LOGNOTICE)
        vd = get_video_data(c.url, c.name, c.id, a_path)

        list_item = xbmcgui.ListItem(label=vd['name'])
        list_item.setArt({'thumb': vd['thumb'],
                          'icon': vd['thumb'],
                          'fanart': vd['thumb']})
        list_item.setInfo('video', {'title': vd['name'],
                                    'genre': vd['genre'],
                                    'mediatype': 'video'})
        url = get_url(action='list', url=vd['url'])
        xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)


def get_video_data(url, name, cid, path):
    f = os.path.join(path, cid + ".json")
    if not os.path.exists(f):
        xbmc.log('No file : ' + f, level=xbmc.LOGNOTICE)
        data = extractor.load_data(url, name)
        if data is None:
            xbmc.log("Can't load " + url, level=xbmc.LOGERROR)
            return
        with io.open(f, 'w', encoding='utf-8') as fo:
            fo.write(json.dumps(data, ensure_ascii=False))
    else:
        xbmc.log('File found: ' + f, level=xbmc.LOGNOTICE)
        with io.open(f, 'r', encoding='utf-8') as fo:
            data = json.load(fo)
    return data


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


def get_play_url(url):
    data = json.load(urllib2.urlopen(
        'https://www.lrt.lt/servisai/stream_url/vod/media_info/?url=' + url))
    return data["playlist_item"]["file"]


def play_video(url):
    xbmc.log("Play " + url, level=xbmc.LOGNOTICE)
    play_url = get_play_url(url)
    xbmc.log("Got play URL " + play_url, level=xbmc.LOGNOTICE)
    play_item = xbmcgui.ListItem(path=play_url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        xbmc.log("route {0} - {1}".format(params['action'], params['url']), level=xbmc.LOGNOTICE)
        if params['action'] == 'list':
            list_videos(params['url'])
        else:
            if params['action'] == 'play':
                play_video(params['url'])
            else:
                raise ValueError(
                    'Invalid paramstring: {0}!'.format(paramstring))
    else:
        xbmc.log("no params", level=xbmc.LOGNOTICE)
        list_categories()


############################################################################
if __name__ == '__main__':
    router(sys.argv[2][1:])
