from flask import Flask, request, jsonify
import src.database.database as database
import config
from src.customer.customer import Customer
from request import check_request_fields


app = Flask("API")


@app.route('/get-price', methods=['GET'])
def main():
	# Check all fields are good
	expected_fields = config.expected_fields
	response = check_request_fields(expected_fields, request)

	if "Error" in response.keys():
		return jsonify(response)

	received_customer_id = request.args.get(expected_fields[0])
	received_start_date = request.args.get(expected_fields[1])
	received_end_date = request.args.get(expected_fields[2])

	# Fetch data from the DB
	customer_data = database.fetch_customer_data(received_customer_id)

	# Do full data check (customerid is in database, dates in the right format, start date < end date)
	full_data_check = database.check_full_data_validity(received_customer_id,
														received_start_date,
														received_end_date,
														customer_data)
	if full_data_check:
		response["Error"] = full_data_check
		return jsonify(response)

	# Instantiate a new customer based on the data fetched from the DB
	customer = Customer(customer_data_from_db=customer_data,
						start_date=received_start_date,
						end_date=received_end_date)

	# Calculate the price
	customer.calculate_price()
	final_price = customer.price

	# Answer the GET request
	response["price"] = final_price
	return jsonify(response)


if __name__ == '__main__':
	app.run(debug=True, host="0.0.0.0")


