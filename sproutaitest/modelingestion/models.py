from django.db import models
# Create your models here.
from django.db.models import ForeignKey


class BlogPost(models.Model):
    title = models.CharField(null=False, max_length=255, unique=True)
    content = models.TextField(null=False)
    has_foul_language = models.BooleanField(null=False, default=False)

    @property
    def has_any_sentence_awaiting_processing(self):
        return self.awaiting_processing_sentences.exists()

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"BlogPost with Title: {self.title} has foul language: {self.has_foul_language}"


class BacklogSentence(models.Model):
    sentence = models.TextField(null=False)
    creation_date = models.DateTimeField(null=False, auto_now_add=True)
    blog_post = ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="awaiting_processing_sentences")
