from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

User = get_user_model()


class Article(models.Model):

    title = models.CharField(max_length=100)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author"
    )
    comments = models.ManyToManyField(
        "Comment", blank=True, related_name="article_comments"
    )


class Comment(MPTTModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comment"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user"
    )
    text = models.TextField()
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    def clean(self):
        if self.parent is not None:
            if self.parent.article != self.article:
                raise ValidationError(
                    "Родительский комментарий привязан к другой статье"
                )
