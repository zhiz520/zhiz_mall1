from apps.oauth.views import QQLoginView, OauthQQView
from django.urls import path


urlpattern = [
    path('/qq/authorization/', QQLoginView.as_view()),
    path('oauth_callback/', OauthQQView.as_view()),
]