from relationship_app import models

author = models.Author.objects.get(name=author_name)
books = models.Book.objects.filter(author=author)

all_books = models.Book.objects.get()

librarian = models.Librarian.objects.get(name= librarian_name)
librarian_library = librarian.library
