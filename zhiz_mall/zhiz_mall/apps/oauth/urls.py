from apps.oauth.views import QQLoginView
from django.urls import path


urlpattern = [
    path('/qq/authorization/', QQLoginView.as_view()),
]