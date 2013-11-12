from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from bs4 import BeautifulSoup
from boilerpipe.extract import Extractor
from searchology.db import models, session_scope
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
        with session_scope() as session:
            return session.query(
                models.SiteSearch).filter_by(id=self.sid).first()

    def parse_item(self, response):
        html = response.body
        soup = BeautifulSoup(html)
        extractor = Extractor(extractor='ArticleExtractor', html=html)
        text = extractor.getText().encode('utf-8')
        page = {
            "url": response.url,
            "text": text,
            "title": soup.title.string,
        }
        _id = hashlib.md5(response.url).hexdigest()
        es.index(page, index=self.domain, doc_type='page', id=_id, bulk=True)
