import nltk.data
from nltk.tokenize import WhitespaceTokenizer
from collections import OrderedDict
from operator import itemgetter
import re


class SearchQuerySnippet(object):

    def __init__(self, text, query_string, max_length):
        self.text = text.replace('\n', '. ').replace('..', '.')
        self.query_string = query_string
        self.max_length = max_length

    def truncate_sentence(self, sentence, truncate_to):
        spans = WhitespaceTokenizer().span_tokenize(sentence)
        span = next(span for span in spans if span[1] > truncate_to)
        return sentence[:span[0]-1]

    @property
    def last_sentence(self):
        if not hasattr(self, '_last_sentence'):
            last_sentence_span = next(
                span for sentence, span in self.sentences.iteritems()
                if span[1] > (
                    self.max_length + self.first_sentence['span'][0]))
            self._last_sentence = {
                'text': self.text[last_sentence_span[0]:last_sentence_span[1]],
                'span': last_sentence_span
            }
        return self._last_sentence

    @property
    def sentences(self):
        if not hasattr(self, '_sentences'):
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            sentences = tokenizer.tokenize(self.text)
            spans = tokenizer.span_tokenize(self.text)
            d = dict(zip(sentences, spans))
            self._sentences = OrderedDict(
                sorted(d.iteritems(), key=itemgetter(1)))
        return self._sentences

    @property
    def first_sentence(self):
        if not hasattr(self, '_first_sentence'):
            span = next(
                span for sentence, span
                in self.sentences.iteritems() if self.query_string in sentence)
            self._first_sentence = {
                'text': self.text[span[0]:span[1]],
                'span': span
            }
        return self._first_sentence

    @property
    def highlighted_snippet(self):
        if not hasattr(self, '_highlighted_snippet'):
            self._highlighted_snippet = ''
            regex = re.compile(r"\b{}\b".format(self.query_string), re.I)
            i = 0
            for m in regex.finditer(self.snippet):
                self._highlighted_snippet += ''.join([
                    self.snippet[i:m.start()],
                    "<strong>",
                    self.snippet[m.start():m.end()],
                    "</strong>"
                ])
                i = m.end()
            self._highlighted_snippet = "".join([self._highlighted_snippet, self.snippet[m.end():]])
        return self._highlighted_snippet

    @property
    def snippet(self):
        if not hasattr(self, '_snippet'):
            if len(self.first_sentence['text']) > self.max_length:
                self._snippet = self.truncate_sentence(
                    self.first_sentence['text'], self.max_length)
            else:
                start = self.text[
                    self.first_sentence['span'][0]:self.last_sentence['span'][0]-1]
                end = self.truncate_sentence(
                    self.last_sentence['text'], self.max_length - len(start))
                self._snippet = (start + ' ' + end).strip()
        return self._snippet
