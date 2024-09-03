import logging

from celery import shared_task

from myproject.mongo import get_article_collection


logger = logging.getLogger('mongo')

@shared_task(time_limit=10)
def increment_article_view_count(slug):
    collection = get_article_collection()
    try:
        logger.info("trying here 3")
        result = collection.update_one(
            {'slug': slug},
            {'$inc': {'views': 1}},
            upsert=True
        )
        logger.info(f'Article view count updated. Slug: {slug}, Modified Count: {result.modified_count}')
        return result.modified_count
    except Exception as e:
        logger.error(f'Error updating article view count for slug {slug}: {e}')
        raise