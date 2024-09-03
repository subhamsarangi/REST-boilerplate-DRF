from .base import *


DEBUG = False

ALLOWED_HOSTS = ['backend-service.com']

CORS_ALLOWED_ORIGINS = [
    'https://frontend-service.com',
]

CORS_URLS_REGEX = r'^/api/.*$'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', 'us-east-1')

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com/'

CELERY_BROKER_URL = config('CELERY_BROKER_URL') # or use your preferred broker
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND') 
