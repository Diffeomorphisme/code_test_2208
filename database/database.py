import csv
import datetime
from customer import functions


def fetch_customer_data(customer):
	# Fetches the data from a specific customer based on the customerid
	# If there are no customerid matching -> return a dictionary with the keys but no values (None)
	results = {}
	data_fields = []
	customer_data = []
	with open('database/Database.csv', mode='r') as file:
		csv_file = csv.reader(file)
		counter = 0

		for line in csv_file:
			if counter == 0:
				data_fields = line
				counter += 1
			if line[0] == customer:
				# convert text to int, float or None
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
	return results

def check_full_data_validity(customerid: str, start_date: str, end_date: str, customer_data: dict):
	# Check that end date and start date are dates:
	try:
		datetime.datetime.strptime(start_date, "%Y-%m-%d")
	except ValueError:
		return f"Start date not a valid date: {start_date}"
	try:
		datetime.datetime.strptime(end_date, "%Y-%m-%d")
	except ValueError:
		return f"End date not a valid date: {end_date}"

	# Check that end date is later than start date
	if functions.calculate_days_difference(start_date, end_date, True) < 0:
		return f"Start date '{start_date}' is later than end date '{end_date}'"

	# Check that the data retrieved from the DB corresponds to the request
	if customerid != customer_data["customerid"] or customer_data["customerid"] is None:
		return f"Invalid customer ID: '{customerid}'"