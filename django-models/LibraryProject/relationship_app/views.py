from django.shortcuts import render
from .models import Library, Book
from django.views.generic import DetailView

def book_list (request):
    books = Book.objects.all()
    return render(request, template_name='relationship_app/list_books.html', context={'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    slug_field = 'slug'       
    slug_url_kwarg = 'slug'