from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from boilerpipe.extract import Extractor
import db
from db import models


class SearchologySpider(CrawlSpider):

    name = 'searchologyspider'

    def __init__(self, sid=None):
        self.session = db.session
        self.sid = sid
        self.name = self.domain
        self.allowed_domains = [self.domain]
        self.start_urls = ['http://{}'.format(self.domain)]
        self.rules = (
            Rule(
                SgmlLinkExtractor(
                    #allow='.*intro\/overview\.html'
                ),
                callback='parse_item',
                follow=False
            ),
        )
        super(SearchologySpider, self).__init__()

    @property
    def domain(self):
        if self.site_search is not None:
            return self.site_search.domain
        return 'djangodocs.dev'

    @property
    def site_search(self):
        return self.session.query(
            models.SiteSearch).filter_by(id=self.sid).first()

    def parse_item(self, response):
        extractor = Extractor(extractor='ArticleExtractor', html=response.body)
        print extractor.getText().encode('utf-8')
