from django.urls import path
from .views import GetAllStoriesView, CreateStoryView

urlpatterns = [
    path("", GetAllStoriesView.as_view(), name="all_stories"),
    path("create/", CreateStoryView.as_view(), name="create_story"),
]
