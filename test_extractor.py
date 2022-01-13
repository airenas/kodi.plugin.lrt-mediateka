# -*- coding: utf-8 -*-
import io
import json
import unittest

import extractor


class MyTestExtract(unittest.TestCase):
    def test_something(self):
        d = extractor.load_data("https://www.lrt.lt/mediateka/video/panorama", "panorama")
        self.assertEqual(d["name"], "Panorama")

    def test_videos(self):
        d = extractor.get_videos("https://www.lrt.lt/mediateka/video/panorama")
        self.assertEqual(d[0]["genre"], "Panorama")

    def test_rasytojai(self):
        d = extractor.get_videos("https://www.lrt.lt/tema/dokumentiniai-filmai-rasytojai")
        self.assertEqual(d[0]["genre"], "Filmai")

    def test_none(self):
        d = extractor.load_data("https://www.lrt.lt/mediateka/video/panorama-none", "panorama")
        self.assertIsNone(d)

    def test_rasytojai_categorySave(self):
        d = extractor.load_data("https://www.lrt.lt/tema/dokumentiniai-filmai-rasytojai", "panorama")
        with io.open("t.json", 'w', encoding='utf-8') as fo:
            j_str = json.dumps(d, ensure_ascii=False, encoding='utf8')
            fo.write(unicode(j_str))


if __name__ == '__main__':
    unittest.main()
