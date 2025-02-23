from django.shortcuts import render, redirect
from .models import Library, Book, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse


def list_books(request):
    books = Book.objects.all()
    return render(
        request,
        template_name="relationship_app/list_books.html",
        context={"books": books},
    )


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"
    slug_field = "slug"
    slug_url_kwarg = "slug"


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('all_books')  
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


def is_admin(user):
    # Check if the user is authenticated and has a UserProfile with role 'Admin'
    return user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

@user_passes_test(is_admin, login_url='/login/')
def admin_view(request):
    return HttpResponse("Welcome, Admin! This is your admin dashboard.")