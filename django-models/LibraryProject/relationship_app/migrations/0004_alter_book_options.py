# Generated by Django 5.1.6 on 2025-02-26 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': [('can_add_book', 'Can add books'), ('can_change_book', 'Can edit books'), ('can_delete_book', 'Can delete books')]},
        ),
    ]
