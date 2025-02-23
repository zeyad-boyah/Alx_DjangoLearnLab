from django.shortcuts import render, redirect
from .models import Library, Book, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



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