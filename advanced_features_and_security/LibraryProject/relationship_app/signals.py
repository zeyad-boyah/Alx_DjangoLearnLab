from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Book

@receiver(post_migrate)
def assign_book_permissions(sender, **kwargs):
    # Run this only for your app (adjust 'myapp' as needed)
    if sender.name != 'relationship_app':
        return

    content_type = ContentType.objects.get_for_model(Book)
    add_perm = Permission.objects.get(codename='can_add_book', content_type=content_type)
    change_perm = Permission.objects.get(codename='can_change_book', content_type=content_type)
    delete_perm = Permission.objects.get(codename='can_delete_book', content_type=content_type)

    # Create groups for each role
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    librarian_group, _ = Group.objects.get_or_create(name='Librarian')
    member_group, _ = Group.objects.get_or_create(name='Member')

    # Assign permissions:
    # - Admins get all permissions.
    admin_group.permissions.set([add_perm, change_perm, delete_perm])
    # - Librarians might get add and change but not delete.
    librarian_group.permissions.set([add_perm, change_perm])
    # - Members may not get any of these custom permissions.
