"""
Test that the request check returns:
  - no error when the request is correct
  - an error when the request is incorrect
"""

import unittest
from unittest.mock import MagicMock
from src.request import check_request_fields


def get_function(field):
	dict = {"customerid": "customerid", "start_date": "start_date", "end_date": "end_date"}
	if field in dict.keys():
		return dict[field]


class TestRequest(unittest.TestCase):
	def test_request(self):
		expected_fields = ["customerid", "start_date", "end_date"]
		request = MagicMock()
		request.args.get.side_effect = get_function
		self.assertEqual({}, check_request_fields(expected_fields, request))
		self.assertNotEqual({}, check_request_fields(["something", "something_else"], request))


if __name__ == "__main__":
	unittest.main()
