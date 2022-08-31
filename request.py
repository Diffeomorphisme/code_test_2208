def check_request_fields(expected_fields, request):
	response = {}

	# Check request is correct
	for field in expected_fields:
		if request.args.get(field) is None:
			if "Error" not in response.keys():
				response["Error"] = f"Invalid field, expected: '{field}'"
			else:
				response["Error"] += f", '{field}'"

	return response
