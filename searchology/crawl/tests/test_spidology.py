import unittest
from searchology.crawl.spidology import SearchologySpider

class TestSearchologySpider(unittest.TestCase):

    def setUp(self):
        self.spider = SearchologySpider()

    def tearDown(self):
        pass

