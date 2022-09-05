def check_request_fields(expected_fields, request):
	"""Perform a check that incoming data has the espected fields"""
	response = {}

	# Check request is correct
	for field in expected_fields:
		if request.args.get(field) is None:
			if "Error" not in response.keys():
				response["Error"] = f"Invalid field, expected: '{field}'"
			else:
				response["Error"] += f", '{field}'"

	return response
