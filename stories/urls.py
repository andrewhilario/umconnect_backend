from django.urls import path
from .views import GetAllStoriesView, CreateStoryView, DeleteStoriesAfter24Hours

urlpatterns = [
    path("", GetAllStoriesView.as_view(), name="all_stories"),
    path("create/", CreateStoryView.as_view(), name="create_story"),
    path(
        "cron/stories/24hour/",
        DeleteStoriesAfter24Hours.as_view(),
        name="delete_stories_after_24hours",
    ),
]
