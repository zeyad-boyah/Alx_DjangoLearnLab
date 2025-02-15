# update 

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984") # will select the book with the title <Book: 1984> 
book.author = "George Orwell" # updates the author name
book.save() # save the changes

```