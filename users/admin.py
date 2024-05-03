from django.contrib import admin
from .models import *


# Register your models here.
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "date_of_birth",
        "phone_number",
        "bio",
        "created_at",
    ]


class FriendsAdmin(admin.ModelAdmin):
    list_display = ["user", "friend"]


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(Friends, FriendsAdmin)
