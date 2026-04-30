"""
Filename: ext_api_interface.py
Description: module used for interacting with a web service
"""

import requests

# Global constant for the REST API.
SEARCH_API_URL = "http://openlibrary.org/search.json"

class Books_API:
    """Class used for interacting with the OpenLibrary API."""

    def is_book_available(self, book_title: str):
        """Determines if a given book is available to borrow.
        :param book_title: the title of the book
        :returns: True if available, False if not
        """

        json_data = self.__make_request({'q': book_title})
        if json_data and len(json_data['docs']) >= 1:
            return True
        return False

    def books_by_author(self, author: str):
        """Gets all the books written by a given author.
        :param author: the name of the author
        :returns: the titles of all the books in a list form
        """

        json_data = self.__make_request({'author': author})
        if not json_data:
            return []
        books = []
        for book in json_data['docs']:
            books.append(book['title'])
        return books

    def get_book_info(self, book_title: str):
        """Gets the information for a given book.
        :param book_title: the title of the book
        :returns: a list of dictionaries with book data
        """

        json_data = self.__make_request({'q': book_title.lower()})
        if not json_data:
            return []
        books_info = []
        for book in json_data['docs']:
            info = {'title': book['title']}
            if 'first_publish_year' in book:
                info.update({'publish_year': book['first_publish_year']})
            if 'language' in book:
                info.update({'language': book['language']})
            books_info.append(info)
        return books_info

    def get_ebooks(self, book_title: str):
        """Gets the ebooks for a given book.
        :param book_title: the title of the book
        :returns: data about the ebooks
        """

        json_data = self.__make_request({'q': book_title.lower()})
        if not json_data:
            return []
        ebooks = []
        for book in json_data['docs']:
            if book['edition_count'] >= 1:
                ebooks.append({'title': book['title'], 'ebook_count': book['edition_count']})
        return ebooks

    def gather_test_data(self, query_params: dict[str,str]):
        """
        Expose the raw query to help generate test data.
        :param query_params:
        :return:
        """

        return self.__make_request(query_params)

    def __make_request(self, query_params: dict[str,str]):
        """Makes a HTTP request to the given URL.
        :param query_params: the HTTP query parameters
        :returns: the JSON body of the request, None if non 200 status code or ConnectionError
        """

        try:
            response = requests.get(SEARCH_API_URL, params=query_params)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError:
            return None
