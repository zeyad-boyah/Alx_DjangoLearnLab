from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=19.99)
    
