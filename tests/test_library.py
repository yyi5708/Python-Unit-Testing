import unittest

from unittest.mock import Mock
from library.library import Library

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.db = Mock()
        self.library.api = Mock()

    def test_shutdown(self):
        self.library.shutdown()
        self.library.db.close_db.assert_called()

    def test_is_ebook_true(self):
        # setup test
        self.library.api.get_ebooks = Mock(return_value=[
            {'title': 'Learning Python', 'ebook_count': 5}
        ])
        # run test
        result = self.library.is_ebook("Learning Python")
        # validate test
        self.assertTrue(result)
        self.library.api.get_ebooks.assert_called()

    def test_is_ebook_false(self):
        # setup test
        self.library.api.get_ebooks = Mock(return_value=[])
        # run test
        result = self.library.is_ebook("Unknown Book")
        # validate test
        self.assertFalse(result)

    def test_get_ebooks_count(self):
        # setup test
        self.library.api.get_ebooks = Mock(return_value=[
            {'title': 'Learning Python', 'ebook_count': 3},
            {'title': 'Learning Python', 'ebook_count': 2}
        ])
        # run test
        result = self.library.get_ebooks_count("Learning Python")
        # validate test
        self.assertEqual(5, result)

    def test_is_book_by_author_true(self):
        # setup test
        self.library.api.books_by_author = Mock(return_value=[
            "Learning Python"
        ])
        # run test
        result = self.library.is_book_by_author("Mark Lutz", "Learning Python")
        # validate test
        self.assertTrue(result)

    def test_is_book_by_author_false(self):
        # setup test
        self.library.api.books_by_author = Mock(return_value=[
            "Other Book"
        ])
        # run test
        result = self.library.is_book_by_author("Mark Lutz", "Learning Python")
        # validate test
        self.assertFalse(result)

    def test_get_languages_for_book(self):
        # setup test
        self.library.api.get_book_info = Mock(return_value=[
            {'title': 'Learning Python', 'language': ['English']},
            {'title': 'Learning Python', 'language': ['Spanish']}
        ])
        # run test
        result = self.library.get_languages_for_book("Learning Python")
        # validate test
        self.assertEqual({'English', 'Spanish'}, result)

    def test_register_patron_success(self):
        # setup test
        self.library.db.insert_patron = Mock(return_value=123)
        # run test
        result = self.library.register_patron("John", "Doe", 25, 1)
        # validate test
        self.assertEqual(123, result)
        self.library.db.insert_patron.assert_called()

    def test_register_patron_duplicate(self):
        # setup test
        self.library.db.insert_patron = Mock(return_value=None)
        # run test
        result = self.library.register_patron("John", "Doe", 25, 1)
        # validate test
        self.assertIsNone(result)

    def test_is_patron_registered_true(self):
        # setup test
        mock_patron = Mock()
        mock_patron.member_id = 1
        self.library.db.retrieve_patron = Mock(return_value=mock_patron)
        # run test
        result = self.library.is_patron_registered(mock_patron)
        # validate test
        self.assertTrue(result)

    def test_is_patron_registered_false(self):
        # setup test
        mock_patron = Mock()
        mock_patron.member_id = 1
        self.library.db.retrieve_patron = Mock(return_value=None)
        # run test
        result = self.library.is_patron_registered(mock_patron)
        # validate test
        self.assertFalse(result)

    def test_borrow_book(self):
        # setup test
        mock_patron = Mock()
        mock_patron.borrowed_books = []
        self.library.borrow_book("Python", mock_patron)
        # run test
        mock_patron.add_borrowed_book.assert_called_with("python")
        # validate test
        self.library.db.update_patron.assert_called_with(mock_patron)

    def test_return_borrowed_book(self):
        # setup test
        mock_patron = Mock()
        mock_patron.borrowed_books = ["python"]
        self.library.return_borrowed_book("Python", mock_patron)
        # run test
        mock_patron.return_borrowed_book.assert_called_with("python")
        # validate test
        self.library.db.update_patron.assert_called_with(mock_patron)

    def test_is_book_borrowed_true(self):
        # setup test
        mock_patron = Mock()
        mock_patron.borrowed_books = ["python"]
        # run test
        result = self.library.is_book_borrowed("Python", mock_patron)
        # validate test
        self.assertTrue(result)

    def test_is_book_borrowed_false(self):
        # setup test
        mock_patron = Mock()
        mock_patron.borrowed_books = ["java"]
        # run test
        result = self.library.is_book_borrowed("Python", mock_patron)
        # validate test
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
