import csv


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
	return results
