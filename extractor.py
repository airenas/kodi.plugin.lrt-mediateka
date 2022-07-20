# -*- coding: utf-8 -*-
import json
import logging
import urllib.request

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
    req = urllib.request.Request(url, None, headers)
    resp = urllib.request.urlopen(req)
    html = resp.read()
    soup = BeautifulSoup(html, "html.parser")
    divs = get_video_divs(soup)

    for d in divs:
        parent_div = d.find_parent('div')
        if not skip(d):
            return {"name": name.title(),
                    "url": url,
                    "genre": extract_genre(parent_div),
                    "thumb": extract_image(parent_div)}
    return None


def skip(p_html):
    div = p_html.find_parent('div', attrs={'class': 'swipe-list-xs-down'})
    if div:
        return True
    return False


def skip_news(p_html):
    if p_html.has_attr('class'):
        for c in p_html['class']:
            if c == u'news-list--feed-horizontal':
                return True
    return False


def is_media(p_html):
    play_span = p_html.find_all('span', attrs={'class': 'play-button'})
    return len(play_span) > 0


def get_video_divs(soup):
    div_p = soup.find_all('div', {"class": "news-list"})
    logging.info('Div size ' + str(len(div_p)))
    divs = []
    for d in div_p:
        if not skip_news(d):
            dt = d.find_all('div', attrs={'class': 'media-block'})
            for dd in dt:
                if is_media(dd):
                    divs.append(dd)
    return divs


def get_videos(url):
    logging.info("Loading " + url)
    headers = {'Cookie': 'beget=begetok; has_js=1;',
               'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38'}
    req = urllib.request.Request(url, None, headers)
    resp = urllib.request.urlopen(req)
    html = resp.read()
    soup = BeautifulSoup(html, "html.parser")

    divs = get_video_divs(soup)
    logging.info('Div size ' + str(len(divs)))

    res = []
    uniq_res = set()
    for d in divs:
        parent_div = d.find_parent('div')
        m = parent_div.find('h3', attrs={'class': 'news__title'})
        link = m.find('a')
        ref = link.get('href')
        if (not ref in uniq_res) and (not skip(d)):
            r = {}

            dt = extract_date(parent_div)
            if dt:
                r["name"] = dt + ' ' + m.get_text()
            else:
                r["name"] = m.get_text()

            r["url"] = ref
            r["genre"] = extract_genre(parent_div)
            r["thumb"] = extract_image(d)
            res.append(r)
            uniq_res.add(ref)
    return res


def extract_date(p_html):
    m = p_html.find('span', attrs={'class': 'info-block__text'})
    if m:
        logging.info('Date ' + m.get_text().encode('utf-8'))
        return m.get_text()
    logging.info('No date ')
    return None


def to_json_string(data):
    try:
        res = json.dumps(data, ensure_ascii=False).encode('utf8')
    except Exception as err:
        logging.error(err)
        res = json.dumps(data, ensure_ascii=True).encode('utf8')
    return res