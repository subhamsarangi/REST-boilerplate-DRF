from celery import shared_task

@shared_task
def basic_article_task(arg1, arg2):
    # Your task logic here
    return f"Task completed with arguments: {arg1}, {arg2}"