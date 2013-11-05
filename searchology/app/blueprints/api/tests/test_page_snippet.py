import unittest
from searchology.app.blueprints.api.page_snippet import SearchQuerySnippet


class TestSearchQuerySnippet(unittest.TestCase):

    def setUp(self):
        with open('/vagrant/moby-dick.txt') as f:
            self.text = f.read()
        self.sqs = SearchQuerySnippet(self.text, 'reefs', 170)

    def test_first_sentence(self):
        print self.sqs.first_sentence

    def test_sentences(self):
        print self.sqs.sentences
