from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'heroimage', 'is_published', 'slug', 'owner', 'created_at', 'updated_at']
        read_only_fields = ['owner', 'created_at', 'updated_at', 'slug']

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data) 
