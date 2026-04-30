import unittest

from library import patron

PATRON_FIRST_NAME = 'Fred'
PATRON_LAST_NAME = 'Cartz'
PATRON_AGE = 60
PATRON_MEMBER_ID = '1234'
PATRON_REPR = "<Patron '1234' [Fred Cartz @ 60]>"

class TestPatron(unittest.TestCase):

    def setUp(self):
        self.pat = patron.Patron(PATRON_FIRST_NAME, PATRON_LAST_NAME, PATRON_AGE, PATRON_MEMBER_ID)

    def test_valid_name(self):
        self.assertTrue(isinstance(self.pat, patron.Patron))
        self.assertEqual(PATRON_FIRST_NAME, self.pat.fname, "Wrong first name ")
        self.assertEqual(PATRON_LAST_NAME, self.pat.lname, "Wrong last name ")
        self.assertEqual(PATRON_AGE, self.pat.age, "Wrong age ")
        self.assertEqual(PATRON_MEMBER_ID, self.pat.member_id, "Wrong member ID ")

    def test_invalid_name(self):
        self.assertRaises(patron.InvalidNameException, patron.Patron, '1fname', '1lname', '20', '1234')

    def test_with_age(self):
        patron_with_age = self.pat.with_age(21)
        self.assertEqual(21, patron_with_age.age)

    def test_add_borrowed_book(self):
        self.assertEqual([], self.pat.borrowed_books)
        self.pat.add_borrowed_book('book1')
        self.assertEqual(['book1'], self.pat.borrowed_books)

    def test_add_borrowed_book_already_contained(self):
        self.pat.add_borrowed_book('book1')
        self.pat.add_borrowed_book('book1') # add the same book twice
        self.assertEqual(['book1'], self.pat.borrowed_books)

    def test_return_borrowed_book_contained(self):
        self.pat.add_borrowed_book('book1')
        self.pat.return_borrowed_book('book1')
        self.assertEqual([], self.pat.borrowed_books)

    def test_return_borrowed_book_not_contained(self):
        self.pat.add_borrowed_book('book1')
        self.pat.return_borrowed_book('book2')
        self.assertEqual(['book1'], self.pat.borrowed_books)

    def test_equals(self):
        patron2 = patron.Patron(PATRON_FIRST_NAME, PATRON_LAST_NAME, PATRON_AGE, PATRON_MEMBER_ID)
        self.assertEqual(self.pat, patron2)

    def test_not_equals(self):
        patron2 = patron.Patron(PATRON_FIRST_NAME, PATRON_LAST_NAME, 21, PATRON_MEMBER_ID)
        self.assertNotEqual(self.pat, patron2)

    def test_repr(self):
        self.assertEqual(self.pat.__repr__(), PATRON_REPR)
