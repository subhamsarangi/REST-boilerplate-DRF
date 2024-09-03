from myproject.celery import app as celery_app

if __name__ == '__main__':
    celery_app.start(argv=['worker', '-E', '-l', 'INFO', '-P', 'solo'])
