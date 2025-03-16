from django.urls import path
from api import views


urlpatterns = [
    path("books/", views.BookListView.as_view(), name = "all books"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name = "Lookup a book"),
    path("books/<int:pk>/create/", views.BookCreateView.as_view(), name = "Create a book"),
    path("books/<int:pk>/delete/", views.BookDeleteView.as_view(), name = "Delete a book"),
    path("books/<int:pk>/update/", views.BookUpdateView.as_view(), name = "Update a book"),
]