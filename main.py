import datetime

import communication
import database
import functions


class Customer():
	# ***Attributes from DB***
	# 'customerid',
	# 'price_A', 'price_B', 'price_C',
	# 'start_A', 'start_B', 'start_C',
	# 'discount_A_percent', 'discount_B_percent', 'discount_C_percent',
	# 'discount_A_start', 'discount_B_start', 'discount_C_start',
	# 'discount_A_end', 'discount_B_end', 'discount_C_end',
	# 'free_days'
	# ***Other attributes***
	# start_date, end_date
	# service_a, service_b, service_c

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
		self.active_services = [self.service_a, self.service_b, self.service_c]

	def calculate_price(self):
		# Find out which services the customer is paying for (ie active)
		self.active_services = functions.determine_active_services(self.active_services)

		# Calculate the total number of days for each active service
		for service in self.active_services:
			service.total_days = functions.calculate_days_difference(service.start_date, service.end_date,
																	 businessdays=service.workday)

		# if the number of all active services days is lower than the number of free days => price is 0
		# End of estimation, no need to go further
		sum = 0
		for service in self.active_services:
			sum += service.total_days
		if (sum) <= int(self.free_days):
			self._price = 0
			return

		# Evaluate the end date of free days for each service
		if self.free_days != 0:
			functions.calculate_free_days_end(self.active_services, self.start_date, self.end_date, self.free_days)

		# Calculate the number of paid days (without the free days) for each service
		# Evaluate the number of days with a discount applied for each service
		for service in self.active_services:
			service.active_date = service.end_free_days_date
			service.paid_days = functions.calculate_days_difference(service.active_date, service.end_date,
																	businessdays=service.workday)
			service.discounted_days = functions.calculate_discount_days(service, self.start_date, self.end_date)

		# Calculate the total price and round it to 2 digits
		self._price = round(functions.calculate_total_price(self.active_services), 2)

	@property
	def price(self):
		return self._price


class Service():
	def __init__(self, price, start_date, end_date, discount, discount_start, discount_end, workday: bool):
		self.price = price
		self.start_date = start_date
		self.active_date = start_date
		self.end_date = end_date
		self.discount = discount
		self.discount_start = discount_start
		self.discount_end = discount_end
		self.workday = workday
		self.total_days = 0
		self.paid_days = 0
		self.total_free_days = 0
		self.discounted_days = 0
		self.end_free_days_date = start_date


def main():
	fields = ["customerid", "start_date", "end_date"]
	# Receive the data from the API call
	incoming_data = communication.receive_data()

	# Do initial data check: right number of fields, fields with the right names
	initial_data_check = functions.check_initial_data_validity(incoming_data, fields)
	if initial_data_check:
		communication.send_data(initial_data_check)
		return

	received_customerid = incoming_data["customerid"]
	received_start_date = incoming_data["start_date"]
	received_end_date = incoming_data["end_date"]

	# Fetch data from the DB
	customer_data = {}
	customer_data = database.fetch_customer_data(received_customerid)

	# Do full data check (customerid is in database, dates in the right format, start date < end date)
	full_data_check = functions.check_full_data_validity(received_customerid,
														 received_start_date,
														 received_end_date,
														 customer_data)
	if full_data_check:
		communication.send_data(full_data_check)
		return

	# Instantiate a new customer based on the data fetched from the DB
	customer = Customer(customer_data_from_db=customer_data,
						start_date=received_start_date,
						end_date=received_end_date)

	customer.calculate_price()

	# Send the data back
	final_price = customer.price
	response = "{"+"price: "+str(final_price)+"}"
	communication.send_data(response)

if __name__ == "__main__":
	main()
