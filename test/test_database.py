import unittest
from src.database import database


class TestDatabase(unittest.TestCase):

	def setUp(self):
		self.customer_id = "Customer X"
		self.start_date = "2019-09-20"
		self.end_date = "2019-10-01"
		self.customer_data = {"customerid": "Customer X", "price_A": 0.2, "price_B": 0.24, "price_C": 0.4,
							   "discount_A_percent": 0, "discount_B_percent": 0, "discount_C_percent": 20,
							   "discount_A_start": None, "discount_B_start": None, "discount_C_start": "2019-09-22",
							   "discount_A_end": None, "discount_B_end": None, "discount_C_end": "2019-09-24",
							   "start_A": "2019-09-20", "start_B": None, "start_C": "2019-09-20", "free_days": 0}
		self.wrong_customer_id = "CustomerX"
		self.wrong_start_date = self.end_date
		self.wrong_end_date = self.start_date

	@unittest.skip("Test requires changing the csv address")
	def test_fetch_customer_data(self):
		self.assertEqual(database.fetch_customer_data(self.customer_id), self.customer_data)

	def test_check_full_data_validity(self):
		self.assertIsNone(database.check_full_data_validity(self.customer_id, self.start_date,
														   self.end_date, self.customer_data),
						  									msg="Should return None in normal case")
		self.assertIsNotNone(database.check_full_data_validity(self.wrong_customer_id, self.start_date,
														   self.end_date, self.customer_data), msg="Should ")
		self.assertIsNotNone(database.check_full_data_validity(self.customer_id, self.wrong_start_date,
															   self.wrong_end_date, self.customer_data))



if __name__ == "__main__":
	unittest.main()