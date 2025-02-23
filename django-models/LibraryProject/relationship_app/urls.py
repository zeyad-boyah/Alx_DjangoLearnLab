from django.urls import path
from . import views

urlpatterns = [
    path("all_books/", views.book_list, name="all_books"),
    path("library_detail/<slug:slug>/", views.LibraryDetailView.as_view(), name="library_detail"),
]