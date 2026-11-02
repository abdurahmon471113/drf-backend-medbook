from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "clinics"

urlpatterns = [
    path("test/", views.TestGetView.as_view(), name="test"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
]