from django.shortcuts import render
from rest_framework import generics
from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer
from django.contrib.auth.mixins import LoginRequiredMixin

# api to list all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# to look up a specific book with primary key in the slug like /books/pk/
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"

# to create a book with a post request while logged in 
class BookCreateView(LoginRequiredMixin, generics.CreateAPIView ):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"

# to update a book with a Put request while logged in 
class BookUpdateView(LoginRequiredMixin, generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"

# to delete  a book with pk while logged 
class BookDeleteView(LoginRequiredMixin, generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"