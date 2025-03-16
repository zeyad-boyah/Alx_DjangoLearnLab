from django.shortcuts import render
from rest_framework import generics
from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
class BookCreateView(generics.CreateAPIView ):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

# to update a book with a Put request while logged in 
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

# to delete  a book with pk while logged 
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]