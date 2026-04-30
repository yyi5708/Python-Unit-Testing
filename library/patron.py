"""
Filename: patron.py
Description: Patron class for SWEN-352 mocking activity.
"""

import re

class InvalidNameException(Exception):
    """Custom Exception for an invalid name."""

    pass

class Patron:
    """Patron class used to represent a user for a library."""

    def __init__(self, fname: str, lname: str, age: int, memberID: str):
        """Constructor for the Patron class.
        :param fname: the first name for the Patron
        :param lname: the last name for the Patron
        :param age: the age of the Patron
        :param memberID: the ID for the Patron in the library's system
        """

        if re.search(r'\d', fname) or re.search(r'\d', lname):
            raise InvalidNameException("Name should not contain numbers")
        self.__fname = fname
        self.__lname = lname
        self.__age = age
        self.__member_id = memberID
        self.__borrowed_books = []

    @property
    def fname(self) -> str:
        """Getter for the first name of the Patron.
        :returns: the first name of the Patron
        """

        return self.__fname

    @property
    def lname(self) -> str:
        """Getter for the last name of the Patron.
        :returns: the last name of the Patron
        """

        return self.__lname

    @property
    def age(self) -> int:
        """Getter for the age of the Patron.
        :returns: the age of the Patron
        """

        return self.__age

    @property
    def member_id(self) -> str:
        """Getter for the memberID of the Patron.
        :returns: the memberID of the Patron
        """

        return self.__member_id

    @property
    def borrowed_books(self) -> list[str]:
        """Gets the list of borrowed books for the Patron.
        :returns: the list of borrowed books
        """

        return self.__borrowed_books.copy()

    def with_age(self, age: int) -> 'Patron':
        """Creates a new Patron object with the same attributes as the current Patron, but with a different age."""

        return Patron(self.fname, self.lname, age, self.member_id)

    def add_borrowed_book(self, book):
        """Adds a book to the list of borrowed books for the Patron
        :param book: the title of the book
        """

        book = book.lower()
        if book in self.__borrowed_books:
            return
        self.__borrowed_books.append(book)

    def return_borrowed_book(self, book):
        """Removes the borrowed book from the list of books currently checked out.
        :param book: the title of the book to remove
        """

        book = book.lower()
        if book in self.__borrowed_books:
            self.__borrowed_books.remove(book)

    def __eq__(self, other):
        """Equals function for the Patron class."""

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Not-equal function for the Patron class."""

        return not self.__eq__(other)

    def __repr__(self):
        return f"<Patron '{self.member_id}' [{self.fname} {self.lname} @ {self.age}]>"
