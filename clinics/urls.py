from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView



app_name = "clinics"








urlpatterns = [
    path("doctors/", views.FindDoctorAPI.as_view(), name="doctors"),
    path("doctors/<int:pk>/services/", views.DoctorServiceDetailAPI.as_view(), name="doctors_services"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path("doctors/<int:pk>/slots/", views.AvailableSlotsAPI.as_view(), name="doctors_slots"),

]