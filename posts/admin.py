from django.contrib import admin
from .models import PostModel, LikeModel, CommentModel


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at", "updated_at"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 20


class LikesAdmin(admin.ModelAdmin):
    list_display = ["user", "post", "created_at"]
    search_fields = ["user__username"]
    list_filter = ["created_at"]
    list_per_page = 20


class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "comment", "created_at", "updated_at"]
    search_fields = ["user__username"]
    list_filter = ["created_at", "updated_at"]
    list_per_page = 20


admin.site.register(PostModel, PostAdmin)
admin.site.register(LikeModel, LikesAdmin)
admin.site.register(CommentModel, CommentAdmin)
