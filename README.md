**Code test - Pricing calculator**
============

**Background**
--------

Look at Instructions files for the initial instructions, background, user story, etc.

**What'd I do?**
--------

This program does the following:
- Check the input from the API call (entries all present, dates making sense, etc)
- Reach out to the database (here represented by a .csv file) and fetch the data. 
- Make sure the data request exists in the database
- Instantiate a customer class with attributes from the data fetched from the database
- Instantiate service classes with attributes from the data fetched from the database for each service
- Calculate the total price. This is done in the following steps:
  - Evaluate which services are active in the period
  - Evaluate the total number of days for each service (including outside the period)
  - Evaluate the number of free days for each service (including outside the period)
  - This gives the number of non-free days (including discounted days) for the period for each service
  - From this, evaluate the number of non-free days for the period for each service
  - Evaluate the number of discounted days during the period for each service
  - Subtract (the discounted days * the discount) to the non-free days and multiply the result with the price for each service
  - Add the price for all services => $$$ here is the total price $$$


**My questions**
--------
Some things are a bit uncertain at this point and I had to make assumptions:
- _Global_ 
    - I have considered that the free days had to be distributed among all services from a stock of days
    - (60 days to 3 services become 20, 20, 20) 
    - "global"  could mean that the days are calendar days, and not service days 
    - (this would have made my life much easier)
  

- _Start and end of service_
    - As of now, services do not seem to have an end date.
    - I kept it that way, one could consider that a customer could stop using a service while still using another
    - That would lead to a few changes :)




**Technologies**
--------

Python 3
