from django.db import models
from users.models import UserModel


# Create your models here.
class ReelModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="reels")
    reel_video = models.CharField(max_length=1000)
    reel_caption = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        UserModel, through="ReelLikeModel", related_name="reel_likes"
    )

    def __str__(self):
        return self.user.username


class ReelCommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    reel = models.ForeignKey(
        ReelModel, on_delete=models.CASCADE, related_name="comments"
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class ReelLikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    reel = models.ForeignKey(
        ReelModel, on_delete=models.CASCADE, related_name="reel_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class ReelShareModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    reel = models.ForeignKey(
        ReelModel, on_delete=models.CASCADE, related_name="reel_shares"
    )
    share_content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
