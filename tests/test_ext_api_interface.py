import os
import unittest
from library import ext_api_interface
from unittest.mock import Mock, MagicMock
import requests
import json

class TestExtApiInterface(unittest.TestCase):
    def setUp(self):
        self.api = ext_api_interface.Books_API()
        self.book = "Learning Python"
        self.rootPath = './'
        if os.getcwd().__contains__('tests'):
            self.rootPath = '../'
        with open(self.rootPath + 'tests_data/ebooks.json', 'r') as f:
            self.books_data = json.loads(f.read())
        with open(self.rootPath + 'tests_data/openlib_sample_data.json', 'r') as f:
            self.json_data = json.loads(f.read())

    def test_is_book_available_connection_error(self):
        # setup test
        ext_api_interface.requests.get = Mock(side_effect=requests.ConnectionError)
        # run test
        result = self.api.is_book_available('bogus book')
        # validate test
        self.assertFalse(result)
        ext_api_interface.requests.get.assert_called()    

    def test_is_book_available(self):
        #setup test
        response_mock = MagicMock()
        response_mock.json = Mock(return_value=self.json_data)
        response_mock.raise_for_status = Mock(return_value=None)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        # run test
        result = self.api.is_book_available(self.book)
        # validate test
        self.assertTrue(result)
        ext_api_interface.requests.get.assert_called()
        response_mock.raise_for_status.assert_called()
        response_mock.json.assert_called()

    def test_books_by_author(self):
        #setup test
        response_mock = MagicMock()
        json = {'docs': [{'title': 'Learning Python'}]}
        response_mock.json = Mock(return_value=json)
        response_mock.raise_for_status = Mock(return_value=None)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        # run test
        result = self.api.books_by_author('Mark Lutz')
        # validate test
        self.assertEqual(['Learning Python'], result)
        ext_api_interface.requests.get.assert_called()  
        response_mock.raise_for_status.assert_called()
        response_mock.json.assert_called()
        
    def test_books_by_author_error(self):
        response_mock = self.__make_mock_response(None)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        self.assertEqual([], self.api.books_by_author('Mark Lutzss'))
        ext_api_interface.requests.get.assert_called()
        self.__assert_mock_called(response_mock)

    def test_get_book_info(self):
        json = {'docs': [{'title': 'Learning Python', 'first_publish_year': 1999, 'language': ['English']}]}
        response_mock = self.__make_mock_response(json)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        result = self.api.get_book_info('Learning Python')
        self.assertEqual([{'title': 'Learning Python', 'publish_year': 1999, 'language': ['English']}], result)
        ext_api_interface.requests.get.assert_called()
        self.__assert_mock_called(response_mock)
        
    def test_get_book_info_error(self):
        response_mock = self.__make_mock_response(None)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        self.assertEqual([], self.api.get_book_info('Learning Python'))
        ext_api_interface.requests.get.assert_called()
        self.__assert_mock_called(response_mock)

    def test_get_ebooks(self):
        # setup test
        response_mock = MagicMock()
        response_mock.json = Mock(return_value=self.json_data)
        response_mock.raise_for_status = Mock(return_value=None)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        # run test
        result = self.api.get_ebooks(self.book)
        # validate test
        self.assertEqual(self.books_data, result)
        ext_api_interface.requests.get.assert_called()
        response_mock.raise_for_status.assert_called()
        response_mock.json.assert_called()

    def test_get_ebooks_2(self):
        # setup test
        response_mock = self.__make_mock_response(self.json_data)
        ext_api_interface.requests.get = Mock(return_value=response_mock)
        # run test
        result = self.api.get_ebooks(self.book)
        # validate test
        self.assertEqual(self.books_data, result)
        ext_api_interface.requests.get.assert_called()
        self.__assert_mock_called(response_mock)

    def __make_mock_response(self, json_data) -> MagicMock:
        response_mock = MagicMock()
        response_mock.json = Mock(return_value=json_data)
        response_mock.raise_for_status = Mock(return_value=None)
        return response_mock

    def __assert_mock_called(self, response_mock):
        response_mock.raise_for_status.assert_called()
        response_mock.json.assert_called()