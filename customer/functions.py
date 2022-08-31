import datetime
import numpy


def determine_active_services(services: list):
	to_remove = []
	actives_services = services

	for service in actives_services:
		if service.start_date is None:
			to_remove.append(service)

	for inactive_service in to_remove:
		if inactive_service in actives_services:
			actives_services.remove(inactive_service)

	return actives_services


def calculate_days_difference(start_date: str, end_date: str, businessdays=False) -> int:
	if not businessdays:
		start_date_reworked = datetime.datetime.strptime(start_date, "%Y-%m-%d")
		end_date_reworked = datetime.datetime.strptime(end_date, "%Y-%m-%d")
		delta = end_date_reworked - start_date_reworked
		difference = delta.days
	else:
		difference = numpy.busday_count(begindates=start_date, enddates=end_date)
	return difference


def calculate_free_days_end(services, start_date: str, end_date: str, free_days: int):
	free_days_old = []
	earliest_date = start_date
	for service in services:
		free_days_old.append(0)
		earliest_date = min(earliest_date, service.start_date)
	test_date = datetime.datetime.strptime(earliest_date, "%Y-%m-%d")
	number_of_days = calculate_days_difference(test_date.strftime('%Y-%m-%d'),
											   end_date, businessdays=False)

	for i in range(number_of_days):
		sum = 0
		for service in services:
			if datetime.datetime.strptime(service.start_date, "%Y-%m-%d") <= test_date:
				service.total_free_days = calculate_days_difference(service.start_date,
																	test_date.strftime('%Y-%m-%d'),
																	businessdays=service.workday)
				sum += service.total_free_days

		increased_days = []
		for index, service in enumerate(services):
			if service.total_free_days > free_days_old[index]:
				increased_days.append(service)

		if sum < free_days:
			for increased_day in increased_days:
				increased_day.end_free_days_date = (test_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

		elif sum == free_days:
			break
		else:
			overshoot = sum - free_days
			for i in range(overshoot):
				increased_days[i].total_free_days -= 1
				increased_days[i].end_free_days_date = (test_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
			break

		for index, service in enumerate(services):
			free_days_old[index] = service.total_free_days
		test_date += datetime.timedelta(days=1)


def calculate_discount_days(service, start_date, end_date):
	discounted_days = 0
	if service.discount > 0:
		max_date = max(max(service.discount_start, start_date),
					   max(service.discount_start, service.end_free_days_date))
		if service.discount_end is None:
			discounted_days = calculate_days_difference(max_date,
														min(service.end_date, end_date),
														service.workday)
		else:
			discounted_days = calculate_days_difference(max_date,
														service.discount_end, service.workday)
		if discounted_days < 0:
			discounted_days = 0

	return discounted_days

