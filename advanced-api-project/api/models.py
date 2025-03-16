from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=250)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} by {self.author}"