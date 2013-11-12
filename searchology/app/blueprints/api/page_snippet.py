import nltk.data
from nltk.tokenize import WhitespaceTokenizer
from collections import OrderedDict
from operator import itemgetter
import re


class SearchQuerySnippet(object):

    def __init__(self, text, query_string, max_length=170, tokenizer=None):
        self.text = text.strip().replace('\n', ' ')
        self.query_string = query_string
        self.max_length = max_length
        if tokenizer is None:
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = tokenizer

    def truncate_sentence(self, sentence, truncate_to):
        spans = WhitespaceTokenizer().span_tokenize(sentence)
        span = next(span for span in spans if span[1] > truncate_to)
        return sentence[:span[0]-1]

    def highlighter(
            self, text, phrase_to_highlight,
            before='<strong>', after='</strong>'):
        highlighted = ''
        regex = re.compile(r"\b{}\b".format(phrase_to_highlight), re.I)
        i = 0
        for m in regex.finditer(text):
            highlighted += ''.join([
                text[i:m.start()],
                before,
                text[m.start():m.end()],
                after
            ])
            i = m.end()
        return "".join([highlighted, text[i:]])

    @property
    def sentences(self):
        if not hasattr(self, '_sentences'):
            sentences = self.tokenizer.tokenize(self.text)
            spans = self.tokenizer.span_tokenize(self.text)
            d = dict(zip(sentences, spans))
            self._sentences = OrderedDict(
                sorted(d.iteritems(), key=itemgetter(1)))
        return self._sentences

    @property
    def first_sentence(self):
        if not hasattr(self, '_first_sentence'):
            try:
                sentence, span = next(
                    (sentence, span) for sentence, span
                        in self.sentences.iteritems()
                            if self.query_string in sentence)
            except StopIteration:
                sentence, span = self.sentences.items()[0]
            self._first_sentence = {
                'text': sentence,
                'span': span
            }
        return self._first_sentence

    @property
    def last_sentence(self):
        if not hasattr(self, '_last_sentence'):
            try:
                sentence, span = next(
                    (sentence, span) for sentence, span in self.sentences.iteritems()
                        if span[1] > (
                            self.max_length + self.first_sentence['span'][0])
                )
            except StopIteration:
                sentence, span = self.sentences.items()[-1]
            self._last_sentence = {
                'text': sentence,
                'span': span
            }
        return self._last_sentence

    @property
    def snippet(self):
        if not hasattr(self, '_snippet'):
            if len(self.text) < self.max_length:
                return self.text
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

    @property
    def highlighted_snippet(self):
        if not hasattr(self, '_highlighted_snippet'):
            self._highlighted_snippet = self.highlighter(
                self.snippet, self.query_string)
        return self._highlighted_snippet
