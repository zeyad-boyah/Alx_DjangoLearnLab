# delete a book

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984") # will select the book with the title <Book: 1984> 

book.delete() # deletes the book
Book.objects.all() # shows no books <QuerySet []>
```