from django.shortcuts import render, redirect
from .models import Library, Book, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.dispatch import Signal

# testing signals by sending one to user_profile.save
# this is far from the best approach but was done to test the signals framework 
user_profile_created = Signal()


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
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("all_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance, role="Member")
        user_profile_created.send(sender=UserProfile, user_profile=profile)


@receiver(user_profile_created)
def save_user_profile(sender, user_profile, **kwargs):
    user_profile.save()


def is_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Admin"
    )


@user_passes_test(is_admin, login_url="/login/")
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


def is_librarian(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Librarian"
    )


@user_passes_test(is_librarian, login_url="/login/")
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


def is_member(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Member"
    )


@user_passes_test(is_member, login_url="/login/")
def member_view(request):
    return render(request, "relationship_app/member_view.html")
