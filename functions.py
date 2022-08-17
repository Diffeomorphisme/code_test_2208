import csv
import datetime
import numpy


def fetch_customer_data(customer):
	# Fetches the data from a specific customer based on the customerid
	# If there are no customerid matching
	results = {}
	data_fields = []
	customer_data = []
	with open('Database.csv', mode='r') as file:
		csv_file = csv.reader(file)
		counter = 0

		for line in csv_file:
			if counter == 0:
				data_fields = line
				counter += 1
			if line[0] == customer:
				for element in line:
					if element.isdigit():
						customer_data.append(int(element))
					elif element.replace('.', '', 1).isdigit() and element.count('.') < 2:
						customer_data.append(float(element))
					elif element == "None":
						customer_data.append(None)
					else:
						customer_data.append(element)

	if len(customer_data) == len(data_fields):
		for index, field in enumerate(data_fields):
			results[field] = customer_data[index]
	else:
		for index, field in enumerate(data_fields):
			results[field] = None
	print(results)
	return results


def calculate_days_difference(start_date: str, end_date: str, businessdays=False) -> int:
	if not businessdays:
		start_date_reworked = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		end_date_reworked = datetime.datetime.strptime(end_date, "%Y-%m-%d")
		delta = end_date_reworked - start_date_reworked
		difference = delta.days
	else:
		difference = numpy.busday_count(begindates=start_date, enddates=end_date)
	return difference


def calculate_free_days(services, start_date: str, end_date: str, free_days: int):

	number_of_days = calculate_days_difference(start_date, end_date, businessdays=False)
	free_days_old = []
	for service in services:
		free_days_old.append(0)
	test_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")

	for i in range(number_of_days):
		sum = 0
		for service in services:
			if datetime.datetime.strptime(service.start_date, "%Y-%m-%d") < test_date:
				service.total_free_days = calculate_days_difference(max(start_date, service.start_date),
																	test_date.strftime('%Y-%m-%d'),
																	businessdays=service.workday)
				sum += service.total_free_days

		if sum < free_days:
			pass
		elif sum == free_days:
			break
		else:
			overshoot = sum - free_days
			increased_days = []
			for index, service in enumerate(services):
				if service.total_free_days > free_days_old[index]:
					increased_days.append(service)

			for i in range(overshoot):
				print(i)
				increased_days[-1 - i].total_free_days -= 1
			break

		for index, service in enumerate(services):
			free_days_old[index] = service.total_free_days
		test_date += datetime.timedelta(days=1)
		print(test_date)