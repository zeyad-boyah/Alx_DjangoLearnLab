# retrieve a book

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984") # outputs a book with the same title <Book: 1984>
print(vars(book)) # this will display the all the book attributes {'_state': <django.db.models.base.ModelState object at 0x7f817332bac0>, 'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'George Orwell', 'publication_year': 1949}
```