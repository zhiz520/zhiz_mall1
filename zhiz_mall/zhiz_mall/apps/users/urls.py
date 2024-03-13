from apps.users.views import UsernameCountView
from django.urls import path


urlpatterns = [
    path('usernames/<username:UsernameConverter>/count/', UsernameCountView.as_view())
]