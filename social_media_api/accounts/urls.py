from django.urls import path
from accounts import views

urlpatterns = [
    path("register/", views.RegistrationAPIView.as_view(), name="register"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path("follow/<int:user_id>/", views.FollowUserAPIView.as_view(), name="follow-user"),
    path("unfollow/<int:user_id>/", views.UnFollowUserAPIView.as_view(), name="unfollow-user"),
]
