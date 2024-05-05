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


class FriendRequestsAdmin(admin.ModelAdmin):
    list_display = ["sender", "receiver", "is_accepted"]


admin.site.register(UserModel, UserModelAdmin)
admin.site.register(Friends, FriendsAdmin)
admin.site.register(FriendRequests, FriendRequestsAdmin)
