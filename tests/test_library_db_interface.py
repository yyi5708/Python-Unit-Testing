import unittest

from unittest.mock import Mock, call
from library import library_db_interface
from library.patron import Patron

class TestLibraryDBInterface(unittest.TestCase):

    def setUp(self):
        self.db_interface = library_db_interface.Library_DB()
        self.db_interface.db.close()
        self.db_interface.db = Mock()

    def tearDown(self):
        self.db_interface.close_db()
        self.db_interface = None

    def test_insert_patron_success(self):
        # setup test
        patron_mock = Mock()
        patron_mock.member_id = "1"
        data = {
            "fname": "John",
            "lname": "Doe",
            "age": 30,
            "memberID": "1",
            "borrowed_books": []
        }
        self.db_interface.retrieve_patron = Mock(return_value=None)
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        self.db_interface.db.insert = Mock(return_value=1)
        # run test
        result = self.db_interface.insert_patron(patron_mock)
        # validate test
        self.assertEqual(result, 1)
        self.db_interface.db.insert.assert_called_with(data)

    def test_insert_patron_none(self):
        # setup test: N/A
        # run test
        result = self.db_interface.insert_patron(None)
        # validate test
        self.assertIsNone(result)

    def test_insert_patron_duplicate(self):
        # setup test
        patron_mock = Mock()
        patron_mock.member_id = "1"
        self.db_interface.retrieve_patron = Mock(return_value=patron_mock)
        # run test
        result = self.db_interface.insert_patron(patron_mock)
        # validate test
        self.assertIsNone(result)

    def test_get_patron_count_empty(self):
        # setup test
        self.db_interface.db.all = Mock(return_value=[])
        # run test
        count = self.db_interface.get_patron_count()
        # validate test
        self.assertEqual(count, 0)

    def test_get_patron_count_multiple(self):
        # setup test
        self.db_interface.db.all = Mock(return_value=[{}, {}])
        # run test
        count = self.db_interface.get_patron_count()
        # validate test
        self.assertEqual(count, 2)

    def test_get_all_patrons_empty(self):
        # setup test
        self.db_interface.db.all = Mock(return_value=[])
        # run test
        result = self.db_interface.get_all_patrons()
        # validate test
        self.assertEqual(result, [])

    def test_get_all_patrons_success(self):
        # setup test
        data = [
            {"fname": "John",
            "lname": "Doe",
            "age": 30,
            "memberID": "1",
            "borrowed_books": []},
            {"fname": "Jane",
            "lname": "Smith",
            "age": 30,
            "memberID": "2",
            "borrowed_books": []}
        ]
        self.db_interface.db.all = Mock(return_value=data)
        # run test
        result = self.db_interface.get_all_patrons()
        # validate test
        self.assertEqual(result, data)

    def test_retrieve_patron_success(self):
        # setup test
        data = [{
            "fname": "John",
            "lname": "Doe",
            "age": 30,
            "memberID": "1",
            "borrowed_books": []
        }]
        self.db_interface.db.search = Mock(return_value=data)
        # run test
        result = self.db_interface.retrieve_patron("1")
        # validate test
        self.assertIsInstance(result, Patron)

    def test_retrieve_patron_not_found(self):
        # setup test
        self.db_interface.db.search = Mock(return_value=[])
        # run test
        result = self.db_interface.retrieve_patron("100")
        # validate test
        self.assertIsNone(result)

    def test_update_patron_success(self):
        # setup test
        patron_mock = Mock()
        patron_mock.member_id = "1"
        data = {
            "fname": "John",
            "lname": "Doe",
            "age": 100,
            "memberID": "1",
            "borrowed_books": []
        }
        self.db_interface.convert_patron_to_db_format = Mock(return_value=data)
        db_update_mock = Mock(return_value=[1])
        self.db_interface.db.update = db_update_mock
        # run test
        result = self.db_interface.update_patron(patron_mock)
        # validate test
        self.assertTrue(result)
        db_update_mock.assert_called()

    def test_update_patron_none(self):
        # setup test: N/A
        # run test
        result = self.db_interface.update_patron(None)
        # validate test
        self.assertFalse(result)

    def test_convert_patron_to_db_format(self):
        # setup test
        patron = Patron("John", "Doe", 30, "1")
        # run test
        result = self.db_interface.convert_patron_to_db_format(patron)
        # validate test
        expected = {
            "fname": "John",
            "lname": "Doe",
            "age": 30,
            "memberID": "1",
            "borrowed_books": []
        }
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
