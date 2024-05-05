from django.db import models
from django.contrib.postgres.fields import ArrayField

from users.models import UserModel
from cloudinary.models import CloudinaryField

# Create your models here.


class PostModel(models.Model):
    POST_TYPE = (
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private"),
        ("FRIENDS", "Friends"),
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    post_image = models.CharField(max_length=1000, blank=True, null=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPE, default="PUBLIC")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_shared = models.BooleanField(default=False)
    likes = models.ManyToManyField(UserModel, through="LikeModel", related_name="likes")

    def __str__(self):
        return self.content


class CommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_image = CloudinaryField("comment_image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment


class LikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class ShareModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    share_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class ShareLikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    share = models.ForeignKey(ShareModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class ShareCommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    share = models.ForeignKey(ShareModel, on_delete=models.CASCADE)
    share_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.share_comment
