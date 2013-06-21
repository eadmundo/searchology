from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from boilerpipe.extract import Extractor
from db import models, session
import pyes
import hashlib
import atexit

es = pyes.ES('localhost:9200')


@atexit.register
def refresh_es():
    es.refresh()


class SearchologySpider(CrawlSpider):

    name = 'searchologyspider'

    def __init__(self, sid=None):
        self.session = session
        self.sid = sid
        self.name = self.domain
        self.allowed_domains = [self.domain]
        self.start_urls = ['http://{}'.format(self.domain)]
        self.rules = (
            Rule(
                SgmlLinkExtractor(
                    # allow='.*intro\/overview\.html'
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
        return 'docs.djangoproject.dev'

    @property
    def site_search(self):
        return self.session.query(
            models.SiteSearch).filter_by(id=self.sid).first()

    def parse_item(self, response):
        extractor = Extractor(extractor='ArticleExtractor', html=response.body)
        text = extractor.getText().encode('utf-8')
        page = {
            "url": response.url,
            "text": text,
        }
        _id = hashlib.md5(response.url).hexdigest()
        es.index(page, index=self.domain, doc_type='page', id=_id, bulk=True)
