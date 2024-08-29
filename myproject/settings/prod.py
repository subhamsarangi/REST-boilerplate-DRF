from .base import *

DEBUG = False

ALLOWED_HOSTS = ['my-production-domain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'POSTGRES',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Email settings for production
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.your-email-provider.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@example.com'
# EMAIL_HOST_PASSWORD = 'your-email-password'

# Static files (CSS, JavaScript, Images)

STATIC_ROOT = BASE_DIR / 'staticfiles'