import datetime

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
		self.service_a = Service(self.price_A, self.start_A, self.end_date,
								 self.discount_A_percent, self.discount_A_start, self.discount_A_end, True)
		self.service_b = Service(self.price_B, self.start_B, self.end_date,
								 self.discount_B_percent, self.discount_B_start, self.discount_B_end, True)
		self.service_c = Service(self.price_C, self.start_C, self.end_date,
								 self.discount_C_percent, self.discount_C_start, self.discount_C_end, False)
		self._days_A = 0
		self._days_B = 0
		self._days_C = 0

	def _calculate_free_days(self, services):
		test_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
		number_of_days = functions.calculate_days_difference(self.start_date, self.end_date, businessdays=False)
		for i in range(number_of_days):
			sum = 0
			for service in services:
				if datetime.datetime.strptime(service.start_date, "%Y-%m-%d") < test_date:
					service.free_days = functions.calculate_days_difference(max(self.start_date, service.start_date),
																			test_date.strftime('%Y-%m-%d'),
																			businessdays=service.workday)
					sum += service.free_days
			if sum == self.free_days:
				break
			elif sum == self.free_days + 1:
				self.service_c.free_days -= 1
			elif sum == self.free_days + 2:
				self.service_b.free_days -= 1
				self.service_c.free_days -= 1

			test_date += datetime.timedelta(days=1)
		print(f"Total days: {self.service_a.days} - Free days {self.service_a.free_days}")
		print(f"Total days: {self.service_b.days} - Free days {self.service_b.free_days}")
		print(f"Total days: {self.service_c.days} - Free days {self.service_c.free_days}")

	@property
	def price(self):
		active_services = [self.service_a, self.service_b, self.service_c]
		to_remove = []

		for service in active_services:
			if service.start_date == "None":
				to_remove.append(service)
			else:
				service.days = functions.calculate_days_difference(service.start_date, service.end_date,
																   businessdays=service.workday)

		for inactive_service in to_remove:
			if inactive_service in active_services:
				active_services.remove(inactive_service)

		if (self.service_a.days + self.service_b.days + self.service_c.days) < int(self.free_days):
			self._price = 0
			return self._price

		if self.free_days != 0:
			self._calculate_free_days(active_services)


		self._price = 10000
		return self._price


class Service():
	def __init__(self, price, start_date, end_date, discount, discount_start, discount_end, workday: bool):
		self.price = price
		self.start_date = start_date
		self.end_date = end_date
		self.discount = discount
		self.discount_start = discount_start
		self.discount_end = discount_end
		self.workday = workday
		self.days = 0
		self.free_days = 0


def main():
	received_customerid = "Customer Y"
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
