import logging

from django.core.management.base import BaseCommand

from modelingestion.factories.model_factory import ModelFactory
from modelingestion.mlengine.processor import BlogpostProcessor
from modelingestion.models import BacklogSentence

logger = logging.Logger(__name__)


class Command(BaseCommand):
    """
    Command used to clear all items saved to the backlog for processing when the API is not accessible.
    If not yet accessible items won't be cleared otherwise entries will be removed from the database and where
    meaningful the posts will be updated
    """
    def handle(self, *args, **options):
        processor = BlogpostProcessor(model=ModelFactory.default_factory().create_default_model())
        backlog_entries = BacklogSentence.objects.all()

        entries_to_delete = []
        for entry in backlog_entries:
            logger.info(f"Processing {entry}")
            can_delete_entry = False
            try:
                can_delete_entry = processor.process_backlog_post(backlog_sentence=entry)
            except Exception as failure:
                logger.error(f"Failed processing backlog entry {entry} because {failure}")

            if can_delete_entry:
                entries_to_delete.append(entry.id)
        logger.info(f"Proceeding to remove entries {entries_to_delete}")
        # This is a django inefficiency, the other way would be to delete each manually and it doesn't offer
        # a clear bulk_delete as it does for update or insert but still better than running a delete for each entry
        BacklogSentence.objects.filter(id__in=entries_to_delete).delete()
