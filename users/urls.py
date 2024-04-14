from django.urls import path
from . import views


urlpatterns = [
    path("register/", views.SignUpView.as_view(), name="signup"),
    path(
        "update/<int:pk>/",
        views.UpdateUserView.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
            }
        ),
        name="update",
    ),
]
