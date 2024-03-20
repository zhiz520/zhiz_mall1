from django.urls import path
from apps.verifications.views import ImageCodeView, SmsCodeView


urlpatterns = [
    path('image_code/<uuid>/', ImageCodeView.as_view()),
    path('sms_code/<mobile>/', SmsCodeView.as_view()),
]