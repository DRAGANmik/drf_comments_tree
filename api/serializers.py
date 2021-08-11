from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Article, Comment

User = get_user_model()


class CommentPOSTSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "text"]


class CommentSerializer(serializers.ModelSerializer):

    children = serializers.SerializerMethodField(
        read_only=True, method_name="get_child_comments"
    )

    class Meta:
        model = Comment
        fields = ["id", "text", "article", "user", "children"]

    def get_child_comments(self, obj):
        serializer = CommentSerializer(instance=obj.get_children(), many=True)
        return serializer.data


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "title"]

        model = Article

    def create(self, validated_data):
        request = self.context.get("request")
        article = Article.objects.create(**validated_data, author=request.user)
        return article
