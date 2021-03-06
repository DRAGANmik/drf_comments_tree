from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArticleViewSet, CommentViewSet

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="articles")
router.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("v1/", include(router.urls)),
]
