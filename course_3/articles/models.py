import random
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL

class ArticleQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)

class Article(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  
    slug = models.SlugField(max_length=255, blank=True, null=True)
    content = models.TextField()           
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    publish = models.DateField(null=True, blank=True)
    
    objects = ArticleManager()

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    