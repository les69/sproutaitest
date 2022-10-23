import json
import logging

from django.http import HttpResponseNotFound, JsonResponse
# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from modelingestion.factories.model_factory import ModelFactory
from modelingestion.mlengine.processor import BlogpostProcessor
from modelingestion.models import BlogPost
from modelingestion.request.models import BlogPostRequest

logger = logging.Logger(__name__)


@csrf_exempt
def ingest_blogpost(request):
    """
    Ingest a BlogPost with a Request containing a title and a list of paragraphs, save it into database
    and attempt to run foul text detection on it. Upon Failure, save entries into the database for a later time
    processing.

    :param request:
    :return:
        HttpResponse with status=202 if the processing was incomplete
        HttpResponse with status=200 if all of the processing was done correctly
        HttpResponse with status=500 for any unexpected failures



        All responses also include the fields:
            ingestion_status: (let the user know the processing status independently from http statuses)
            foul_content_found: True/False if any foul text was detected, even with partly processed text
            blog_post_id: Blog post ID for later reference in case processing was incomplete to allow the client to
                check if the complete text had foul text later in time. None in case of failure
    """
    try:
        payload = json.loads(request.body)
        post = BlogPostRequest.build_from_response(payload=payload)
        blog_post = BlogPost.objects.create(title=post.title, content=post.content)
        processor = BlogpostProcessor(model=ModelFactory.default_factory().create_default_model())
        detections = map(
            lambda sentence: processor.process_sentence_for_blog_post(blog_post=blog_post, sentence=sentence),
            post.sentences)
        any_foul = any(detections)
        blog_post.has_foul_language = any_foul
        blog_post.save()

        if blog_post.has_any_sentence_awaiting_processing:
            return JsonResponse(
                data={"ingestion_status": "incomplete", "foul_content_found": any_foul,
                      "blog_post_id": blog_post.id},
                status=202,
                reason="Ingestion incomplete!")
        return JsonResponse(
            data={"ingestion_status": "complete", "foul_content_found": any_foul, "blog_post_id": blog_post.id},
            status=200)
    except Exception as failure:
        # fail nicely
        logger.error(f"Ingestion failed because {failure}")
        return JsonResponse(
            data={"ingestion_status": "failed", "foul_content_found": False, "blog_post_id": None},
            reason=f"internal failure because of {failure}",
            status=500)


@csrf_exempt
def blog_post_details_by_id(request, blog_post_id):
    blog_post = get_object_or_404(BlogPost, pk=blog_post_id)
    if blog_post.has_any_sentence_awaiting_processing:
        return JsonResponse(
            data={"foul_content_found": blog_post.has_foul_language, "processing_status": "incomplete"},
            status=202,
            reason="Ingestion incomplete!")
    return JsonResponse(
        content_type="application/json",
        data={"foul_content_found": blog_post.has_foul_language, "processing_status": "complete"},
        status=200)


@csrf_exempt
def blog_post_details_by_title(request, blog_title):
    try:
        blog_post = BlogPost.objects.get(title=blog_title)
    except BlogPost.DoesNotExist:
        return HttpResponseNotFound()
    if blog_post.has_any_sentence_awaiting_processing:
        return JsonResponse(
            data={"foul_content_found": blog_post.has_foul_language, "processing_status": "incomplete"},
            status=202,
            reason="Ingestion incomplete!")
    return JsonResponse(
        data={"foul_content_found": blog_post.has_foul_language, "processing_status": "complete"},
        status=200)
