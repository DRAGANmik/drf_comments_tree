from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Article, Comment
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    ArticleSerializer,
    CommentPOSTSerializer,
    CommentSerializer,
)


class ListRetrieveViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    pass


class CommentViewSet(ListRetrieveViewSet):
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ["article"]

    def get_queryset(self):
        if self.action == "list":
            return Comment.objects.root_nodes().select_related(
                "parent", "article"
            )
        return Comment.objects.all().select_related("parent", "article")

    @action(
        detail=True,
        methods=["POST"],
        url_path="add",
        url_name="comment-create",
        serializer_class=CommentPOSTSerializer,
    )
    def comment_create(self, request, pk):
        """Add comment to another comment"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = get_object_or_404(Comment, pk=pk)
        Comment.objects.create(
            **serializer.validated_data,
            parent=comment,
            article=comment.article,
            user=request.user,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=["PATCH", "DELETE"],
        url_path="change",
        url_name="comment-change",
        serializer_class=CommentPOSTSerializer,
    )
    def comment_change(self, request, pk):
        """Update and delete only your comment"""
        serializer = self.serializer_class(data=request.data)
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if request.method == "PATCH":
            serializer.is_valid(raise_exception=True)
            comment.text = serializer.validated_data.get("text")
            comment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleViewSet(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthorOrReadOnly]

    @action(
        detail=True,
        methods=["POST"],
        url_path="comment",
        url_name="comment-create",
        serializer_class=CommentPOSTSerializer,
    )
    def comment(self, request, pk):
        """Add comment to article"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        article = get_object_or_404(Article, pk=pk)
        Comment.objects.create(
            **serializer.validated_data,
            parent=None,
            article=article,
            user=request.user,
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
