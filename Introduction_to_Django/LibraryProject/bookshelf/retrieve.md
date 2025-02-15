# retrieve a book

```python
from bookshelf.models import Book

Book.objects.get(title="1984") # outputs a book with the same title <Book: 1984>
```