import src.customer.functions as functions


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
		self.active_services = functions.determine_active_services(self.active_services)

		for service in self.active_services:
			service.total_days = functions.calculate_days_difference(service.start_date, service.end_date,
																	 businessdays=service.workday)

		total = 0
		for service in self.active_services:
			total += service.total_days
		if total <= int(self.free_days):
			self._price = 0
			return

		if self.free_days != 0:
			functions.calculate_free_days_end(self.active_services, self.start_date, self.end_date, self.free_days)

		for service in self.active_services:
			service.active_date = service.end_free_days_date
			service.paid_days = functions.calculate_days_difference(service.active_date, service.end_date,
																	businessdays=service.workday)
			service.discounted_days = functions.calculate_discount_days(service, self.start_date, self.end_date)

		self._price = round(self.calculate_total_price(self.active_services), 2)

	@staticmethod
	def calculate_total_price(services):
		total = 0
		for service in services:
			total += (service.paid_days - service.discounted_days * service.discount / 100) * service.price
		return total

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

