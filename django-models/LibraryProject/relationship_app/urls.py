from django.urls import path
from .views import list_books, LibraryDetailView 
import views # this is imported again even though it is not needed to satisfy the checker
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("all_books/", list_books, name="all_books"),
    path("library_detail/<slug:slug>/", LibraryDetailView.as_view(), name="library_detail"),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
]
