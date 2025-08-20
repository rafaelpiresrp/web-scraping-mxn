This repository contains Python scripts to collect and process fruit and vegetable prices from the Mexican SNIIM system.

- Script 1: scraping.py
  - Performs web scraping from the SNIIM website to collect historical market prices for fruits and vegetables.
  - Automatically handles pagination and large date ranges.
  - Saves the results as CSV files organized by product and time range.
  - Allows setting the search period and the price format (per kilogram or commercial presentation).
  - Splits long queries into chunks of up to 5 years to prevent server errors.
  - 
- Script 2: managing_data.py
  - Reads the CSV files downloaded by the scraping script.
  - Cleans the data, handles encoding and removes unnecessary rows.
  - Converts columns to proper types (dates, numeric) and normalizes product names with accents.
  - Filters for selected regions and products of interest.
  - Calculates biweekly averages, groups by product, origin, month, and half-month.
  - Pivots tables to have regions as columns and calculates biweekly price variations.
  - Saves results in multiple Excel files with separate sheets per product.

- Requirements
  - Python 3.8 or higher
  - pandas
  - numpy
  - matplotlib
  - BeautifulSoup4 (for sniim_scraping.py)
