from rest_framework import serializers
from .models import Article
from api.serializers import UserPublicSerializer

class ArticleSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(source='user', read_only=True)
    class Meta:
        model = Article
        fields = [
            'pk',
            'author',
            'title',
            'body',
            'path',
            'endpoint',
        ]