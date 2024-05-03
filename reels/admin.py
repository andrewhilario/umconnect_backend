from django.contrib import admin

# Register your models here.
from .models import *


class ReelCommentAdmin(admin.ModelAdmin):
    list_display = ["user", "reel", "comment", "created_at"]
    search_fields = ["user", "reel", "comment", "created_at"]
    list_filter = ["user", "reel", "comment", "created_at"]

    class Meta:
        model = ReelCommentModel


class ReelLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "reel", "created_at"]
    search_fields = ["user", "reel", "created_at"]
    list_filter = ["user", "reel", "created_at"]

    class Meta:
        model = ReelLikeModel


class ReelShareAdmin(admin.ModelAdmin):
    list_display = ["user", "reel", "share_content", "created_at"]
    search_fields = ["user", "reel", "share_content", "created_at"]
    list_filter = ["user", "reel", "share_content", "created_at"]

    class Meta:
        model = ReelShareModel


class ReelAdmin(admin.ModelAdmin):
    list_display = ["user", "reel_video", "reel_caption", "created_at"]
    search_fields = ["user", "reel_video", "reel_caption", "created_at"]
    list_filter = ["user", "reel_video", "reel_caption", "created_at"]

    class Meta:
        model = ReelModel


admin.site.register(ReelCommentModel, ReelCommentAdmin)
admin.site.register(ReelLikeModel, ReelLikeAdmin)
admin.site.register(ReelShareModel, ReelShareAdmin)
admin.site.register(ReelModel, ReelAdmin)
