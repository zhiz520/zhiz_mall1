from apps.users.views import UsernameCountView, RegisterView
from django.urls import path


urlpatterns = [
    path('usernames/<username:UsernameConverter>/count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
]