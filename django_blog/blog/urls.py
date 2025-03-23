from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Authentication URLs from django default
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Custom registration and profile management views
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # post viewsssss
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment/new/', views.add_comment, name='comment-create'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

]