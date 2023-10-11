from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from authentication.v1.views import SignUpViewSet, SignInViewSet


router = DefaultRouter()
router.register("signup", SignUpViewSet, basename="signup")
router.register("signin", SignInViewSet, basename="signin")


urlpatterns = [
    path("token", TokenObtainPairView.as_view()),
    path("refresh-token", TokenRefreshView.as_view()),
    path("", include(router.urls)),
]
