# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup


def extract_image(p_html):
    img = p_html.find('img', attrs={'class': 'media-block__image'})
    if img and img.get('data-src'):
        return 'https://www.lrt.lt' + img.get('data-src')
    if img and img.get('src'):
        return 'https://www.lrt.lt' + img.get('src')
    return ''


def extract_genre(p_html):
    m = p_html.find('a', attrs={'class': 'info-block__link'})
    if m:
        return m.get_text()
    return ''


def load_data(url, name):
    headers = {'Cookie': 'beget=begetok; has_js=1;',
               'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38'}
    req = urllib2.Request(url, None, headers)
    resp = urllib2.urlopen(req)
    html = resp.read()
    soup = BeautifulSoup(html, "html.parser")
    divs = soup.find_all('div', attrs={'class': 'media-block'})
    for d in divs:
        parentDiv = d.find_parent('div')
        if not skip(d):
            r = {}
            r["name"] = name.title()
            r["url"] = url
            r["genre"] = extract_genre(parentDiv)
            r["thumb"] = extract_image(parentDiv)
            return r
    return None


def skip(p_html):
    div = p_html.find_parent('div', attrs={'class': 'swipe-list-xs-down'})
    if div:
        return True
    return False