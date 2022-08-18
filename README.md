**Code test - Pricing calculator**
============

**Background**
--------

Look at _Instructions.md_ file for the initial instructions, background, user story, etc.

**What'd I do?**
--------

This program does the following:
- Check the input from the API call (entries all present, dates making sense, etc)
- Reach out to the database (here represented by a .csv file) and fetch the data. 
- Make sure the data request exists in the database
- Instantiate a customer class with attributes from the data fetched from the database
- Instantiate service classes with attributes from the data fetched from the database for each service
- Calculate the total price. This is done in several steps:
  - Evaluate which services are active
  - Evaluate the total number of days for each service (including outside the period)
  - Evaluate the number of free days for each service (including outside the period)
  - From this, evaluate the number of paid days (including discounted days) for the period for each service
  - Evaluate the number of discounted days during the period for each service
  - Subtract (the discounted days * the discount) to the paid days and multiply the result <br />
    with the price for each service
  - Add the price for all services => $$$ here is the total price $$$


**API**
--------

- uri: /get-price
- data fields
    - customerid
    - start_date: YYYY-MM-DD
    - end_date: YYYY-MM-DD
    - No private key in place, but one might be needed
- response
    - error -> Error: Text of the error
    - no error -> price: value of the price


**My questions**
--------
Some things are a bit uncertain at this point, and I had to make assumptions:
- _Global_ 
    - I have considered that the free days had to be distributed among all services from a stock of days
    - (60 days to 3 services become 20, 20, 20 or something like 18, 18, 24) 
    - "global"  could mean that the days are calendar days, and not service days 
    - (this would have made my life much easier)
    - I would have tried to clarify this before continuing further
  

- _Start and end of service_
    - As of now, services do not seem to have an end date.
        - I kept it that way, but one can consider that a customer could stop using a service while still using another
        - That would lead to a few changes :) I would have tried to clarify this before continuing further
    - All dates used in the test are excluding end dates when calculating durations.
        - This is true for the duration of the services (last day excluded)
        - This is also true for the discounts
        - This can be changed, though :)

  
- _Storage of data_
    - I have considered that the data needed for the price estimation was stored in a database <br /> 
      that the API is accessing
    - I did not work on a specific database structure and considered that 
        - all data is stored in a single table
        - the customerid is the key of the table
        - if one were to add a new service (say Service D), new columns would have to be entered in the database <br /> 
          and a minimal amount of code would be changed 



**Technologies**
--------

Python 3
