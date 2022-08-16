import functions


class Customer():
	# DATA Fields from DB:
	# 'customerid',
	# 'price_A', 'price_B', 'price_C',
	# 'start_A', 'start_B', 'start_C',
	# 'discount_A_percent', 'discount_B_percent', 'discount_C_percent',
	# 'discount_A_start', 'discount_B_start', 'discount_C_start',
	# 'discount_A_end', 'discount_B_end', 'discount_C_end',
	# 'free_days'

	def __init__(self, customer_data_from_db: dict, start_date: str, end_date: str):
		for key, value in customer_data_from_db.items():
			setattr(self, key, value)
		self._price = 0
		self.start_date = start_date
		self.end_date = end_date
		self._days_A = 0
		self._days_B = 0
		self._days_C = 0

	@property
	def price(self):
		print(functions.calculate_days_difference(self.start_date, self.end_date, businessdays=True))
		if self.start_A != "None":
			self._days_A = functions.calculate_days_difference(self.start_A, self.end_date, businessdays=True)
		if self.start_B != "None":
			self._days_B = functions.calculate_days_difference(self.start_B, self.end_date, businessdays=True)
		if self.start_C != "None":
			self._days_C = functions.calculate_days_difference(self.start_C, self.end_date, businessdays=False)

		if (self._days_A + self._days_B + self._days_C) < int(self.free_days):
			self._price = 0
			return self._price

		self._price = 10000
		return self._price


def main():
	received_customerid = "Customer X"
	received_start_date = "2018-01-01"
	received_end_date = "2019-10-01"

	# Fetch data from the DB
	customer_data = {}
	customer_data = functions.fetch_customer_data(received_customerid)

	# Check that the data retrieved from the DB corresponds to the request
	if received_customerid != customer_data["customerid"]:
		print("Problem in fetching the customer data")

	# Instantiate a new customer based on the data fetched from the DB
	customer = Customer(customer_data_from_db=customer_data,
						start_date=received_start_date,
						end_date=received_end_date)

	print(customer.price)


if __name__ == "__main__":
	main()
