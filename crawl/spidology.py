from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


class SearchologySpider(CrawlSpider):

    name = 'docs.djangoproject.dev'

    def __init__(self, sid=None):
        self.allowed_domains = ['docs.djangoproject.dev']
        self.start_urls = ['http://docs.djangoproject.dev']
        self.rules = (
            Rule(SgmlLinkExtractor(
                allow='.*topics/settings\.html'), callback='parse_item'),
        )
        super(SearchologySpider, self).__init__()

    def parse_item(self, response):
        self.log(response.url)
