from rest_framework import generics, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly
from .serializers import BookSerializer
from api.models import Book


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Book.objects.all()
    serializer_class = BookSerializer