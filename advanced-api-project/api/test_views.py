from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from api.models import Book, Author
from datetime import datetime

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user.
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # Create an author instance.
        self.author = Author.objects.create(name='Author One')
        # Create two book instances.
        self.book1 = Book.objects.create(title='Book One', publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2019, author=self.author)
        self.client = APIClient()

    def test_list_books(self):
        """Test listing all books."""
        url = reverse('all books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect two books in the response.
        self.assertEqual(len(response.data), 2)

    def test_create_book_without_authentication(self):
        """Test that unauthenticated users cannot create a book."""
        self.client.logout()  # Ensure no user is logged in.
        url = reverse('Create a book', kwargs={'pk': self.author.pk})
        data = {
            'title': 'Book Three',
            'publication_year': 2021,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        # This should be forbidden if authentication is required.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_with_authentication(self):
        """Test creating a book with proper authentication."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('Create a book', kwargs={'pk': self.author.pk})
        data = {
            'title': 'Book Three',
            'publication_year': 2021,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify the book count increased.
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        """Test updating an existing book."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('Update a book', kwargs={'pk': self.book1.pk})
        data = {
            'title': 'Book One Updated',
            'publication_year': 2020,
            'author': self.author.pk
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One Updated')

    def test_delete_book(self):
        """Test deleting a book."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('Delete a book', kwargs={'pk': self.book1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_filter_books_by_publication_year(self):
        """Test filtering books by publication_year."""
        url = reverse('all books')
        response = self.client.get(url, {'publication_year': 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect only one book with publication_year 2020.
        self.assertEqual(len(response.data), 1)

    def test_search_books_by_title(self):
        """Test searching books by title."""
        url = reverse('all books')
        response = self.client.get(url, {'search': 'One'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure 'Book One' appears in the search results.
        titles = [book['title'] for book in response.data]
        self.assertIn('Book One', titles)

    def test_order_books_by_title(self):
        """Test ordering books by title."""
        url = reverse('all books')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the titles are sorted alphabetically.
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_create_book_future_publication_year(self):
        """Test validation for a future publication year."""
        self.client.login(username='testuser', password='testpass')
        url = reverse('Create a book', kwargs={'pk': self.author.pk})
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        response = self.client.post(url, data)
        # Expect a validation error.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for the error message in non_field_errors.
        self.assertIn("publication_year can't be in the future", response.data.get("non_field_errors", []))
