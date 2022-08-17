import datetime

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

	def _calculate_free_days_end(self, services):

		free_days_old = []
		earliest_date = self.start_date
		for service in services:
			free_days_old.append(0)
			earliest_date = min(earliest_date, service.start_date)
		test_date = datetime.datetime.strptime(earliest_date, "%Y-%m-%d")
		number_of_days = functions.calculate_days_difference(test_date.strftime('%Y-%m-%d'),
															 self.end_date, businessdays=False)

		for i in range(number_of_days):
			sum = 0
			print(f"test_date: {test_date}")
			for service in services:
				if datetime.datetime.strptime(service.start_date, "%Y-%m-%d") <= test_date:
					service.total_free_days = functions.calculate_days_difference(service.start_date,
																				  test_date.strftime('%Y-%m-%d'),
																				  businessdays=service.workday)
					sum += service.total_free_days
			print(f"sum: {sum}")
			increased_days = []
			for index, service in enumerate(services):
				if service.total_free_days > free_days_old[index]:
					increased_days.append(service)

			if sum < self.free_days:
				print("Blih")
				for increased_day in increased_days:
					increased_day.end_free_days_date = (test_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

			elif sum == self.free_days:
				print("Blah")
				break
			else:
				print("Blouh")
				overshoot = sum - self.free_days
				print(f"overshoot: {overshoot}")
				for i in range(overshoot):
					print(i)
					increased_days[i].total_free_days -= 1
					increased_days[i].end_free_days_date = (test_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
				break

			for index, service in enumerate(services):
				free_days_old[index] = service.total_free_days
			test_date += datetime.timedelta(days=1)

	def _calculate_discount_days(self, services):
		for service in services:
			if service.discount > 0:
				max_date = max(max(service.discount_start, self.start_date),
							   max(service.discount_start, service.end_free_days_date))
				if service.discount_end is None:
					service.discounted_days = functions.calculate_days_difference(max_date,
																				  min(service.end_date, self.end_date)
																				  , service.workday)
				else:
					service.discounted_days = functions.calculate_days_difference(max_date,
																				  service.discount_end, service.workday)
				if service.discounted_days < 0:
					service.discounted_days = 0

	def _determine_active_services(self):
		active_services = [self.service_a, self.service_b, self.service_c]
		to_remove = []

		for service in active_services:
			if service.start_date is None:
				to_remove.append(service)

		for inactive_service in to_remove:
			if inactive_service in active_services:
				active_services.remove(inactive_service)

		return active_services

	def _calculate_price(self, active_services):
		price = 0
		for service in active_services:
			price += (service.discounted_days * (1 - service.discount / 100)
					  + (service.active_days - service.discounted_days)) * service.price
		return price

	def calculate_price(self) -> float:
		# Find out which services the customer is paying for
		# and calculate the total number of days for each service
		active_services = self._determine_active_services()
		for service in active_services:
			service.total_days = functions.calculate_days_difference(service.start_date, service.end_date,
																	 businessdays=service.workday)

		# if the collective number of days is lower than the number of free days => price is 0
		if (self.service_a.total_days + self.service_b.total_days + self.service_c.total_days) < int(self.free_days):
			self._price = 0
			return self._price

		# Evaluate the end date of free days for each service
		if self.free_days != 0:
			self._calculate_free_days_end(active_services)

		for service in active_services:
			service.active_date = service.end_free_days_date
			service.active_days = functions.calculate_days_difference(service.active_date, service.end_date,
																	  businessdays=service.workday)
			print(service.active_days)

		# Evaluate the number of days with a discount applied for each service
		self._calculate_discount_days(active_services)
		for service in active_services:
			print(f"Discounted days: {service.discounted_days} - "
				  f"Total active days {service.active_days}")

		self._price = round(self._calculate_price(active_services), 2)
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
		self.active_days = 0
		self.total_free_days = 0
		self.discounted_days = 0
		self.end_free_days_date = start_date


def main():
	received_customerid = "Customer X"
	received_start_date = "2018-09-20"
	received_end_date = "2018-10-01"
	# Check that end date is later than start date

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

	price = customer.calculate_price()
	print(price)

if __name__ == "__main__":
	main()
