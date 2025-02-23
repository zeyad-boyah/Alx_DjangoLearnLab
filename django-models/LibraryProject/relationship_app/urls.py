from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path("all_books/", list_books, name="all_books"),
    path("library_detail/<slug:slug>/", LibraryDetailView.as_view(), name="library_detail"),
]