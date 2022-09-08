import unittest
from unittest.mock import MagicMock
from src.customer import functions


class TestFunctions(unittest.TestCase):
	def setUp(self) -> None:
		self.start_date = "2019-09-20"
		self.end_date = "2019-10-01"

	def test_determine_active_services(self):
		service_1 = MagicMock()
		service_2 = MagicMock()
		service_1.start_date = self.start_date
		service_2.start_date = None
		self.assertEqual([service_1], functions.determine_active_services([service_1, service_2]))
		self.assertEqual([],functions.determine_active_services([service_2, service_2, service_2]))

	def test_calculate_days_difference(self):
		self.assertEqual(11, functions.calculate_days_difference(self.start_date, self.end_date, businessdays=False))
		self.assertNotEqual(12, functions.calculate_days_difference(self.start_date, self.end_date, businessdays=False))
		self.assertEqual(7, functions.calculate_days_difference(self.start_date, self.end_date, businessdays=True))
		self.assertNotEqual(8, functions.calculate_days_difference(self.start_date, self.end_date, businessdays=True))


if __name__ == "__main__":
	unittest.main()
