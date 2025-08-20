This repository contains Python scripts to collect and process fruit and vegetable prices from the Mexican SNIIM system.

- Script 1: sniim_scraping.py
  - Performs web scraping from the SNIIM website to collect historical market prices for fruits and vegetables.
  - Automatically handles pagination and large date ranges.
  - Saves the results as CSV files organized by product and time range.
  - Allows setting the search period and the price format (per kilogram or commercial presentation).
  - Splits long queries into chunks of up to 5 years to prevent server errors.

- Script 2: odepa_processing.py
  - Processes a CSV file containing food prices.
  - Converts price columns to numeric and parses the date column.
  - Groups data by month and region and calculates average prices per product.
  - Saves the results as Excel files with multiple sheets, one per product.

- Requirements
  - Python 3.8 or higher
  - pandas
  - numpy
  - matplotlib
  - BeautifulSoup4 (for sniim_scraping.py)
