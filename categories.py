# -*- coding: utf-8 -*-


class CInfo:

    def __init__(self):
        pass


settings = [
    {'v_panorama': ['panorama', 'dienos-tema']},
    {'v_sportas': ['sportas-orai']},
    {'v_klauskite_daktaro': ['klauskite-daktaro']},
    {'v_filmai': ['filmai']},
]

statics = [
    {'name': 'Serialai',
     'url': 'https://www.lrt.lt/tema/serialai',
     'genre': 'Serialai',
     'id': 'serials'},
    {'name': 'Mediateka',
     'url': 'https://www.lrt.lt/mediateka',
     'genre': 'Mediateka',
     'id': 'mediateka'},
    {'name': 'Filmai (tema)',
     'url': 'https://www.lrt.lt/tema/filmai',
     'genre': 'Filmai',
     'id': 'movies1'},
    {'name': 'Elito kinas',
     'url': 'https://www.lrt.lt/tema/elito-kinas',
     'genre': 'Filmai',
     'id': 'movies2'},
    {'name': 'Dokumentiniai filmai (tema)',
     'url': 'https://www.lrt.lt/tema/dokumentinis-filmas',
     'genre': 'Filmai',
     'id': 'documentary'},
    {'name': 'Dokumentiniai filmai',
     'url': 'https://www.lrt.lt/mediateka/video/kiti/filmai/dokumentiniai-filmai',
     'genre': 'Filmai',
     'id': 'documentary1'},
    {'name': 'Dokumentiniai filmai - rašytojai',
     'url': 'https://www.lrt.lt/tema/dokumentiniai-filmai-rasytojai',
     'genre': 'Filmai',
     'id': 'documentary2'}

]


def get(addon):
    res = []
    for st in statics:
        c = CInfo()
        c.name = st['name']
        c.id = st['name']
        c.url = st['url']
        res.append(c)
    for set in settings:
        for key in set:
            if addon.getSetting(key) == "true":
                for v_name in set[key]:
                    c = CInfo()
                    c.name = v_name.title()
                    c.id = v_name
                    c.url = "https://www.lrt.lt/mediateka/video/" + v_name
                    res.append(c)
    video = addon.getSetting("video")
    videos = video.split(",")
    for v in videos:
        v = v.strip()
        if v:
            c = CInfo()
            c.name = v.title()
            c.id = v
            c.url = "https://www.lrt.lt/mediateka/video/" + v
            res.append(c)
    return res
