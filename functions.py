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
				customer_data = line

	if len(customer_data) == len(data_fields):
		for index, field in enumerate(data_fields):
			results[field] = customer_data[index]
	else:
		for index, field in enumerate(data_fields):
			results[field] = "None"
	return results


def calculate_days_difference(start_date, end_date, businessdays=False) -> int:
	if not businessdays:
		start_date_reworked = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		end_date_reworked = datetime.datetime.strptime(end_date, "%Y-%m-%d")
		delta = end_date_reworked - start_date_reworked
		difference = delta.days
	else:
		difference = numpy.busday_count(begindates=start_date, enddates=end_date)
	return difference