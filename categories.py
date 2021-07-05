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
    {'name': 'Dokumentiniai filmai (tema)',
     'url': 'https://www.lrt.lt/tema/dokumentinis-filmas',
     'genre': 'Filmai',
     'id': 'documentary'},
    {'name': 'Dokumentiniai filmai',
     'url': 'https://www.lrt.lt/mediateka/video/kiti/filmai/dokumentiniai-filmai',
     'genre': 'Filmai',
     'id': 'documentary1'}
]


def get():
    res = []
    for st in statics:
        c = CInfo()
        c.name = st['name']
        c.id = st['name']
        c.url = st['url']
        res.append(c)
    return res
