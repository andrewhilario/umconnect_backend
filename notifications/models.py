from django.db import models
from users.models import UserModel


# Create your models here.
class Notifications(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="notifications", null=True
    )
    title = models.CharField(max_length=100)
    message = models.TextField()
    notification_type = models.CharField(max_length=100)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
