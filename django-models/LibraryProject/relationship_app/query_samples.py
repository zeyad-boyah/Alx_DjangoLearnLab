from relationship_app import models


def query_books_by_author(author_name):
    author = models.Author.objects.get(name=author_name)
    return models.Book.objects.filter(author=author)


def list_books_in_library(library_name):

    try:
        library = models.Library.objects.get(name=library_name)
        return library.books.all()
    except models.Library.DoesNotExist:
        return None


def get_librarian_for_library(library_name):
    library = models.Library.objects.get(name=library_name)
    librarian = models.Librarian.objects.get(library=library)
    return librarian


# Example usage:
if __name__ == "__main__":
    books = query_books_by_author("john")
    print("Books by 'john':", list(books))

    library_books = list_books_in_library("Central Library")
    if library_books is not None:
        print("Books in 'Central Library':", list(library_books))
    else:
        print("Library 'Central Library' not found.")

    librarian = get_librarian_for_library("Central Library")
    if librarian is not None:
        print("Librarian for 'Central Library':", librarian)
    else:
        print("No librarian found for 'Central Library'.")
