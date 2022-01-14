# -*- coding: utf-8 -*-
import io
import json
import sys
import unittest

from sympy.stats import std

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
        self.assertGreater(len(d[0]), 0)

    def test_none(self):
        d = extractor.load_data("https://www.lrt.lt/mediateka/video/panorama-none", "panorama")
        self.assertIsNone(d)

    def test_rasytojai_categorySave(self):
        d = extractor.load_data("https://www.lrt.lt/tema/dokumentiniai-filmai-rasytojai", "panorama")
        sys.stdout.write(extractor.to_json_string(d).decode("utf8"))


if __name__ == '__main__':
    unittest.main()
