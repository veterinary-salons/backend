from django.urls import path
from drf_social_oauth2.views import TokenView, InvalidateSessions

urlpatterns = [
    path("token", TokenView.as_view()),
    path("invalidate-sessions", InvalidateSessions.as_view()),
]
