from rest_framework import serializers
from api.models import Book, Author
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
    
    def validate(self, data):
        # use the .get() on data since this is a dict with attributes of the book instance
        publication_year = data.get('publication_year')
        current_year = datetime.now().year
        if publication_year and publication_year > current_year:
            raise serializers.ValidationError("publication_year can't be in the future")
        return data
    
class AuthorSerializer(serializers.ModelSerializer):
    # this is made to return all instances of books related to an instance of author
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ["name", "books"]