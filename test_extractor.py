import unittest

import extractor


class MyTestExtract(unittest.TestCase):
    def test_something(self):
        d = extractor.load_data("https://www.lrt.lt/mediateka/video/panorama", "panorama")
        self.assertEqual(d["name"], "Panorama")


if __name__ == '__main__':
    unittest.main()
