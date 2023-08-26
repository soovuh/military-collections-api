from django.urls import path

from custom_auth.views import UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
]