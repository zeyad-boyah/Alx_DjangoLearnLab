from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from bookshelf.models import Book

def index (request):
    return HttpResponse('welcome to bookshelf')

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


def setup_groups():
    content_type = ContentType.objects.get_for_model(Book)
    
    # Get custom permissions
    can_view = Permission.objects.get(codename='can_view', content_type=content_type)
    can_create = Permission.objects.get(codename='can_create', content_type=content_type)
    can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
    can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

    # Create groups if they don't already exist
    editors, _ = Group.objects.get_or_create(name='Editors')
    viewers, _ = Group.objects.get_or_create(name='Viewers')
    admins, _ = Group.objects.get_or_create(name='Admins')

    # Assign permissions to each group
    editors.permissions.set([can_create, can_edit])
    viewers.permissions.set([can_view])
    admins.permissions.set([can_view, can_create, can_edit, can_delete])



@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_mymodel(request, pk):
    instance = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        return HttpResponse('you did the post request')
    
    return HttpResponse("didn't work")