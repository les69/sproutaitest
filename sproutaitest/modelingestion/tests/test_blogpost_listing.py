from django.test import TestCase
from django.urls import reverse
from modelingestion.models import BacklogSentence, BlogPost


class BlogPostDetailTestCase(TestCase):

    def test_blogpost_details_by_id_existing_instance_completed_processing(self):
        blog_post = BlogPost.objects.create(title="test_blogpost_details_by_id_existing_instance_completed_processing",
                                            content=["test paragraphs"])

        response = self.client.get(reverse("view_blogpost_by_id", kwargs={"blog_post_id": blog_post.id}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "complete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertFalse(blog_post.has_any_sentence_awaiting_processing)

    def test_blogpost_details_by_id_nonexisting_instance(self):
        response = self.client.get(reverse("view_blogpost_by_id", kwargs={"blog_post_id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_blogpost_details_by_id_existing_instance_awaiting_processing(self):
        blog_post = BlogPost.objects.create(
            title="test_blogpost_details_by_id_nonexisting_instance_awaiting_processing",
            content=["test paragraphs"])
        BacklogSentence.objects.create(sentence="test", blog_post=blog_post)
        response = self.client.get(reverse("view_blogpost_by_id", kwargs={"blog_post_id": blog_post.id}))
        self.assertEqual(response.status_code, 202)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "incomplete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertTrue(blog_post.has_any_sentence_awaiting_processing)

    def test_blogpost_details_by_id_existing_instance_awaiting_processing_cleared(self):
        blog_post = BlogPost.objects.create(
            title="test_blogpost_details_by_id_existing_instance_awaiting_processing_cleared",
            content=["test paragraphs"])
        backlog = BacklogSentence.objects.create(sentence="test", blog_post=blog_post)
        response = self.client.get(reverse("view_blogpost_by_id", kwargs={"blog_post_id": blog_post.id}))
        self.assertEqual(response.status_code, 202)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "incomplete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertTrue(blog_post.has_any_sentence_awaiting_processing)

        backlog.delete()
        response = self.client.get(reverse("view_blogpost_by_id", kwargs={"blog_post_id": blog_post.id}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "complete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertFalse(blog_post.has_any_sentence_awaiting_processing)

    def test_blogpost_details_by_title_existing_instance_completed_processing(self):
        blog_post = BlogPost.objects.create(
            title="test_blogpost_details_by_title_existing_instance_completed_processing",
            content=["test paragraphs"])

        response = self.client.get(reverse("view_blogpost_by_title", kwargs={"blog_title": blog_post.title}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "complete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertFalse(blog_post.has_any_sentence_awaiting_processing)

    def test_blogpost_details_by_title_nonexisting_instance(self):
        response = self.client.get(reverse("view_blogpost_by_title", kwargs={"blog_title": "nonexisting"}))
        self.assertEqual(response.status_code, 404)

    def test_blogpost_details_by_title_existing_instance_awaiting_processing(self):
        blog_post = BlogPost.objects.create(
            title="test_blogpost_details_by_id_nonexisting_instance_awaiting_processing",
            content=["test paragraphs"])
        BacklogSentence.objects.create(sentence="test", blog_post=blog_post)
        response = self.client.get(reverse("view_blogpost_by_title", kwargs={"blog_title": blog_post.title}))
        self.assertEqual(response.status_code, 202)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "incomplete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertTrue(blog_post.has_any_sentence_awaiting_processing)

    def test_blogpost_details_by_title_existing_instance_awaiting_processing_cleared(self):
        blog_post = BlogPost.objects.create(
            title="test_blogpost_details_by_id_existing_instance_awaiting_processing_cleared",
            content=["test paragraphs"])
        backlog = BacklogSentence.objects.create(sentence="test", blog_post=blog_post)
        response = self.client.get(reverse("view_blogpost_by_title", kwargs={"blog_title": blog_post.title}))
        self.assertEqual(response.status_code, 202)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "incomplete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertTrue(blog_post.has_any_sentence_awaiting_processing)

        backlog.delete()
        response = self.client.get(reverse("view_blogpost_by_title", kwargs={"blog_title": blog_post.title}))
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response["processing_status"], "complete")
        self.assertEqual(json_response["foul_content_found"], blog_post.has_foul_language)
        self.assertFalse(blog_post.has_any_sentence_awaiting_processing)
