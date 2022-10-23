from unittest import TestCase

from request.models import BlogPostRequest


class BlogPostResponseTestCase(TestCase):
    def test_creation_with_valid_request_single_paragraph_single_sentence(self):
        payload = {"title": "test", "paragraphs": ["first paragraph text."]}
        post = BlogPostRequest.build_from_response(payload=payload)
        self.assertEqual(post.title, "test")
        self.assertEqual(post.content, "first paragraph text.")
        self.assertEqual(post.sentences, [post.title, "first paragraph text"])

    def test_creation_with_valid_request_single_paragraph_with_multiple_sentences(self):
        payload = {"title": "test", "paragraphs": ["first paragraph sentence.second sentence"]}
        post = BlogPostRequest.build_from_response(payload=payload)
        self.assertEqual(post.title, "test")
        self.assertEqual(post.content, "first paragraph sentence.second sentence")
        self.assertEqual(post.sentences, [post.title, "first paragraph sentence", "second sentence"])

    def test_creation_with_valid_request_multiple_paragraphs_with_multiple_sentences(self):
        payload = {"title": "test",
                   "paragraphs": ["first paragraph sentence.second sentence.",
                                  "second paragraph first sentence.hello"]}
        post = BlogPostRequest.build_from_response(payload=payload)
        self.assertEqual(post.title, "test")
        self.assertEqual(post.content,
                         "first paragraph sentence.second sentence.second paragraph first sentence.hello")
        self.assertEqual(post.sentences,
                         [post.title, "first paragraph sentence", "second sentence", "second paragraph first sentence",
                          "hello"])

    def test_creation_should_raise_error_missing_title(self):
        payload = {"paragraphs": ["first paragraph text."]}
        self.assertRaises(KeyError, BlogPostRequest.build_from_response, payload=payload)

    def test_creation_should_raise_error_missing_paragraph(self):
        payload = {"title": "test"}
        self.assertRaises(KeyError, BlogPostRequest.build_from_response, payload=payload)

    def test_creation_with_empty_paragraphs(self):
        payload = {"title": "test", "paragraphs": []}
        post = BlogPostRequest.build_from_response(payload=payload)
        self.assertEqual(post.title, "test")
        self.assertEqual(post.content, "")
        self.assertEqual(post.sentences, [post.title])
