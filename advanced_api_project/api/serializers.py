from rest_framework import serializers
from api.models import Book, Author
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    
    def validate(self, data):
        publication_year = data.get('publication_year')
        current_year = datetime.now().year
        if publication_year and publication_year > current_year:
            raise serializers.ValidationError("publication_year can't be in the future")
        return data
    
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True)
    class Meta:
        model = Author
        fields = ["name", "books"]