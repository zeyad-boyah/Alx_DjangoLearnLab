from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.models import Book, Author
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    
    def validate(self, attrs):
        publication_year = attrs.get('publication_year')
        current_year = datetime.now().year
        if publication_year and publication_year > current_year:
            raise ValidationError("publication_year can't be in the future")
        return attrs
    