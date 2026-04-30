"""
Filename: library_db_interface.py
Description: module used for interacting with the local database
"""

import os

from typing import Optional
from library.patron import Patron
from tinydb import TinyDB, Query

class Library_DB:
    """Class for the local library database."""

    DATABASE_FILE = 'db.json'

    def __init__(self, start_clean=False):
        """Constructor for the Library_DB object."""

        if start_clean and os.path.exists(self.DATABASE_FILE):
            os.remove(self.DATABASE_FILE)
        self.db = TinyDB(self.DATABASE_FILE)

    def insert_patron(self, patron: Patron) -> Optional[int]:
        """Inserts a Patron into the database.
        :param patron: the Patron object
        :returns: the Patron's ID or None
        """

        if not patron:
            return None
        if self.retrieve_patron(patron.member_id): # patron already in db
            return None
        data = self.convert_patron_to_db_format(patron)
        return self.db.insert(data)

    def get_patron_count(self):
        """Gets the number of Patrons in the database.
        :returns: the total number of Patrons in the DB
        """

        results = self.db.all()
        return len(results)

    def get_all_patrons(self):
        """Gets a list of all the Patrons in the database.
        :returns: a list of all the Patrons
        """

        results = self.db.all()
        return results

    def update_patron(self, patron) -> bool:
        """Updates a Patron's data in the DB.
        :param patron: the new Patron object to be updated
        :returns: False if the patron parameter is not the correct object
        """

        if not patron:
            return False
        query = Query()
        data = self.convert_patron_to_db_format(patron)
        updated_ids = self.db.update(data, query.memberID == patron.member_id)
        return len(updated_ids) > 0

    def retrieve_patron(self, memberID):
        """Gets a Patron from the database.
        :param memberID: the ID for the Patron to retrieve
        :returns: the Patron with the given ID, or None
        """

        query = Query()
        # assuming no two people in the db have the same memberID
        results = self.db.search(query.memberID == memberID)
        if results:
            return Patron(results[0]['fname'], results[0]['lname'], results[0]['age'],
            results[0]['memberID'])
        return None

    def close_db(self):
        """Closes the database."""

        self.db.close()

    def convert_patron_to_db_format(self, patron):
        """Converts the Patron object to a dictionary format.
        :param patron: the Patron python object
        :returns: a dictionary of the Patron's data
        """
        
        return {'fname': patron.fname, 'lname': patron.lname, 'age': patron.age, 'memberID': patron.member_id,
        'borrowed_books': patron.borrowed_books}
