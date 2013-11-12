import unittest
from collections import OrderedDict
from searchology.app.blueprints.api.page_snippet import SearchQuerySnippet

TEXT = """
The text starts here.
This is the second sentence of the text.
This is the third.
This is the last sentence of the text.
"""

class TestSearchQuerySnippet(unittest.TestCase):

    def setUp(self):
        self.sqs = SearchQuerySnippet(TEXT, 'sentence', 90)

    def test_highlighter_with_default_wrapper(self):
        self.assertEqual(
            self.sqs.highlighter(
                'The word strong should be tagged.', 'strong'),
            'The word <strong>strong</strong> should be tagged.'
        )

    def test_highlighter_with_alternate_wrapper(self):
        self.assertEqual(
            self.sqs.highlighter(
                'The word strong should be tagged.', 'strong', '<em>', '</em>'),
            'The word <em>strong</em> should be tagged.'
        )

    def test_sentence_truncation_to_word_boundary(self):
        self.assertEqual(
            self.sqs.truncate_sentence('three word sentence.', 14),
            'three word'
        )

    def test_snippet_gets_truncated(self):
        self.assertLessEqual(len(self.sqs.snippet), 90)

    def test_snippet_has_query_highlighted(self):
        self.assertEqual(
            self.sqs.highlighted_snippet,
            'This is the second <strong>sentence</strong> of the text. '
            'This is the third. This is the last <strong>sentence</strong> of'
        )

    def test_gets_first_sentence_with_term_in(self):
        self.assertEqual(
            self.sqs.first_sentence,
            {'text': 'This is the second sentence of the text.', 'span': (22, 62)}
        )

    def test_gets_last_sentence(self):
        self.assertEqual(
            self.sqs.last_sentence,
            {'text': 'This is the last sentence of the text.', 'span': (82, 120)}
        )

    def test_sentences_are_in_ordered_dict(self):
        self.assertIsInstance(self.sqs.sentences, OrderedDict)

    def test_sentences_are_in_correct_order(self):
        self.assertEqual(
            self.sqs.sentences.keys(),
            [
                "The text starts here.",
                "This is the second sentence of the text.",
                "This is the third.",
                "This is the last sentence of the text."
            ]
        )

    def test_sentence_spans_are_in_correct_position(self):
        self.assertEqual(
            self.sqs.sentences.values(),
            [
                (0, 21),
                (22, 62),
                (63, 81),
                (82, 120)
            ]
        )


class TestSearchQuerySnippetNoMatchedTerm(unittest.TestCase):

        def setUp(self):
            self.sqs = SearchQuerySnippet(TEXT, 'banana')

        def test_first_sentence_is_just_first_sentence_of_text(self):
            self.assertEqual(
                self.sqs.first_sentence,
                {'text': 'The text starts here.', 'span': (0, 21)}
            )
