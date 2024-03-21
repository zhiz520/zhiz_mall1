from apps.users.views import CenterView, LoguotView, UsernameCountView, RegisterView, LoginView
from django.urls import path


urlpatterns = [
    path('usernames/<username:UsernameConverter>/count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LoguotView.as_view()),
    path('center/', CenterView.as_view())

]