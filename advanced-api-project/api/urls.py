from django.urls import path
from api import views


urlpatterns = [
    path("books/", views.BookListView.as_view(), name = "all books"),
    path("authors/", views.AuthorBookListview.as_view(), name = "all authors with their books"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name = "Lookup a book"),
    path("books/create/<int:pk>/", views.BookCreateView.as_view(), name = "Create a book"),
    path("books/delete/<int:pk>/", views.BookDeleteView.as_view(), name = "Delete a book"),
    path("books/update/<int:pk>/", views.BookUpdateView.as_view(), name = "Update a book"),
]