# -*- coding: utf-8 -*-
import io
import json
import os
import sys
import time
import urllib2
from urllib import urlencode
from urlparse import parse_qsl

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import categories
import extractor

_url = sys.argv[0]
_handle = int(sys.argv[1])


def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_categories():
    xbmcplugin.setPluginCategory(_handle, 'LRT Mediateka')
    xbmcplugin.setContent(_handle, 'videos')
    ADDON = xbmcaddon.Addon()
    PATH = sys.argv[0]
    a_path = xbmc.translatePath(ADDON.getAddonInfo("Profile"))
    a_path = os.path.join(a_path, ".cache")
    if not os.path.exists(a_path):
        os.makedirs(a_path)
    xbmc.log("Path {0} cache path {1}".format(PATH, a_path), level=xbmc.LOGNOTICE)

    drop_old_files(a_path)

    for c in categories.get(ADDON):
        xbmc.log("Video {0}".format(c.id), level=xbmc.LOGNOTICE)
        try:
            vd = get_video_data(c.url, c.name, c.id, a_path)
        except Exception as err:
            display_error(ADDON, "Can't load " + c.url, err)
            continue

        if vd is None:
            display_error(ADDON, "Can't load " + c.url)
            continue

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


def display_error(addon, message='n/a', err=None):
    line1 = addon.getLocalizedString(30250)
    line2 = addon.getLocalizedString(30251)
    xbmc.log(message, level=xbmc.LOGERROR)
    if err is not None:
        xbmc.log(repr(err), level=xbmc.LOGERROR)
    xbmcgui.Dialog().notification(line1, line2 + message, xbmcgui.NOTIFICATION_ERROR, 5000)


def drop_old_files(path):
    now = time.time()
    for filename in os.listdir(path):
        _, ext = os.path.splitext(filename)
        ff = os.path.join(path, filename)
        if ext == ".json" and os.path.isfile(ff):
            if os.path.getmtime(ff) < now - 10 * 86400 or os.path.getsize(ff) == 0:
                xbmc.log("Drop file {0}".format(ff), level=xbmc.LOGNOTICE)
                os.remove(ff)


def get_video_data(url, name, cid, path):
    f = os.path.join(path, cid + ".json")
    if not os.path.exists(f):
        xbmc.log('No file : ' + f, level=xbmc.LOGNOTICE)
        xbmc.log('Load data from : ' + url, level=xbmc.LOGNOTICE)
        data = extractor.load_data(url, name)
        if data is None:
            xbmc.log("Can't load " + url, level=xbmc.LOGERROR)
            return None
        j_str = json.dumps(data, ensure_ascii=False, encoding='utf8')
        xbmc.log("Json : '{0}'".format(j_str), level=xbmc.LOGNOTICE)
        with io.open(f, 'w', encoding='utf-8') as fo:
            fo.write(unicode(j_str))
    else:
        xbmc.log('File found: ' + f, level=xbmc.LOGNOTICE)
        with io.open(f, 'r', encoding='utf-8') as fo:
            data = json.load(fo)
    return data


def list_videos(url):
    xbmcplugin.setPluginCategory(_handle, url)
    xbmcplugin.setContent(_handle, 'videos')
    videos = extractor.get_videos(url)
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
