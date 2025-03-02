from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import Group
from django.conf import settings

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    class Meta():
        permissions = [
            ("can_add_book", "Can add books"),
            ("can_change_book","Can edit books"),
            ("can_delete_book", "Can delete books"),
        ]

    def __str__(self):
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    books = models.ManyToManyField(Book, related_name="library")

    def save(self, *args, **kwargs):
        # Automatically generate a slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(
        Library, related_name="librarian", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ("Admin", "Admin"),
        ("Librarian", "Librarian"),
        ("Member", "Member"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def assign_user_group(self):
        if self.role == "Admin":
            group = Group.objects.get(name="Admin")
        elif self.role == "Librarian":
            group = Group.objects.get(name="Librarian")
        elif self.role == "Member":
            group = Group.objects.get(name="Member")
        self.user.groups.add(group)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password) # if password is none it will be marked as unusable so he can't login in with blank pass (for social login)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, date_of_birth, password, **extra_fields)


class CustomUser (AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField()

    objects= CustomUserManager()