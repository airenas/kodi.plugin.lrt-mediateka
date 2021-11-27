import unittest

import extractor


class MyTestExtract(unittest.TestCase):
    def test_something(self):
        d = extractor.load_data("https://www.lrt.lt/mediateka/video/panorama", "panorama")
        self.assertEqual(d["name"], "Panorama")

    def test_videos(self):
        d = extractor.get_videos("https://www.lrt.lt/mediateka/video/panorama")
        self.assertEqual(d[0]["genre"], "Panorama")

    def test_none(self):
        d = extractor.load_data("https://www.lrt.lt/mediateka/video/panorama-none", "panorama")
        self.assertIsNone(d)


if __name__ == '__main__':
    unittest.main()
