import json
from unittest import mock

from django.test import TestCase
from django.urls import reverse
from modelingestion.interfaces.mlendpoint import LanguageDetectionModelProtocol
from modelingestion.mlengine.processor import ApiEndpointException
from modelingestion.models import BacklogSentence, BlogPost


class WorkingMockModel(LanguageDetectionModelProtocol):
    protocol_name = "working_mock_model"

    def detect_foul_language_in_sentence(self, sentence: str) -> bool:
        if "test_foul_word" in sentence:
            return True
        return False


class UnavailableMockModel(LanguageDetectionModelProtocol):
    protocol_name = "unavailable_mock_model"

    def detect_foul_language_in_sentence(self, sentence: str) -> bool:
        raise ApiEndpointException("error")


class IngestionViewTestCase(TestCase):

    @mock.patch("modelingestion.factories.model_factory.ModelFactory.create_default_model",
                return_value=WorkingMockModel())
    def test_ingestion_text_without_foul_language_api_working(self, _mock):
        payload = {"title": "test_ingestion_text_without_foul_language_api_working",
                   "paragraphs": ["first paragraph sentence.second sentence"]}
        response = self.client.post(reverse("ingest-blogpost"), data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        blog_post = BlogPost.objects.get(title=payload["title"])
        self.assertIsNotNone(blog_post)
        self.assertFalse(blog_post.has_foul_language)
        json_response = response.json()
        self.assertEqual(json_response["blog_post_id"], blog_post.id)
        self.assertEqual(json_response["ingestion_status"], "complete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)

    @mock.patch("modelingestion.factories.model_factory.ModelFactory.create_default_model",
                return_value=WorkingMockModel())
    def test_ingestion_text_with_foul_language_api_working(self, _mock):
        payload = {"title": "test_ingestion_text_with_foul_language_api_working",
                   "paragraphs": ["first paragraph test_foul_word.second sentence"]}
        response = self.client.post(reverse("ingest-blogpost"), data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        blog_post = BlogPost.objects.get(title=payload["title"])
        self.assertIsNotNone(blog_post)
        self.assertTrue(blog_post.has_foul_language)
        json_response = response.json()
        self.assertEqual(json_response["blog_post_id"], blog_post.id)
        self.assertEqual(json_response["ingestion_status"], "complete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)

    @mock.patch("modelingestion.factories.model_factory.ModelFactory.create_default_model",
                return_value=WorkingMockModel())
    def test_ingestion_text_with_foul_language_invalid_payload(self, _mock):
        payload = {"invalid_entry": "test_ingestion_text_with_foul_language_invalid_payload",
                   "paragraphs": ["first paragraph test_foul_word.second sentence"]}
        response = self.client.post(reverse("ingest-blogpost"), data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 500)
        json_response = response.json()
        self.assertEqual(json_response["blog_post_id"], None)
        self.assertEqual(json_response["ingestion_status"], "failed")
        self.assertFalse(json_response["foul_content_found"])

    @mock.patch("modelingestion.factories.model_factory.ModelFactory.create_default_model",
                return_value=UnavailableMockModel())
    def test_ingestion_text_with_foul_language_api_not_working(self, _mock):
        payload = {"title": "test_ingestion_text_with_foul_language_api_not_working",
                   "paragraphs": ["first paragraph test_foul_word.second sentence"]}
        response = self.client.post(reverse("ingest-blogpost"), data=json.dumps(payload),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 202)
        blog_post = BlogPost.objects.get(title=payload["title"])
        self.assertIsNotNone(blog_post)
        self.assertTrue(BacklogSentence.objects.filter(blog_post=blog_post).exists())
        self.assertTrue(blog_post.awaiting_processing_sentences)
        json_response = response.json()
        self.assertEqual(json_response["blog_post_id"], blog_post.id)
        self.assertEqual(json_response["ingestion_status"], "incomplete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
