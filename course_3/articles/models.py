import random
from django.db import models
from django.utils.text import slugify

class Article(models.Model):
    title = models.CharField(max_length=255)  
    slug = models.SlugField(max_length=255, blank=True, null=True)
    content = models.TextField()           
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    publish = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
