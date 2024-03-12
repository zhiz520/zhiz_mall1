from apps.users.views import UsernameCountView
from django.urls import path


urlpatterns = [
    path('username/<username:UsernameConverter>/count/', UsernameCountView.as_view())
]