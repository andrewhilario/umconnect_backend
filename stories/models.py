from django.db import models
from users.models import UserModel


# Create your models here.
class Stories(models.Model):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="stories"
    )
    story = models.CharField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
