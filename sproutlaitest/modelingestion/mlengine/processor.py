import logging

from requests import RequestException

from modelingestion.interfaces.exceptions import ApiEndpointException
from modelingestion.interfaces.mlendpoint import LanguageDetectionModelProtocol
from modelingestion.models import BacklogSentence, BlogPost

logger = logging.Logger(__name__)


def save_sentence_on_failure(func):
    def _wrapper(*args, **kwargs):
        try:
            _res = func(*args, **kwargs)
            return _res
        except (ApiEndpointException, RequestException) as endpoint_failure:
            blog_post = kwargs.get("blog_post")
            sentence = kwargs.get("sentence")
            # If none is in kwargs, they're both in args
            if blog_post is None and sentence is None:
                blog_post, sentence = args
            # case in which one is kwarg and the other is not. sentence cannot come before blog_post
            elif sentence is None:
                sentence = args
            logger.error(f"Failed processing sentence {sentence} for blog_post: {blog_post} because {endpoint_failure}")
            BacklogSentence.objects.create(blog_post=blog_post, sentence=sentence)
        except Exception as general_exception:
            raise general_exception
        return None

    return _wrapper


class BlogpostProcessor:
    def __init__(self, model: LanguageDetectionModelProtocol) -> None:
        super().__init__()
        self._model = model

    @save_sentence_on_failure
    def process_sentence_for_blog_post(self, blog_post: BlogPost, sentence: str):
        """

        :param blog_post:
        :param sentence:
        :return:
        """
        logger.info(f"Processing sentence for {sentence} blog post {blog_post}")
        return self._model.detect_foul_language_in_sentence(sentence=sentence)

    def process_backlog_post(self, backlog_sentence: BacklogSentence) -> bool:
        """

        :param backlog_sentence:
        :return:
        """
        result = self.process_sentence_for_blog_post(blog_post=backlog_sentence.blog_post,
                                                     sentence=backlog_sentence.sentence)
        # If the API is still down, then mark the backlog entry as unprocessed
        if result is None:
            return False
        blog_post = backlog_sentence.blog_post

        # we do not want to update posts that have already found foul language!
        # This could cause situation where an unprocessed sentence overrides the result with a previously foulness
        if not blog_post.has_foul_language:
            blog_post.has_foul_language = result
            blog_post.save()
        return True
