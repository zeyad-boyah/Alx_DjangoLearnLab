from django.shortcuts import render
from rest_framework import generics, filters
from api.models import Book, Author
from api.serializers import BookSerializer, AuthorSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework



# api to list all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # For filtering by publication_year or other exact matches:
    filterset_fields = ['publication_year']
    # For text searches on title and the related author's name:
    search_fields = ['title', 'author__name']
    # allow ordering by title and publication_year
    ordering_fields = ['title', 'publication_year']  

# to look up a specific book with primary key in the slug like /books/pk/
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]

# to create a book with a post request while logged in 
class BookCreateView(generics.CreateAPIView ):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

# to update a book with a Put request while logged in 
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]

# to delete  a book with pk while logged 
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "pk"
    permission_classes = [IsAuthenticated]


class AuthorBookListview(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer