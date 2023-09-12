from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

urlpatterns = [
    path("token", TokenObtainPairView.as_view()),
    path("refresh-token", TokenRefreshView.as_view()),
]
