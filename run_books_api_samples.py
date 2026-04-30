"""
Filename: run_books_api_samples.py
Description: A simple script to drive the Ext API component.
"""

from library.ext_api_interface import Books_API

def main():
    """
    A simple script to exercise the BookService component.
    """

    book_svc = Books_API()
    show_python_ebooks(book_svc)
    print()
    show_python_books_in_german(book_svc)
    print()
    show_books_by_kathysierra(book_svc)

def show_python_ebooks(book_svc: Books_API):
    python_books = book_svc.get_ebooks('Python')
    print(f"There are {len(python_books)} Python books in the collection.")
    for book in python_books:
        print(book)

def show_python_books_in_german(book_svc: Books_API):
    python_books = book_svc.get_book_info('Python')
    german_books = [book for book in python_books if ('ger' in book.get('language', []))]
    print(f"There are {len(german_books)} Python books in German.")
    for book in german_books:
        print(book)

def show_books_by_kathysierra(book_svc: Books_API):
    kathys_books: list[str] = book_svc.books_by_author('Kathy Sierra')
    print(f"There are {len(kathys_books)} books written by Kathy Sierra.")
    for book in kathys_books:
        print(book)

if __name__ == "__main__":
    main()
