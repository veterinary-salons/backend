from django.urls import path
from drf_social_oauth2.views import TokenView

urlpatterns = [path("token", TokenView.as_view())]
