import secrets
import string
import os

import boto3
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.contrib.postgres.search import SearchVectorField, SearchVector

from myauth.models import User
from .utils import get_image_upload_path


class Article(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    heroimage = models.ImageField(upload_to=get_image_upload_path, null=True, blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['search_vector']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug or self.is_title_changed() or self.is_content_changed():
            self.search_vector = SearchVector('title', 'content')

        if not self.slug or self.is_title_changed():
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        if self.heroimage:
            if settings.DEBUG:
                if hasattr(self.heroimage, 'path') and os.path.isfile(self.heroimage.path):
                    os.remove(self.heroimage.path)
            else:
                if hasattr(self.heroimage, 'url'):
                    s3 = boto3.client('s3')
                    s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=self.heroimage.name)
        super().delete(*args, **kwargs)

    def generate_unique_slug(self):
        length = 12
        characters = string.ascii_letters + string.digits
        while True:
            random_slug = ''.join(secrets.choice(characters) for _ in range(length))
            if not Article.objects.filter(slug=random_slug).exists():
                return f"{slugify(self.title)}-{random_slug}"


    def is_title_changed(self):
        if self.pk:
            old_article = Article.objects.get(pk=self.pk)
            return old_article.title != self.title
        return False
    
    def is_content_changed(self):
        if self.pk:
            old_article = Article.objects.get(pk=self.pk)
            return old_article.content != self.content
        return False

    def __str__(self):
        return str(self.title)
