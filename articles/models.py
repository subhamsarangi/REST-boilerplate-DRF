import secrets
import string

from django.db import models
from django.utils.text import slugify

from myauth.models import User

class Article(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate the slug if not set
        if not self.slug or self.is_title_changed():
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        length = 12
        characters = string.ascii_letters + string.digits  # Alphanumeric characters

        while True:
            random_slug = ''.join(secrets.choice(characters) for _ in range(length))
            if not Article.objects.filter(slug=random_slug).exists():
                return f"{slugify(self.title)}-{random_slug}"


    def is_title_changed(self):
        """
        Check if the title has changed and thus requires a new slug.
        """
        if self.pk:
            old_article = Article.objects.get(pk=self.pk)
            return old_article.title != self.title
        return False

    def __str__(self):
        return self.title
