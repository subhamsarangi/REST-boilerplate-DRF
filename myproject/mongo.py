import logging

from pymongo import MongoClient
from decouple import config


logger = logging.getLogger('mongo')

def get_mongo_client():
    try:
        client = MongoClient(config('MONGO_URL'))
        return client
    except Exception as e:
        logger.error(f'Error creating MongoDB client: {e}')
        raise

def get_article_collection():
    logger.info("trying here 2")
    try:
        client = get_mongo_client()
        db = client[config('MONGO_DB_NAME')]
        collection = db['article_analytics']
        return collection
    except Exception as e:
        logger.error(f'Error accessing MongoDB collection: {e}')
        raise
