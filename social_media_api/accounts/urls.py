from django.urls import path
from accounts import views

urlpatterns = [
    path("register/", views.RegistrationAPIView.as_view(), name="register"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
]
